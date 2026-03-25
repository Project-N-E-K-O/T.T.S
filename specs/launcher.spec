# -*- mode: python ; coding: utf-8 -*-
"""
T.T.S (Talking Twin Simulator) 主程序打包配置
包含 main_server + memory_server，不包含 agent_server
"""
import sys
import os
import platform
from PyInstaller.utils.hooks import collect_all

# 获取 spec 文件所在目录和项目根目录
SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))
PROJECT_ROOT = os.path.dirname(SPEC_DIR)

# 切换到项目根目录
original_dir = os.getcwd()
os.chdir(PROJECT_ROOT)

print(f"[Build] SPEC_DIR: {SPEC_DIR}")
print(f"[Build] PROJECT_ROOT: {PROJECT_ROOT}")
print(f"[Build] Working from: {os.getcwd()}")

# 收集所有必要的依赖
datas = []
binaries = []
hiddenimports = []

# 收集关键包（T.T.S 不需要 browser_use / langchain）
critical_packages = [
    'dashscope',
    'openai',
    'sqlalchemy',
]

for pkg in critical_packages:
    try:
        tmp_ret = collect_all(pkg)
        datas += tmp_ret[0]
        binaries += tmp_ret[1]
        hiddenimports += tmp_ret[2]
    except Exception as e:
        print(f"Warning: Could not collect {pkg}: {e}")

# 添加配置文件
import glob
config_json_files = glob.glob(os.path.join(PROJECT_ROOT, 'config/*.json'))
print(f"[Build] Packing {len(config_json_files)} config files:")
for json_file in config_json_files:
    print(f"  - {json_file}")
    datas.append((json_file, 'config'))

def add_data(src, dest):
    """添加数据文件，支持通配符"""
    src_path = os.path.join(PROJECT_ROOT, src)
    if '*' in src:
        files = glob.glob(src_path)
        if files:
            for f in files:
                datas.append((f, dest))
        else:
            print(f"[Build] Warning: No files matched pattern '{src}', skipping")
    elif os.path.exists(src_path):
        datas.append((src_path, dest))
    else:
        print(f"[Build] Warning: {src_path} not found, skipping")

# 静态资源
add_data('static/css', 'static/css')
add_data('static/js', 'static/js')
add_data('static/fonts', 'static/fonts')
add_data('static/vrm', 'static/vrm')
add_data('static/mao_pro', 'static/mao_pro')
add_data('static/ziraitikuwa', 'static/ziraitikuwa')
add_data('static/libs', 'static/libs')
add_data('static/icons', 'static/icons')
add_data('static/locales', 'static/locales')
add_data('static/neko', 'static/neko')
add_data('static/kemomimi', 'static/kemomimi')
add_data('static/default', 'static/default')
add_data('static/*.js', 'static')
add_data('static/*.json', 'static')
add_data('static/*.ico', 'static')
add_data('static/*.png', 'static')
add_data('assets', 'assets')
add_data('templates', 'templates')

# Steam 相关（如果存在）
add_data('steam_appid.txt', '.')

if sys.platform == 'darwin':
    for dll_name in ['libsteam_api.dylib', 'SteamworksPy.dylib']:
        dll_path = os.path.join(PROJECT_ROOT, dll_name)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))
elif sys.platform == 'win32':
    for dll_name in ['steam_api64.dll', 'SteamworksPy64.dll', 'steam_api64.lib']:
        dll_path = os.path.join(PROJECT_ROOT, dll_name)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))

