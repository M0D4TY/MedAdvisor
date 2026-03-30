#!/usr/bin/env python3
"""测试FastAPI服务器启动"""
import sys
import os
import subprocess
import time
import urllib.request
import json
import signal

# 设置项目根目录为当前目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_server_startup():
    """测试服务器启动和基本功能"""
    print("=" * 50)
    print("测试FastAPI服务器启动")
    print("=" * 50)

    # 首先测试应用创建
    print("\n1. 测试应用创建...")
    try:
        from app.api.app import create_app
        app = create_app()
        print(f"[OK] 应用创建成功，有 {len(app.routes)} 个路由")
    except Exception as e:
        print(f"[FAIL] 应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 启动服务器
    print("\n2. 启动服务器...")

    # 使用uvicorn启动服务器
    cmd = [sys.executable, "-m", "uvicorn", "app.main:main", "--host", "127.0.0.1", "--port", "8000"]

    # 启动子进程
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

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

    print(f"服务器进程PID: {server_process.pid}")
    print(f"启动命令: {' '.join(cmd)}")

    # 等待服务器启动
    print("\n3. 等待服务器启动（5秒）...")
    time.sleep(5)

    # 检查进程是否还在运行
    if server_process.poll() is not None:
        print("[FAIL] 服务器进程已退出")
        stdout, stderr = server_process.communicate()
        print("标准输出:")
        print(stdout)
        print("\n标准错误:")
        print(stderr)
        return False

    # 测试健康检查端点
    print("\n4. 测试健康检查端点...")
    max_retries = 3
    health_ok = False

    for i in range(max_retries):
        try:
            req = urllib.request.Request('http://127.0.0.1:8000/health')
            response = urllib.request.urlopen(req, timeout=5)
            data = json.loads(response.read().decode())
            print(f"[OK] 健康检查成功: {data}")
            health_ok = True
            break
        except Exception as e:
            print(f"  尝试 {i+1}/{max_retries}: 健康检查失败 - {e}")
            if i < max_retries - 1:
                time.sleep(2)

    if not health_ok:
        print("[FAIL] 健康检查失败")
        server_process.terminate()
        server_process.wait(timeout=5)
        return False

    # 测试版本端点
    print("\n5. 测试版本端点...")
    try:
        req = urllib.request.Request('http://127.0.0.1:8000/api/version')
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode())
        print(f"[OK] 版本端点成功: {data}")
    except Exception as e:
        print(f"[FAIL] 版本端点失败: {e}")
        server_process.terminate()
        server_process.wait(timeout=5)
        return False

    # 测试聊天API
    print("\n6. 测试聊天API...")
    try:
        import json as json_module
        data = json_module.dumps({"message": "你好", "user_id": "test_user"}).encode('utf-8')
        req = urllib.request.Request('http://127.0.0.1:8000/api/chat', data=data)
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, timeout=10)
        result = json_module.loads(response.read().decode())
        print(f"[OK] 聊天API成功: 收到响应 (session_id: {result.get('session_id')})")
        print(f"  响应内容: {result.get('response', '')[:100]}...")
    except Exception as e:
        print(f"[WARN] 聊天API测试失败（可能是预期内的）: {e}")

    # 停止服务器
    print("\n7. 停止服务器...")
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
        print("[OK] 服务器已停止")
    except subprocess.TimeoutExpired:
        print("[WARN] 服务器未正常停止，强制终止")
        server_process.kill()
        server_process.wait()

    print("\n" + "=" * 50)
    print("服务器测试完成")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = test_server_startup()
    sys.exit(0 if success else 1)