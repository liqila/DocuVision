# 多模态文档解析服务 (Multimodal Document Parser)

一个基于Python的多模态文档解析服务，支持多种文档格式的智能解析，包括文本提取、图像分析和结构化数据处理。本项目使用OpenAI Vision API进行图像分析，支持多语言处理。

## 🌟 主要特性

- **多格式支持**：
  - PDF文档
  - Word文档 (.doc, .docx)
  - Excel表格 (.xls, .xlsx)
  - PowerPoint演示文稿 (.ppt, .pptx)
  - 图片文件 (.png, .jpg, .jpeg, .gif, .bmp, .webp)
  - 文本文件 (.txt, .log, .csv, .json, .yaml, .xml, .md)

- **智能处理**：
  - 文本提取和OCR
  - 图像内容分析
  - 表格数据结构化
  - 多语言自动识别

- **高性能设计**：
  - 异步处理
  - 模块化架构
  - 可扩展API

## 🛠️ 技术栈

- **核心依赖**：
  ```
  python-dotenv>=0.19.0
  PyMuPDF>=1.19.0
  langchain>=0.1.0
  pydantic>=2.0.0
  pillow>=10.0.0
  langchain-openai>=0.0.2
  openai>=1.0.0
  ```

- **Web框架**：
  ```
  fastapi>=0.68.0
  uvicorn>=0.15.0
  python-multipart>=0.0.5
  ```

- **文档处理**：
  ```
  python-docx>=0.8.11
  python-pptx>=0.6.21
  pandas>=1.5.0
  openpyxl>=3.1.0
  ```

## 📦 快速开始

1. **克隆项目**：
   ```bash
   git clone <repository-url>
   cd doc-parser
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**：
   ```bash
   cp .env.example .env
   # 编辑.env文件，设置必要的配置项：
   # OPENAI_API_KEY=your-api-key
   # ENV=development
   # API_HOST=0.0.0.0
   # API_PORT=8000
   ```

4. **启动服务**：
   ```bash
   python run.py
   ```

5. **测试API**：
   ```bash
   python tests/test_api.py
   ```

## 📁 项目结构

```
doc-parser/
├── api/                # API实现
│   └── app.py         # FastAPI应用
├── config/            # 配置文件
│   ├── settings.py    # 全局设置
│   └── logging_config.py  # 日志配置
├── loaders/           # 文档加载器
│   ├── base.py       # 基础加载器
│   ├── pdf_loader.py # PDF加载器
│   ├── word_loader.py # Word加载器
│   └── ...           # 其他文档加载器
├── processors/        # 处理器
│   ├── base.py       # 基础处理器
│   └── image_extractor.py  # 图像提取器
├── services/         # 业务服务
│   └── document_service.py # 文档服务
├── tests/            # 测试文件
├── .env.example      # 环境变量示例
├── requirements.txt   # 项目依赖
└── setup.py          # 安装配置
```

## 🔧 配置说明

在`.env`文件中配置以下参数：

```
# OpenAI配置
OPENAI_API_KEY=your-api-key-here

# 环境配置
ENV=development  # development, production, lambda

# 模型配置
VISION_MODEL=gpt-4o-mini

# 服务配置
API_HOST=0.0.0.0
API_PORT=8000
```

## 📝 API使用

### 文档处理接口

```
# 处理单个或多个文档
POST /process
Content-Type: multipart/form-data

# 请求参数
files: List[UploadFile]  # 支持多文件上传

# 响应示例
{
    "file_name.pdf": [
        {
            "content": "提取的文本内容...",
            "metadata": {
                "source": "文件路径",
                "page": 1,
                "total_pages": 10,
                "images": [
                    {
                        "bbox": [x1, y1, x2, y2],
                        "content": "图像分析结果",
                        "extraction_status": "success"
                    }
                ]
            }
        }
    ]
}
```

### 健康检查接口

```
GET /health
响应: {"status": "healthy"}
```

## 🔍 特性详解

### 图像分析能力

- 使用OpenAI Vision API进行图像内容分析
- 支持多语言图像文字识别
- 智能提取图表信息
- 上下文感知的图像描述

### 文档处理能力

- PDF文档的分页处理和图像提取
- Word文档的格式保持和图表识别
- Excel表格的结构化数据提取
- PowerPoint的幻灯片内容分析
- 文本文件的智能格式识别

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🔄 更新日志

### v0.1.0 (2024-02-22)
- 初始版本发布
- 支持多种文档格式处理
- 集成OpenAI Vision API
- 实现基础API功能
- 添加完整的文档加载器
- 支持异步处理和多文件上传

## 📞 联系方式

- 项目地址：[GitHub Repository](https://github.com/yourusername/doc-parser)
- 问题反馈：请在GitHub Issues中提交
- 贡献代码：欢迎提交Pull Request

## 🙏 致谢

- OpenAI - 提供Vision API支持
- FastAPI - 优秀的Web框架
- LangChain - 强大的LLM应用框架
- 所有贡献者和用户

## 📚 相关资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [OpenAI API文档](https://platform.openai.com/docs)
- [LangChain文档](https://python.langchain.com/docs/get_started/introduction)