"""修复嵌入模型配置"""
import sys
import os
sys.path.insert(0, '.')

from langchain_ollama import OllamaEmbeddings
from app.config import settings

def test_ollama_embeddings():
    """测试Ollama嵌入模型"""
    print("测试Ollama嵌入模型...")

    try:
        # 创建嵌入模型实例
        embeddings = OllamaEmbeddings(
            model=settings.ollama_embed_model,
            base_url=settings.ollama_base_url
        )

        # 测试简单文本嵌入
        test_text = "感冒有什么症状？"
        print(f"测试文本: {test_text}")

        # 获取嵌入向量
        vector = embeddings.embed_query(test_text)
        print(f"嵌入向量维度: {len(vector)}")
        print(f"前5个值: {vector[:5]}")

        # 测试批量嵌入
        texts = ["头痛", "发烧", "咳嗽"]
        batch_vectors = embeddings.embed_documents(texts)
        print(f"批量嵌入结果: {len(batch_vectors)} 个向量")

        return True

    except Exception as e:
        print(f"嵌入模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_ollama_models():
    """检查Ollama模型是否可用"""
    print("\n检查Ollama模型...")

    try:
        import requests
        response = requests.get(f"{settings.ollama_base_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"已安装的模型: {len(models)} 个")
            for model in models:
                print(f"  - {model['name']}")

            # 检查所需模型
            chat_model_exists = any(settings.ollama_chat_model in model['name'] for model in models)
            embed_model_exists = any(settings.ollama_embed_model in model['name'] for model in models)

            print(f"\n聊天模型 '{settings.ollama_chat_model}': {'[OK] 已安装' if chat_model_exists else '[ERROR] 未安装'}")
            print(f"嵌入模型 '{settings.ollama_embed_model}': {'[OK] 已安装' if embed_model_exists else '[ERROR] 未安装'}")

            return chat_model_exists and embed_model_exists

    except Exception as e:
        print(f"检查Ollama模型失败: {e}")
        return False

def fix_embedding_config():
    """修复嵌入模型配置"""
    print("\n修复嵌入模型配置...")

    # 如果mxbai-embed-large不可用，使用nomic-embed-text作为备选
    alternative_model = "nomic-embed-text:latest"

    try:
        # 检查备选模型
        import requests
        response = requests.get(f"{settings.ollama_base_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])

            if any(alternative_model in model['name'] for model in models):
                print(f"备选模型 '{alternative_model}' 可用")

                # 更新配置建议
                print(f"\n建议更新配置:")
                print(f"在 app/config.py 中修改:")
                print(f"ollama_embed_model = \"{alternative_model}\"")

                # 测试备选模型
                print(f"\n测试备选模型...")
                embeddings = OllamaEmbeddings(
                    model=alternative_model,
                    base_url=settings.ollama_base_url
                )

                test_text = "测试文本"
                vector = embeddings.embed_query(test_text)
                print(f"备选模型嵌入成功，维度: {len(vector)}")

                return True
            else:
                print(f"备选模型 '{alternative_model}' 未安装")
                print(f"请运行: ollama pull {alternative_model}")
                return False

    except Exception as e:
        print(f"修复配置失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 嵌入模型修复工具 ===")

    # 检查Ollama模型
    models_ok = check_ollama_models()

    if not models_ok:
        print("\nOllama模型不完整，请安装所需模型:")
        print(f"1. 安装聊天模型: ollama pull {settings.ollama_chat_model}")
        print(f"2. 安装嵌入模型: ollama pull {settings.ollama_embed_model}")
        print(f"3. 或使用备选嵌入模型: ollama pull nomic-embed-text")

    # 测试嵌入模型
    print("\n" + "="*50)
    embedding_test = test_ollama_embeddings()

    if not embedding_test:
        print("\n嵌入模型测试失败，尝试修复...")
        fix_embedding_config()

    print("\n" + "="*50)
    if embedding_test:
        print("[SUCCESS] 嵌入模型测试通过")
    else:
        print("[ERROR] 嵌入模型测试失败，请检查Ollama配置")

if __name__ == "__main__":
    main()