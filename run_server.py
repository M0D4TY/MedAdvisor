#!/usr/bin/env python3
"""启动医疗顾问服务器"""
import sys
import os
import subprocess
import time
import urllib.request
import json
import atexit

# 设置项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def start_server():
    """启动FastAPI服务器"""
    print("=" * 60)
    print("医疗顾问客服系统 - 服务器启动")
    print("=" * 60)

    # 检查应用创建
    print("\n[1/5] 检查应用配置...")
    try:
        from app.api.app import create_app
        app = create_app()
        print(f"   [OK] 应用创建成功 ({len(app.routes)}个路由)")
    except Exception as e:
        print(f"   [FAIL] 应用创建失败: {e}")
        return None

    # 设置环境变量
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

    # 启动命令
    cmd = [sys.executable, "-m", "uvicorn", "app.api.app:create_app",
           "--host", "127.0.0.1", "--port", "8000"]

    print(f"\n[2/5] 启动服务器...")
    print(f"   命令: {' '.join(cmd)}")
    print(f"   工作目录: {project_root}")

    # 启动服务器进程
    server_process = subprocess.Popen(
        cmd,
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # 注册退出处理函数
    def cleanup():
        if server_process.poll() is None:
            print("\n终止服务器进程...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

    atexit.register(cleanup)

    print(f"   服务器PID: {server_process.pid}")

    # 等待服务器启动
    print("\n[3/5] 等待服务器启动...")
    time.sleep(5)

    # 检查进程状态
    if server_process.poll() is not None:
        print("   [FAIL] 服务器进程已退出")
        stdout, stderr = server_process.communicate()
        print("   标准输出:")
        print(stdout[:500])
        print("\n   标准错误:")
        print(stderr[:500])
        return None

    # 测试连接
    print("\n[4/5] 测试服务器连接...")
    max_retries = 5
    connected = False

    for i in range(max_retries):
        try:
            req = urllib.request.Request('http://127.0.0.1:8000/health', timeout=5)
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode())
            print(f"   [OK] 服务器运行正常: {data}")
            connected = True
            break
        except Exception as e:
            print(f"   尝试 {i+1}/{max_retries}: 连接失败 - {e}")
            if i < max_retries - 1:
                time.sleep(2)

    if not connected:
        print("   [WARN] 服务器可能未完全启动，但进程仍在运行")

    # 显示访问信息
    print("\n[5/5] 服务器启动完成!")
    print("=" * 60)
    print("\n访问地址:")
    print(f"   主页:      http://127.0.0.1:8000")
    print(f"   API文档:   http://127.0.0.1:8000/docs")
    print(f"   健康检查:  http://127.0.0.1:8000/health")
    print(f"   聊天API:   POST http://127.0.0.1:8000/api/chat")
    print("\n配置信息:")
    print(f"   主机: 127.0.0.1")
    print(f"   端口: 8000")
    print(f"   进程ID: {server_process.pid}")
    print("\n停止服务器: 按 Ctrl+C 或关闭此窗口")
    print("=" * 60)

    return server_process

def main():
    """主函数"""
    try:
        process = start_server()
        if process is None:
            print("\n服务器启动失败，请检查错误信息")
            sys.exit(1)

        # 等待用户中断
        print("\n服务器正在运行...")
        try:
            # 等待进程结束
            stdout, stderr = process.communicate()
            print(f"服务器退出:")
            if stdout:
                print(f"标准输出:\n{stdout[:1000]}")
            if stderr:
                print(f"标准错误:\n{stderr[:1000]}")
        except KeyboardInterrupt:
            print("\n收到中断信号，停止服务器...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print("服务器已停止")
            except subprocess.TimeoutExpired:
                print("服务器未正常停止，强制终止")
                process.kill()

    except Exception as e:
        print(f"启动过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()