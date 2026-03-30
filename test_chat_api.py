#!/usr/bin/env python3
"""测试聊天API"""
import json
import requests

def test_chat_api():
    """测试聊天端点"""
    url = "http://127.0.0.1:8000/api/chat"

    # 测试数据
    payload = {
        "message": "头痛发烧怎么办？",
        "user_id": "test_user",
        "session_id": ""
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return True
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_health():
    """测试健康检查"""
    url = "http://127.0.0.1:8000/health"
    try:
        response = requests.get(url, timeout=5)
        print(f"健康检查: {response.json()}")
        return True
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_version():
    """测试版本端点"""
    url = "http://127.0.0.1:8000/api/version"
    try:
        response = requests.get(url, timeout=5)
        print(f"版本信息: {response.json()}")
        return True
    except Exception as e:
        print(f"版本检查失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试聊天API ===")

    # 测试健康检查
    print("\n1. 测试健康检查...")
    if not test_health():
        print("健康检查失败，服务器可能未启动")
        exit(1)

    # 测试版本端点
    print("\n2. 测试版本信息...")
    test_version()

    # 测试聊天端点
    print("\n3. 测试聊天端点...")
    success = test_chat_api()

    if success:
        print("\n[OK] 聊天API测试通过")
    else:
        print("\n[ERROR] 聊天API测试失败")