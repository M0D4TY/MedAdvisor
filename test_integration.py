"""系统集成测试"""
import sys
import time
import subprocess
import requests
import json

def test_api_health():
    """测试健康检查端点"""
    print("测试健康检查端点...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"[OK] 健康检查通过: {response.json()}")
            return True
        else:
            print(f"[ERROR] 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] 健康检查异常: {e}")
        return False

def test_chat_api():
    """测试聊天API"""
    print("\n测试聊天API...")
    try:
        payload = {
            "message": "我有点头痛，怎么办？",
            "user_id": "test_user"
        }
        response = requests.post(
            "http://localhost:8000/api/chat",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 聊天API响应成功")
            print(f"  响应内容: {data['response'][:100]}...")
            print(f"  处理时间: {data['processing_time']:.2f}秒")
            print(f"  会话ID: {data['session_id']}")
            return True
        else:
            print(f"[ERROR] 聊天API失败: {response.status_code}")
            print(f"  响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] 聊天API异常: {e}")
        return False

def test_agent_direct():
    """直接测试Agent"""
    print("\n直接测试Agent...")
    try:
        sys.path.insert(0, '.')
        from app.agents import get_medical_agent, AgentContext

        agent = get_medical_agent()
        context = AgentContext(
            user_id="test_user",
            session_id="test_session_123",
            user_query="感冒有什么症状？"
        )

        result = agent.process_query("感冒有什么症状？", context)

        if result["success"]:
            print(f"[OK] Agent测试成功")
            print(f"  回复: {result['response'][:100]}...")
            print(f"  处理时间: {result['processing_time']:.2f}秒")
            return True
        else:
            print(f"[ERROR] Agent测试失败: {result.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"[ERROR] Agent测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=== 医疗顾问客服系统集成测试 ===")

    # 检查服务器是否运行
    print("检查服务器状态...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        server_running = response.status_code == 200
    except:
        server_running = False

    if not server_running:
        print("服务器未运行，跳过API测试")
        # 只测试Agent
        agent_ok = test_agent_direct()
        return agent_ok
    else:
        print("服务器正在运行，执行完整测试")
        health_ok = test_api_health()
        chat_ok = test_chat_api()
        agent_ok = test_agent_direct()

        return health_ok and chat_ok and agent_ok

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] 所有测试通过！")
        sys.exit(0)
    else:
        print("\n[FAILED] 部分测试失败")
        sys.exit(1)