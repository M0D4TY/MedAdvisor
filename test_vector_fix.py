#!/usr/bin/env python3
"""测试向量存储修复"""
import sys
import os
import uuid

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_embedding_model():
    """测试嵌入模型"""
    print("测试嵌入模型...")
    try:
        from app.config import settings
        from langchain_ollama import OllamaEmbeddings

        embeddings = OllamaEmbeddings(
            model=settings.ollama_embed_model,
            base_url=settings.ollama_base_url
        )

        # 测试嵌入
        text = "感冒症状"
        print(f"  嵌入文本: {text}")
        result = embeddings.embed_query(text)
        print(f"  嵌入向量维度: {len(result)}")
        print(f"  前5个值: {result[:5]}")

        # 测试批量嵌入
        texts = ["感冒症状", "阿莫西林用法"]
        results = embeddings.embed_documents(texts)
        print(f"  批量嵌入: {len(results)} 个文档")

        return True
    except Exception as e:
        print(f"  嵌入模型错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vector_store_add():
    """测试向量存储添加文档"""
    print("\n测试向量存储添加文档...")
    try:
        from app.services.vector_store import VectorStoreService

        service = VectorStoreService()
        print(f"  初始文档数: {service.get_collection_stats()['document_count']}")

        # 创建测试文档
        test_doc = {
            'id': str(uuid.uuid4()),
            'title': '感冒症状测试',
            'content': '感冒常见症状包括打喷嚏、流鼻涕、喉咙痛、咳嗽、发热等。症状通常在感染后1-3天出现，持续7-10天。',
            'category': 'symptom',
            'source': '测试修复'
        }

        print(f"  添加测试文档: {test_doc['title']}")
        doc_ids = service.add_documents([test_doc])
        print(f"  添加的文档ID: {doc_ids}")

        # 检查数量
        stats = service.get_collection_stats()
        print(f"  添加后文档数: {stats['document_count']}")

        # 测试搜索
        results = service.search_similar("感冒有哪些症状？", top_k=2)
        print(f"  搜索结果数量: {len(results)}")

        if results:
            for i, result in enumerate(results, 1):
                print(f"    {i}. {result['metadata']['title']}")
                print(f"       相关度: {result['relevance']}")
                print(f"       内容: {result['content'][:50]}...")
        else:
            print("   无搜索结果")

        return True

    except Exception as e:
        print(f"  向量存储错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_init_script():
    """测试初始化脚本"""
    print("\n测试初始化脚本...")
    try:
        from scripts.init_knowledge import initialize_vector_store

        print("  运行初始化向量存储...")
        service = initialize_vector_store()

        stats = service.get_collection_stats()
        print(f"  初始化后文档数: {stats['document_count']}")

        # 测试搜索
        test_queries = ["感冒症状", "阿莫西林", "糖尿病"]

        for query in test_queries:
            print(f"  查询: {query}")
            results = service.search_similar(query, top_k=2)
            print(f"    找到 {len(results)} 个结果")
            for r in results:
                print(f"    - {r['metadata']['title']}")

        return True

    except Exception as e:
        print(f"  初始化脚本错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=== 向量存储修复测试 ===\n")

    tests = [
        ("嵌入模型", test_embedding_model),
        ("向量存储添加", test_vector_store_add),
        ("初始化脚本", test_init_script),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n[{test_name}]")
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"{test_name}测试异常: {e}")
            results.append((test_name, False))

    # 打印摘要
    print("\n=== 测试结果摘要 ===")
    all_passed = True
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"  {test_name}: {status}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n✓ 所有测试通过！向量存储应该可以正常工作。")
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