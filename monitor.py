# -*- coding: utf-8 -*-
import sys, os
if getattr(sys, 'frozen', False):
    # 打包环境：数据文件从 exe 旁边的 _internal/ 读（与 tts_server 共用）
    _exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    _shared_internal = os.path.join(_exe_dir, '_internal')
    if os.path.isdir(_shared_internal):
        _PROJECT_ROOT = _shared_internal
    elif hasattr(sys, '_MEIPASS'):
        _PROJECT_ROOT = sys._MEIPASS
    else:
        _PROJECT_ROOT = _exe_dir
else:
    _PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # 确保 CWD 指向项目根，find_models() 等使用相对路径 'static'
import mimetypes
mimetypes.add_type("application/javascript", ".js")
import asyncio
import json
import logging
from contextlib import asynccontextmanager
from config import MONITOR_SERVER_PORT, MAIN_SERVER_PORT
from utils.config_manager import get_config_manager, get_reserved
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import uvicorn
from fastapi.templating import Jinja2Templates
from utils.frontend_utils import find_models, find_model_config_file, find_model_directory
from utils.workshop_utils import get_default_workshop_folder
from utils.preferences import load_user_preferences

# Setup logger
from utils.logger_config import setup_logging
logger, log_config = setup_logging(service_name="Monitor", log_level=logging.INFO)

# 获取资源路径（支持打包后的环境）
def get_resource_path(relative_path):
    """获取资源的绝对路径，支持开发环境和打包后的环境"""
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

templates = Jinja2Templates(directory=get_resource_path(""))

# 存储所有连接的客户端
connected_clients = set()
subtitle_clients = set()
current_subtitle = ""
should_clear_next = False


