#!/usr/bin/env python3
"""简单测试聊天API"""
import json
import requests
import sys

def test_chat_with_timeout(timeout=30):
    """测试聊天端点，带超时"""
    url = "http://127.0.0.1:8000/api/chat"

    # 简单消息
    payload = {
        "message": "你好",
        "user_id": "test_user_1",
        "session_id": ""
    }

    try:
        print(f"发送请求到聊天端点 (超时: {timeout}秒)...")
        response = requests.post(url, json=payload, timeout=timeout)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"成功! 响应:")
            print(f"  session_id: {result.get('session_id')}")
            print(f"  processing_time: {result.get('processing_time')}")
            print(f"  response: {result.get('response')[:100]}...")
            return result
        else:
            print(f"错误: {response.status_code}")
            print(f"响应: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print(f"请求超时 (超过{timeout}秒)")
        return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def test_history(session_id):
    """测试历史端点"""
    if not session_id:
        print("无session_id，跳过历史测试")
        return

    url = f"http://127.0.0.1:8000/api/history/{session_id}"

    try:
        response = requests.get(url, timeout=5)
        print(f"\n历史端点状态码: {response.status_code}")
        if response.status_code == 200:
            history_data = response.json()
            print(f"历史数据: {json.dumps(history_data, ensure_ascii=False, indent=2)}")
            return history_data
        else:
            print(f"历史端点错误: {response.text}")
            return None
    except Exception as e:
        print(f"历史请求失败: {e}")
        return None

if __name__ == "__main__":
    print("=== 简单聊天API测试 ===\n")

    # 测试聊天
    result = test_chat_with_timeout(30)

    if result:
        session_id = result.get('session_id')
        # 测试历史
        test_history(session_id)
        print("\n[OK] 测试完成")
        sys.exit(0)
    else:
        print("\n[ERROR] 聊天测试失败")
        sys.exit(1)