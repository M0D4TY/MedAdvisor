#!/usr/bin/env python3
"""清理并测试向量数据库"""
import sys
import os
import shutil
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def cleanup_chroma_db():
    """清理Chroma数据库"""
    print("清理Chroma数据库...")
    chroma_path = "data/chroma_db"

    if os.path.exists(chroma_path):
        try:
            shutil.rmtree(chroma_path)
            print(f"  已删除: {chroma_path}")
            return True
        except Exception as e:
            print(f"  删除失败: {e}")
            return False
    else:
        print(f"  目录不存在: {chroma_path}")
        return True

def test_embeddings():
    """测试嵌入模型"""
    print("\n测试嵌入模型...")
    try:
        from langchain_ollama import OllamaEmbeddings
        from app.config import settings

        embeddings = OllamaEmbeddings(
            model=settings.ollama_embed_model,
            base_url=settings.ollama_base_url
        )

        # 测试简单嵌入
        text = "感冒症状"
        start = time.time()
        embedding = embeddings.embed_query(text)
        elapsed = time.time() - start

        if embedding and len(embedding) > 0:
            print(f"  成功: 嵌入维度 {len(embedding)}, 耗时 {elapsed:.2f}s")
            return True
        else:
            print("  失败: 无嵌入结果")
            return False

    except Exception as e:
        print(f"  错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vector_store():
    """测试向量存储"""
    print("\n测试向量存储...")
    try:
        from app.services.vector_store import VectorStoreService

        # 创建服务
        service = VectorStoreService()
        print(f"  创建向量存储服务")

        # 检查初始状态
        stats = service.get_collection_stats()
        print(f"  初始文档数: {stats['document_count']}")

        # 添加测试文档
        import uuid
        test_docs = [
            {
                'id': str(uuid.uuid4()),
                'title': '感冒症状',
                'content': '感冒常见症状包括打喷嚏、流鼻涕、喉咙痛、咳嗽、发热等。',
                'category': 'symptom',
                'source': '测试'
            },
            {
                'id': str(uuid.uuid4()),
                'title': '阿莫西林',
                'content': '阿莫西林是青霉素类抗生素，用于治疗细菌感染。',
                'category': 'medicine',
                'source': '测试'
            }
        ]

        print(f"  添加 {len(test_docs)} 个测试文档...")
        doc_ids = service.add_documents(test_docs)
        print(f"  添加的文档ID: {doc_ids}")

        # 检查添加后的状态
        stats = service.get_collection_stats()
        print(f"  添加后文档数: {stats['document_count']}")

        # 测试搜索
        print("  测试搜索...")
        queries = ["感冒症状", "抗生素"]

        for query in queries:
            results = service.search_similar(query, top_k=2)
            print(f"    查询 '{query}': 找到 {len(results)} 个结果")
            for i, r in enumerate(results, 1):
                print(f"      {i}. {r['metadata']['title']} (相关度: {r['relevance']})")

        return True

    except Exception as e:
        print(f"  错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_knowledge_init():
    """测试知识库初始化"""
    print("\n测试知识库初始化...")
    try:
        from scripts.init_knowledge import initialize_vector_store

        print("  运行初始化脚本...")
        service = initialize_vector_store()

        stats = service.get_collection_stats()
        print(f"  初始化后文档数: {stats['document_count']}")

        # 测试搜索
        test_queries = ["感冒症状", "阿莫西林用法", "糖尿病"]

        for query in test_queries:
            results = service.search_similar(query, top_k=2)
            if results:
                print(f"    查询 '{query}': ✓ 找到 {len(results)} 个结果")
            else:
                print(f"    查询 '{query}': ✗ 无结果")

        return True

    except Exception as e:
        print(f"  错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=== 向量数据库清理与测试 ===\n")

    # 清理
    if not cleanup_chroma_db():
        print("清理失败，退出")
        return False

    # 测试
    tests = [
        ("嵌入模型", test_embeddings),
        ("向量存储", test_vector_store),
        ("知识库初始化", test_knowledge_init),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"测试异常: {e}")
            results.append((test_name, False))

    # 打印结果
    print("\n=== 测试结果 ===")
    all_passed = True
    for test_name, success in results:
        status = "通过" if success else "失败"
        print(f"  {test_name}: {status}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n✓ 所有测试通过！向量数据库现在应该可以正常工作。")
    else:
        print("\n✗ 部分测试失败，需要进一步检查。")

    return all_passed

if __name__ == "__main__":
    # Windows编码处理
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    success = main()
    sys.exit(0 if success else 1)