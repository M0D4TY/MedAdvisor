# MedAdvisor 医疗顾问系统

一个基于 AI 大语言模型的医疗顾问聊天系统，使用 RAG（检索增强生成）技术提供智能医疗咨询。

## ✨ 功能特点

- 🤖 **智能对话**: 基于本地 LLM 的医疗问答助手
- 📚 **知识检索**: 使用向量数据库存储和检索医疗知识
- 💬 **友好界面**: 简洁的 Web 聊天界面，支持快速提问
- 🔄 **实时响应**: 流式输出，快速返回答案
- 🌐 **跨平台**: 支持桌面和移动设备访问

## 🛠 技术栈

- **后端**: FastAPI + Uvicorn
- **AI 框架**: LangChain + LangGraph
- **向量数据库**: ChromaDB
- **嵌入模型**: sentence-transformers
- **本地 LLM**: Ollama
- **前端**: HTML5 + CSS3 + JavaScript

## 📋 环境要求

- Python 3.10+
- Ollama (本地运行 LLM)
- 4GB+ RAM

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/M0D4TY/MedAdvisor.git
cd MedAdvisor
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动 Ollama

确保已安装并运行 Ollama：

```bash
ollama serve
ollama pull llama3
```

### 4. 启动服务

```bash
python run_server.py
```

或手动启动：

```bash
set PYTHONPATH=%CD%
python -m uvicorn app.api.app:create_app --host 127.0.0.1 --port 8000
```

### 5. 访问前端

- 方式一：打开 `simple_frontend.html` 文件
- 方式二：访问 `http://localhost:8000`

## 📁 项目结构

```
MedAdvisor/
├── app/
│   └── api/
│       └── app.py          # 主应用代码
├── simple_frontend.html    # 简易前端界面
├── run_server.py           # 服务启动脚本
├── requirements.txt        # Python 依赖
├── FRONTEND_README.md     # 前端使用说明
└── test_*.py              # 测试文件
```

## 💬 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/chat` | POST | 聊天接口 |
| `/api/version` | GET | 版本信息 |

## 🔧 常见问题

**Q: 无法连接到服务器？**
A: 确保后端服务已启动，端口 8000 未被占用

**Q: 聊天没有响应？**
A: 检查 Ollama 是否正常运行，模型是否已下载

**Q: 回答质量不好？**
A: 可以调整知识库内容或更换 LLM 模型

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请提交 Issue