async def cleanup_disconnected_clients():
    """定期清理断开的连接"""
    while True:
        try:
            for client in list(connected_clients):
                try:
                    await client.send_json({"type": "heartbeat"})
                except Exception as e:
                    logger.warning(f"心跳检测失败，移除客户端: {e}")
                    connected_clients.discard(client)
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"清理客户端错误: {e}")
            await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan: 启动/关闭时的资源管理"""
    task = asyncio.create_task(cleanup_disconnected_clients())
    logger.info(f"Monitor 服务已启动，端口: {MONITOR_SERVER_PORT}")
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=get_resource_path("static")), name="static")
_config_manager = get_config_manager()

# 挂载用户Live2D目录（与main_server.py保持一致，CFA感知）
_readable_live2d = _config_manager.readable_live2d_dir
_serve_live2d_path = str(_readable_live2d) if _readable_live2d else str(_config_manager.live2d_dir)
if os.path.exists(_serve_live2d_path):
    app.mount("/user_live2d", StaticFiles(directory=_serve_live2d_path), name="user_live2d")
    logger.info(f"已挂载用户Live2D目录: {_serve_live2d_path}")
# CFA 场景：可写回退目录额外挂载
if _readable_live2d and str(_config_manager.live2d_dir) != _serve_live2d_path:
    _writable_live2d_path = str(_config_manager.live2d_dir)
    if os.path.exists(_writable_live2d_path):
        app.mount("/user_live2d_local", StaticFiles(directory=_writable_live2d_path), name="user_live2d_local")
        logger.info(f"已挂载本地Live2D目录(CFA回退): {_writable_live2d_path}")

# 挂载创意工坊目录（与main_server.py保持一致）
workshop_path = get_default_workshop_folder()
if workshop_path and os.path.exists(workshop_path):
    app.mount("/workshop", StaticFiles(directory=workshop_path), name="workshop")
    logger.info(f"已挂载创意工坊目录: {workshop_path}")

@app.get("/")
async def root_redirect():
    """根路径：重定向到当前角色的 viewer 页面"""
    try:
        _, her_name, _, _, _, _, _, _, _ = _config_manager.get_character_data()
    except Exception:
        her_name = ""
    if her_name:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=f"/{her_name}")
    return HTMLResponse("<h3>No character configured</h3>", status_code=404)

@app.get("/subtitle")
async def get_subtitle():
    return FileResponse(get_resource_path('templates/subtitle.html'))

@app.get("/api/config/page_config")
async def get_page_config(lanlan_name: str = ""):
    """获取页面配置（lanlan_name 和 model_path）"""
    try:
        _, her_name, _, lanlan_basic_config, _, _, _, _, _ = _config_manager.get_character_data()
        target_name = lanlan_name if lanlan_name else her_name

        # 大小写不敏感匹配角色名（URL 可能使用小写）
        char_data = lanlan_basic_config.get(target_name, {})
        if not char_data and target_name:
            target_lower = target_name.lower()
            for key in lanlan_basic_config:
                if key.lower() == target_lower:
                    target_name = key  # 使用 config 里的真实名称
                    char_data = lanlan_basic_config[key]
                    break

        live2d_model_path = get_reserved(
            char_data,
            'avatar',
            'live2d',
            'model_path',
            default='mao_pro',
            legacy_keys=('live2d',),
        )
        if not isinstance(live2d_model_path, str):
            live2d_model_path = str(live2d_model_path) if live2d_model_path is not None else 'mao_pro'
        if live2d_model_path.endswith('.model3.json'):
            parts = live2d_model_path.replace('\\', '/').split('/')
            live2d = parts[-2] if len(parts) >= 2 else parts[-1].removesuffix('.model3.json')
        else:
            live2d = live2d_model_path

        models = find_models()
        model_path = next((m["path"] for m in models if m["name"] == live2d), find_model_config_file(live2d))

        return {
            "success": True,
            "lanlan_name": target_name,
            "model_path": model_path
        }
    except Exception as e:
        logger.error(f"获取页面配置失败: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/config/preferences")
async def get_preferences():
    """获取用户偏好设置（与main_server.py保持一致）"""
    preferences = load_user_preferences()
    return preferences

@app.post("/api/config/preferences")
async def save_preferences_readonly():
    """Monitor 为只读模式，不允许保存偏好设置"""
    return JSONResponse(status_code=200, content={"success": True, "readonly": True})

@app.post("/api/emotion/analysis")
async def emotion_analysis_proxy(request: Request):
    """代理情绪分析请求到主服务器"""
    import aiohttp
    try:
        data = await request.json()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://127.0.0.1:{MAIN_SERVER_PORT}/api/emotion/analysis",
                json=data,
                timeout=aiohttp.ClientTimeout(total=10.0)
            ) as resp:
                result = await resp.json()
                return JSONResponse(status_code=resp.status, content=result)
    except aiohttp.ClientError as e:
        logger.warning(f"情绪分析代理失败（主服务器可能未运行）: {e}")
        return JSONResponse(status_code=502, content={"error": "主服务器不可达"})
    except Exception as e:
        logger.error(f"情绪分析代理错误: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get('/api/live2d/emotion_mapping/{model_name}')
def get_emotion_mapping(model_name: str):
    """获取情绪映射配置"""
    try:
        model_dir, _ = find_model_directory(model_name)
        if not model_dir or not os.path.exists(model_dir):
            return JSONResponse(status_code=404, content={"success": False, "error": "模型目录不存在"})

        model_json_path = None
        for file in os.listdir(model_dir):
            if file.endswith('.model3.json'):
                model_json_path = os.path.join(model_dir, file)
                break

        if not model_json_path or not os.path.exists(model_json_path):
            return JSONResponse(status_code=404, content={"success": False, "error": "模型配置文件不存在"})

        with open(model_json_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        emotion_mapping = config_data.get('EmotionMapping')
        if not emotion_mapping:
            derived_mapping = {"motions": {}, "expressions": {}}
            file_refs = config_data.get('FileReferences', {}) or {}

            motions = file_refs.get('Motions', {}) or {}
            for group_name, items in motions.items():
                files = []
                for item in items or []:
                    try:
                        file_path = item.get('File') if isinstance(item, dict) else None
                        if file_path:
                            files.append(file_path.replace('\\', '/'))
                    except Exception:
                        continue
                derived_mapping["motions"][group_name] = files

            expressions = file_refs.get('Expressions', []) or []
            for item in expressions:
                if not isinstance(item, dict):
                    continue
                name = item.get('Name') or ''
                file_path = item.get('File') or ''
                if not file_path:
                    continue
                file_path = file_path.replace('\\', '/')
                if '_' in name:
                    group = name.split('_', 1)[0]
                else:
                    group = 'neutral'
                derived_mapping["expressions"].setdefault(group, []).append(file_path)

            emotion_mapping = derived_mapping

        return {"success": True, "config": emotion_mapping}
    except Exception as e:
        logger.error(f"获取情绪映射配置失败: {e}")
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

def _locate_model_config(model_dir: str):
    """在模型目录及其一级子目录中查找 .model3.json 文件"""
    if not os.path.isdir(model_dir):
        return None, None, None
    for file in os.listdir(model_dir):
        if file.endswith('.model3.json'):
            return model_dir, file, None
    try:
        for subdir in os.listdir(model_dir):
            subdir_path = os.path.join(model_dir, subdir)
            if not os.path.isdir(subdir_path):
                continue
            for file in os.listdir(subdir_path):
                if file.endswith('.model3.json'):
                    return subdir_path, file, subdir
    except Exception as e:
        logger.warning(f"检查子目录时出错: {e}")
    return None, None, None


@app.get('/api/live2d/model_files/{model_name}')
def get_model_files(model_name: str):
    """获取指定 Live2D 模型的动作和表情文件列表"""
    try:
        model_dir, _ = find_model_directory(model_name)
        if not model_dir or not os.path.exists(model_dir):
            return {"success": False, "error": f"模型 {model_name} 不存在"}

        actual_model_dir, model_config_file, _ = _locate_model_config(model_dir)
        if not model_config_file:
            return {"success": False, "error": "模型配置文件(.model3.json)不存在"}

        model_dir = actual_model_dir
        motion_files = []
        expression_files = []

        def search_files_recursive(directory, target_ext, result_list):
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isfile(item_path):
                        if item.endswith(target_ext):
                            relative_path = os.path.relpath(item_path, model_dir).replace('\\', '/')
                            result_list.append(relative_path)
                    elif os.path.isdir(item_path):
                        search_files_recursive(item_path, target_ext, result_list)
            except Exception as e:
                logger.warning(f"搜索目录 {directory} 时出错: {e}")

        search_files_recursive(model_dir, '.motion3.json', motion_files)
        search_files_recursive(model_dir, '.exp3.json', expression_files)

        return {"success": True, "motion_files": motion_files, "expression_files": expression_files}
    except Exception as e:
        logger.error(f"获取模型文件列表失败: {e}")
        return {"success": False, "error": str(e)}


@app.get('/api/live2d/load_model_parameters/{model_name}')
def load_model_parameters(model_name: str):
    """从模型目录的 parameters.json 文件加载参数"""
    try:
        model_dir, _ = find_model_directory(model_name)
        if not model_dir or not os.path.exists(model_dir):
            return {"success": False, "error": f"模型 {model_name} 不存在"}

        parameters_file = os.path.join(model_dir, 'parameters.json')
        if not os.path.exists(parameters_file):
            return {"success": True, "parameters": {}}

        with open(parameters_file, 'r', encoding='utf-8') as f:
            parameters = json.load(f)

        if not isinstance(parameters, dict):
            return {"success": True, "parameters": {}}

        return {"success": True, "parameters": parameters}
    except Exception as e:
        logger.error(f"加载模型参数失败: {e}")
        return {"success": False, "error": str(e), "parameters": {}}


@app.get("/{lanlan_name}", response_class=HTMLResponse)
async def get_index(request: Request, lanlan_name: str):
    return templates.TemplateResponse("templates/viewer.html", {
        "request": request
    })


@app.websocket("/subtitle_ws")
async def subtitle_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info(f"字幕客户端已连接: {websocket.client}")

    subtitle_clients.add(websocket)

    try:
        if current_subtitle:
            await websocket.send_json({
                "type": "subtitle",
                "text": current_subtitle
            })
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info(f"字幕客户端已断开: {websocket.client}")
    finally:
        subtitle_clients.discard(websocket)


async def broadcast_subtitle():
    """广播字幕到所有字幕客户端"""
    global current_subtitle, should_clear_next
    if should_clear_next:
        await clear_subtitle()
        should_clear_next = False
        await asyncio.sleep(0.3)

    clients = subtitle_clients.copy()
    for client in clients:
        try:
            await client.send_json({
                "type": "subtitle",
                "text": current_subtitle
            })
        except Exception as e:
            logger.warning(f"字幕广播错误: {e}")
            subtitle_clients.discard(client)


async def clear_subtitle():
    """清空字幕"""
    global current_subtitle
    current_subtitle = ""

    clients = subtitle_clients.copy()
    for client in clients:
        try:
            await client.send_json({
                "type": "clear"
            })
        except Exception as e:
            logger.warning(f"清空字幕错误: {e}")
            subtitle_clients.discard(client)


# 主服务器连接端点
@app.websocket("/sync/{lanlan_name}")
async def sync_endpoint(websocket: WebSocket, lanlan_name: str):
    await websocket.accept()
    logger.info(f"[SYNC] 主服务器已连接: {websocket.client}")

    try:
        while True:
            try:
                global current_subtitle
                data = await asyncio.wait_for(websocket.receive_text(), timeout=25)

                data = json.loads(data)
                msg_type = data.get("type", "unknown")

                if msg_type == "gemini_response":
                    subtitle_text = data.get("text", "")
                    current_subtitle += subtitle_text
                    if subtitle_text:
                        await broadcast_subtitle()

                elif msg_type == "turn end":
                    # 回合结束，准备清空字幕（下一条消息到来时清空）
                    global should_clear_next
                    should_clear_next = True

                if msg_type != "heartbeat":
                    await broadcast_message(data)
            except asyncio.exceptions.TimeoutError:
                pass
    except WebSocketDisconnect:
        logger.info(f"[SYNC] 主服务器已断开: {websocket.client}")
    except Exception as e:
        logger.error(f"[SYNC] 同步端点错误: {e}")


# 二进制数据同步端点
@app.websocket("/sync_binary/{lanlan_name}")
async def sync_binary_endpoint(websocket: WebSocket, lanlan_name: str):
    await websocket.accept()
    logger.info(f"[BINARY] 主服务器二进制连接已建立: {websocket.client}")

    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_bytes(), timeout=25)
                if len(data) > 4:
                    await broadcast_binary(data)
            except asyncio.exceptions.TimeoutError:
                pass
    except WebSocketDisconnect:
        logger.info(f"[BINARY] 主服务器二进制连接已断开: {websocket.client}")
    except Exception as e:
        logger.error(f"[BINARY] 二进制同步端点错误: {e}")


# 客户端连接端点
@app.websocket("/ws/{lanlan_name}")
async def websocket_endpoint(websocket: WebSocket, lanlan_name: str):
    await websocket.accept()
    logger.info(f"[CLIENT] 查看客户端已连接: {websocket.client}, 当前总数: {len(connected_clients) + 1}")

    connected_clients.add(websocket)

    try:
        while True:
            try:
                await websocket.receive_text()
            except Exception:
                try:
                    await websocket.receive_bytes()
                except Exception:
                    await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        logger.info(f"[CLIENT] 查看客户端已断开: {websocket.client}")
    except Exception as e:
        logger.warning(f"[CLIENT] 客户端连接异常: {e}")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"[CLIENT] 已移除客户端，当前剩余: {len(connected_clients)}")


async def broadcast_message(message):
    """广播消息到所有客户端"""
    clients = connected_clients.copy()
    disconnected_clients = []

    for client in clients:
        try:
            await client.send_json(message)
        except Exception as e:
            logger.warning(f"[BROADCAST] 广播错误到 {client.client}: {e}")
            disconnected_clients.append(client)

    for client in disconnected_clients:
        connected_clients.discard(client)


async def broadcast_binary(data):
    """广播二进制数据到所有客户端"""
    clients = connected_clients.copy()
    disconnected_clients = []

    for client in clients:
        try:
            await client.send_bytes(data)
        except Exception as e:
            logger.warning(f"[BINARY BROADCAST] 二进制广播错误到 {client.client}: {e}")
            disconnected_clients.append(client)

    for client in disconnected_clients:
        connected_clients.discard(client)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=MONITOR_SERVER_PORT, reload=False)
