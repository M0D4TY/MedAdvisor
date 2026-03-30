#!/usr/bin/env python3
"""快速测试向量存储"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing vector store...")
try:
    from app.services.vector_store import VectorStoreService

    print("1. Creating vector store service...")
    service = VectorStoreService()

    print(f"2. Current collection stats: {service.get_collection_stats()}")

    # Try to add a document
    import uuid
    test_doc = {
        'id': str(uuid.uuid4()),
        'title': '测试文档',
        'content': '这是一个测试文档，用于验证向量存储功能。',
        'category': 'test',
        'source': 'test'
    }

    print(f"3. Adding test document: {test_doc['title']}")
    doc_ids = service.add_documents([test_doc])
    print(f"   Added document IDs: {doc_ids}")

    print(f"4. New collection stats: {service.get_collection_stats()}")

    # Try to search
    print("5. Searching for '测试'...")
    results = service.search_similar("测试", top_k=2)
    print(f"   Found {len(results)} results")

    for i, r in enumerate(results, 1):
        print(f"   {i}. {r['metadata'].get('title', 'No title')} - {r['relevance']}")

    print("\nSUCCESS: Vector store is working!")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()