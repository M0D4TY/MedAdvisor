#!/usr/bin/env python3
"""测试修复后的应用"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有关键模块导入"""
    print("测试模块导入...")
    try:
        from app.config import settings
        print("  ✓ 配置模块导入成功")

        from app.agents.medical_agent import MedicalAgent, AgentContext
        print("  ✓ Agent模块导入成功")

        from app.services.vector_store import VectorStoreService
        print("  ✓ 向量存储模块导入成功")

        from app.database.models import SessionLocal, init_db
        print("  ✓ 数据库模块导入成功")

        from app.api.app import create_app
        print("  ✓ API应用模块导入成功")

        return True
    except Exception as e:
        print(f"  ✗ 导入错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """测试配置加载"""
    print("\n测试配置加载...")
    try:
        from app.config import settings
        print(f"  应用名称: {settings.app_name}")
        print(f"  版本: {settings.app_version}")
        print(f"  Ollama模型: {settings.ollama_chat_model}")
        print(f"  数据库路径: {settings.sqlite_path}")
        return True
    except Exception as e:
        print(f"  ✗ 配置错误: {e}")
        return False

def test_database():
    """测试数据库连接"""
    print("\n测试数据库连接...")
    try:
        from app.database.models import SessionLocal, init_db
        from sqlalchemy import text
        # 初始化数据库（如果不存在）
        init_db()

        # 测试连接
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("  ✓ 数据库连接成功")
        return True
    except Exception as e:
        print(f"  ✗ 数据库错误: {e}")
        return False

def test_vector_store():
    """测试向量存储"""
    print("\n测试向量存储...")
    try:
        from app.services.vector_store import VectorStoreService
        service = VectorStoreService()
        stats = service.get_collection_stats()
        print(f"  文档数量: {stats['document_count']}")
        print(f"  集合名称: {stats['collection_name']}")
        return True
    except Exception as e:
        print(f"  ✗ 向量存储错误: {e}")
        return False

def test_chat_fallback():
    """测试聊天回退功能（无Ollama时）"""
    print("\n测试聊天回退功能...")
    try:
        from app.api.chat import generate_temporary_response

        test_messages = [
            "我头疼怎么办",
            "阿莫西林怎么吃",
            "感冒挂什么科",
            "你好"
        ]

        for msg in test_messages:
            response = generate_temporary_response(msg)
            print(f"  输入: {msg[:20]}...")
            print(f"  响应: {response[:50]}...")
            print()

        print("  ✓ 回退功能正常")
        return True
    except Exception as e:
        print(f"  ✗ 回退功能错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_app():
    """测试FastAPI应用创建"""
    print("\n测试FastAPI应用创建...")
    try:
        from app.api.app import create_app
        app = create_app()

        # 检查路由
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)

        print(f"  已创建应用，{len(routes)}个路由")
        print(f"  示例路由: {routes[:3]}")
        print("  ✓ FastAPI应用创建成功")
        return True
    except Exception as e:
        print(f"  ✗ FastAPI应用错误: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 医疗顾问系统修复测试 ===\n")

    tests = [
        ("模块导入", test_imports),
        ("配置加载", test_config),
        ("数据库连接", test_database),
        ("向量存储", test_vector_store),
        ("聊天回退", test_chat_fallback),
        ("FastAPI应用", test_fastapi_app),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"{test_name}测试异常: {e}")
            results.append((test_name, False))

    # 打印摘要
    print("\n=== 测试结果摘要 ===")
    all_passed = True
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {test_name}: {status}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n✓ 所有测试通过！系统应该可以正常工作。")
    else:
        print("\n✗ 部分测试失败，需要进一步检查。")

    return all_passed

if __name__ == "__main__":
    # 在Windows上避免Unicode编码问题
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    success = main()
    sys.exit(0 if success else 1)