# 隐藏导入（T.T.S: main + memory，不含 agent/brain/browser_use/langchain）
hiddenimports += [
    # Uvicorn
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.websockets.websockets_impl',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',

    # FastAPI
    'fastapi',
    'fastapi.responses',
    'fastapi.staticfiles',
    'starlette',
    'starlette.staticfiles',
    'starlette.templating',

    # 模板引擎
    'jinja2',
    'jinja2.ext',

    # WebSocket
    'websockets',
    'websocket',

    # AI
    'openai',
    'dashscope',
    'httpx',

    # 音频
    'librosa',
    'soundfile',
    'pyaudio',
    'numpy',

    # 图像处理（screenshot_utils 需要）
    'PIL',
    'PIL.Image',

    # 数据库（memory 需要）
    'sqlalchemy',

    # 工具
    'inflect',
    'typeguard',
    'typeguard._decorators',
    'requests',
    'cachetools',
    'aiohttp',
    'regex',

    # 项目主模块（不含 agent_server）
    'main_server',
    'memory_server',
    'monitor',

    # config
    'config',
    'config.api',
    'config.prompts_sys',
    'config.prompts_chara',

    # main_logic
    'main_logic',
    'main_logic.core',
    'main_logic.cross_server',
    'main_logic.omni_offline_client',
    'main_logic.omni_realtime_client',
    'main_logic.tts_client',
    'main_logic.agent_event_bus',

    # main_routers
    'main_routers',
    'main_routers.config_router',
    'main_routers.characters_router',
    'main_routers.live2d_router',
    'main_routers.workshop_router',
    'main_routers.memory_router',
    'main_routers.pages_router',
    'main_routers.websocket_router',
    'main_routers.agent_router',
    'main_routers.system_router',
    'main_routers.shared_state',

    # memory
    'memory',
    'memory.recent',
    'memory.router',
    'memory.semantic',
    'memory.settings',
    'memory.timeindex',

    # utils
    'utils',
    'utils.audio',
    'utils.config_manager',
    'utils.frontend_utils',
    'utils.logger_config',
    'utils.preferences',
    'utils.web_scraper',
    'utils.workshop_utils',
    'utils.token_tracker',

    # Steam（可选）
    'steamworks',
    'steamworks.enums',
    'steamworks.structs',
    'steamworks.exceptions',
    'steamworks.methods',
    'steamworks.util',
    'steamworks.interfaces',
    'steamworks.interfaces.apps',
    'steamworks.interfaces.friends',
    'steamworks.interfaces.matchmaking',
    'steamworks.interfaces.music',
    'steamworks.interfaces.screenshots',
    'steamworks.interfaces.users',
    'steamworks.interfaces.userstats',
    'steamworks.interfaces.utils',
    'steamworks.interfaces.workshop',
    'steamworks.interfaces.microtxn',
    'steamworks.interfaces.input',

    # plugin
    'plugin',
    'plugin.settings',
    'plugin.user_plugin_server',
    'plugin.api',
    'plugin.api.exceptions',
    'plugin.api.models',
    'plugin.core',
    'plugin.core.context',
    'plugin.core.state',
    'plugin.runtime',
    'plugin.sdk',
    'plugin.sdk.base',
    'plugin.sdk.decorators',
    'plugin.sdk.events',
    'plugin.sdk.logger',
    'plugin.sdk.version',
    'plugin.server',
    'plugin.server.exceptions',
    'plugin.server.lifecycle',
    'plugin.server.services',
    'plugin.server.utils',
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'launcher.py')],
    pathex=[PROJECT_ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除 agent 相关的重型依赖
        'browser_use',
        'langchain',
        'langchain_community',
        'langchain_core',
        'langchain_openai',
        'gui_agents',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='tts_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=True if sys.platform == 'darwin' else False,
    target_arch=platform.machine() if sys.platform == 'darwin' else None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(PROJECT_ROOT, 'assets/icon.ico') if sys.platform == 'win32' and os.path.exists(os.path.join(PROJECT_ROOT, 'assets/icon.ico')) else None,
    version=os.path.join(PROJECT_ROOT, 'version_info.txt') if sys.platform == 'win32' and os.path.exists(os.path.join(PROJECT_ROOT, 'version_info.txt')) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='T.T.S',
)

os.chdir(original_dir)
