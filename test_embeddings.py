#!/usr/bin/env python3
"""测试嵌入模型"""
import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== 嵌入模型测试 ===\n")

# 测试Ollama连接
print("1. 测试Ollama连接...")
try:
    import requests
    from app.config import settings

    url = f"{settings.ollama_base_url}/api/tags"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        models = [model["name"] for model in response.json().get("models", [])]
        print(f"  可用的Ollama模型: {models}")

        if settings.ollama_embed_model in models:
            print(f"  成功: 嵌入模型 '{settings.ollama_embed_model}' 可用")
        else:
            print(f"  错误: 嵌入模型 '{settings.ollama_embed_model}' 不可用")
            print(f"    请运行: ollama pull {settings.ollama_embed_model}")
    else:
        print(f"  错误: Ollama连接失败: HTTP {response.status_code}")
except Exception as e:
    print(f"  [ERROR] Ollama连接错误: {e}")

# 测试嵌入模型
print("\n2. 测试嵌入模型初始化...")
try:
    from langchain_ollama import OllamaEmbeddings
    from app.config import settings

    embeddings = OllamaEmbeddings(
        model=settings.ollama_embed_model,
        base_url=settings.ollama_base_url
    )
    print(f"  [OK] 嵌入模型初始化成功: {settings.ollama_embed_model}")

    # 测试嵌入查询
    print("\n3. 测试嵌入查询...")
    test_text = "感冒症状包括打喷嚏、流鼻涕"

    print(f"  查询文本: {test_text}")
    start_time = time.time()

    try:
        embedding = embeddings.embed_query(test_text)
        elapsed = time.time() - start_time

        if embedding:
            print(f"  [OK] 嵌入查询成功")
            print(f"    向量维度: {len(embedding)}")
            print(f"    耗时: {elapsed:.2f} 秒")
            print(f"    前5个值: {embedding[:5]}")
        else:
            print(f"  [ERROR] 嵌入查询返回空结果")

    except Exception as e:
        print(f"  [ERROR] 嵌入查询错误: {e}")
        import traceback
        traceback.print_exc()

    # 测试批量嵌入
    print("\n4. 测试批量嵌入...")
    test_texts = ["感冒症状", "阿莫西林用法", "糖尿病治疗"]

    print(f"  批量文本: {test_texts}")
    start_time = time.time()

    try:
        batch_embeddings = embeddings.embed_documents(test_texts)
        elapsed = time.time() - start_time

        if batch_embeddings and len(batch_embeddings) == len(test_texts):
            print(f"  [OK] 批量嵌入成功")
            print(f"    文档数量: {len(batch_embeddings)}")
            print(f"    耗时: {elapsed:.2f} 秒")
            print(f"    每个向量的维度: {len(batch_embeddings[0])}")
        else:
            print(f"  [ERROR] 批量嵌入结果不匹配")
            print(f"    预期: {len(test_texts)}, 实际: {len(batch_embeddings) if batch_embeddings else 0}")

    except Exception as e:
        print(f"  [ERROR] 批量嵌入错误: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"  [ERROR] 嵌入模型初始化错误: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")