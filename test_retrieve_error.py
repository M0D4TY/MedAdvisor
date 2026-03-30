#!/usr/bin/env python3
"""测试检索错误"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.vector_store import VectorStoreService

def test_retrieve():
    print("测试向量检索...")
    service = VectorStoreService()

    # 测试查询
    queries = ["感冒症状", "头痛", "测试"]

    for query in queries:
        print(f"\n查询: '{query}'")
        try:
            results = service.search_similar(query, top_k=2)
            print(f"  成功，找到 {len(results)} 个结果")
            for i, r in enumerate(results, 1):
                print(f"    {i}. {r['metadata'].get('title', '无标题')}")
        except Exception as e:
            print(f"  错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_retrieve()