#!/usr/bin/env python3
"""最小化测试向量存储"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("导入模块...")
try:
    from app.services.vector_store import VectorStoreService
    print("导入成功")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n创建向量存储服务...")
try:
    service = VectorStoreService()
    print("创建成功")

    stats = service.get_collection_stats()
    print(f"集合统计: {stats}")

    # 尝试搜索
    print("\n尝试搜索...")
    results = service.search_similar("感冒", top_k=1)
    print(f"搜索结果: {len(results)} 个")

    if results:
        print(f"第一个结果: {results[0]['metadata'].get('title', 'No title')}")
    else:
        print("无结果")

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()