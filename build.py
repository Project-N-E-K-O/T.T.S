# -*- coding: utf-8 -*-
"""
T.T.S (Talking Twin Simulator) 打包脚本
打包 tts_server + Monitor 到同一目录，共用 _internal
"""
import os
import sys
import shutil
import subprocess

def build():
    """打包 T.T.S"""
    print("=" * 60)
    print("打包 T.T.S (Talking Twin Simulator)")
    print("=" * 60)

    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller 未安装，正在通过 uv 安装...")
        subprocess.run(["uv", "pip", "install", "pyinstaller"], check=True)
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")

    # 清理旧的构建
    if os.path.exists("build"):
        print("\n清理 build 目录...")
        shutil.rmtree("build")

    tts_dist = os.path.join("dist", "T.T.S")
    if os.path.exists(tts_dist):
        print(f"清理 {tts_dist} 目录...")
        shutil.rmtree(tts_dist)

    # Step 1: 打包 tts_server（onedir，包含 _internal）
    print("\n[1/2] 打包 tts_server...")
    cmd = [sys.executable, "-m", "PyInstaller", "specs/launcher.spec", "--clean", "-y"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: tts_server 打包失败! {e}")
        return False

    # Step 2: 打包 Monitor（onefile，不含数据文件）
    print("\n[2/2] 打包 Monitor...")
    cmd = [sys.executable, "-m", "PyInstaller", "specs/monitor_build.spec", "--clean", "-y"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Monitor 打包失败! {e}")
        return False

    # Step 3: 将 Monitor.exe 移到 T.T.S 目录（与 tts_server 共用 _internal）
    monitor_src = os.path.join("dist", "Monitor.exe")
    monitor_dst = os.path.join("dist", "T.T.S", "Monitor.exe")
    if os.path.exists(monitor_src):
        shutil.move(monitor_src, monitor_dst)
        print(f"\n已将 Monitor.exe 移至 {monitor_dst}")
    else:
        print("\nWARNING: Monitor.exe 未找到，跳过")

    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)
    print(f"\n输出目录: dist\\T.T.S\\")
    print(f"  tts_server.exe  - 主服务器")
    print(f"  Monitor.exe     - 副屏观看")
    print(f"  _internal/      - 共用数据（static、config、templates）")
    return True

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
