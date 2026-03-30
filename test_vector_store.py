"""测试向量存储服务"""
import sys
import os
sys.path.insert(0, '.')

from app.services.vector_store import VectorStoreService

def test_vector_service():
    """测试向量存储服务"""
    print("测试向量存储服务...")

    try:
        # 创建服务实例
        service = VectorStoreService()

        # 获取统计信息
        stats = service.get_collection_stats()
        print(f"向量数据库统计: {stats}")

        # 测试添加文档
        test_docs = [
            {
                "title": "测试症状",
                "content": "头痛、发烧、咳嗽是感冒的常见症状。",
                "category": "symptom",
                "source": "测试数据"
            },
            {
                "title": "测试药品",
                "content": "布洛芬是常用的解热镇痛药。",
                "category": "medicine",
                "source": "测试数据"
            }
        ]

        print(f"添加 {len(test_docs)} 个测试文档...")
        doc_ids = service.add_documents(test_docs)
        print(f"添加的文档ID: {doc_ids}")

        # 重新获取统计
        new_stats = service.get_collection_stats()
        print(f"添加后统计: {new_stats}")

        # 测试搜索
        print("\n测试相似度搜索...")
        results = service.search_similar("头痛发烧怎么办？", top_k=2)
        print(f"搜索到 {len(results)} 个结果")

        for i, r in enumerate(results):
            print(f"  {i+1}. {r['metadata']['title']} (相似度: {r['similarity_score']:.3f})")
            print(f"     内容: {r['content'][:80]}...")

        # 测试元数据过滤
        print("\n测试元数据过滤...")
        medicine_results = service.search_by_metadata({"category": "medicine"})
        print(f"找到 {len(medicine_results)} 个药品文档")

        # 清理测试数据
        print(f"\n清理测试文档...")
        if doc_ids:
            service.delete_documents(doc_ids)
            print(f"已删除 {len(doc_ids)} 个测试文档")

        final_stats = service.get_collection_stats()
        print(f"最终统计: {final_stats}")

        return True

    except Exception as e:
        print(f"向量存储服务测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=== 向量存储服务测试 ===")

    success = test_vector_service()

    if success:
        print("\n[SUCCESS] 向量存储服务测试通过")
        sys.exit(0)
    else:
        print("\n[FAILED] 向量存储服务测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main()