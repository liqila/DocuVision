# Multimodal Document Parser

A Python-based multimodal document parsing service that supports intelligent parsing of various document formats, including text extraction, image analysis, and structured data processing. This project uses OpenAI Vision API for image analysis and supports multilingual processing.

## 🌟 Key Features

- **Multi-format Support**:
  - PDF Documents
  - Word Documents (.doc, .docx)
  - Excel Spreadsheets (.xls, .xlsx)
  - PowerPoint Presentations (.ppt, .pptx)
  - Images (.png, .jpg, .jpeg, .gif, .bmp, .webp)
  - Text Files (.txt, .log, .csv, .json, .yaml, .xml, .md)

- **Intelligent Processing**:
  - Text Extraction and OCR
  - Image Content Analysis
  - Table Data Structuring
  - Multilingual Recognition

- **High-Performance Design**:
  - Asynchronous Processing
  - Modular Architecture
  - Extensible API

## 🛠️ Tech Stack

- **Core Dependencies**:
  ```
  python-dotenv>=0.19.0
  PyMuPDF>=1.19.0
  langchain>=0.1.0
  pydantic>=2.0.0
  pillow>=10.0.0
  langchain-openai>=0.0.2
  openai>=1.0.0
  ```

- **Web Framework**:
  ```
  fastapi>=0.68.0
  uvicorn>=0.15.0
  python-multipart>=0.0.5
  ```

- **Document Processing**:
  ```
  python-docx>=0.8.11
  python-pptx>=0.6.21
  pandas>=1.5.0
  openpyxl>=3.1.0
  ```

## 📦 Quick Start

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/liqila/DocuVision.git
   cd DocuVision
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env file with required settings:
   # OPENAI_API_KEY=your-api-key
   # ENV=development
   # API_HOST=0.0.0.0
   # API_PORT=8000
   ```

4. **Start the Service**:
   ```bash
   python run.py
   ```

5. **Test the API**:
   ```bash
   python tests/test_api.py
   ```

## 📁 Project Structure

```
doc-parser/
├── api/                # API implementation
│   └── app.py         # FastAPI application with cloud function handlers
├── config/            # Configuration files
│   ├── settings.py    # Global settings
│   └── logging_config.py  # Logging configuration
├── loaders/           # Document loaders
│   ├── base.py       # Base loader
│   ├── pdf_loader.py # PDF loader
│   └── ...           # Other loaders
├── processors/        # Processors
│   ├── base.py       # Base processor
│   └── image_extractor.py  # Image extractor
├── services/         # Business services
│   └── document_service.py # Document service
├── tests/            # Test files
├── .env.example      # Environment variables example
├── requirements.txt   # Project dependencies
└── setup.py          # Installation configuration
```

## 🔧 Configuration

Configure the following parameters in `.env`:

```
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here

# Environment Configuration
ENV=development  # development, lambda, gcp, azure

# Cloud Provider Configuration
CLOUD_PROVIDER=local  # local, aws, gcp, azure

# Model Configuration
VISION_MODEL=gpt-4o-mini

# Service Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### AWS Lambda
```bash
# Install Serverless Framework
npm install -g serverless

# Deploy
serverless deploy
```

### Google Cloud Functions
```bash
# Deploy to GCP
gcloud functions deploy docuvision \
    --runtime python39 \
    --trigger-http \
    --entry-point create_gcp_handler
```

### Azure Functions
```bash
# Deploy to Azure
func azure functionapp publish YourFunctionAppName
```

## 🌩️ Cloud Environment Support

### AWS Lambda
- Uses Mangum adapter for AWS Lambda integration
- Automatic CloudWatch logging integration
- `/tmp` directory for temporary file storage

### Google Cloud Functions
- Native Functions Framework integration
- Cloud Logging support
- Temporary storage in function runtime

### Azure Functions
- Azure Functions HTTP trigger support
- Application Insights logging integration
- Local temp storage handling

## 📝 API Usage

### Document Processing Endpoint

```
# Process single or multiple documents
POST /process
Content-Type: multipart/form-data

# Request Parameters
files: List[UploadFile]  # Supports multiple file uploads

# Response Example
{
    "file_name.pdf": [
        {
            "content": "Extracted text content...",
            "metadata": {
                "source": "file_path",
                "page": 1,
                "total_pages": 10,
                "images": [
                    {
                        "bbox": [x1, y1, x2, y2],
                        "content": "Image analysis result",
                        "extraction_status": "success"
                    }
                ]
            }
        }
    ]
}
```

### Health Check Endpoint

```
GET /health
Response: {"status": "healthy"}
```

## 🔍 Feature Details

### Image Analysis Capabilities

- OpenAI Vision API integration for image content analysis
- Multilingual text recognition in images
- Intelligent chart and graph extraction
- Context-aware image description

### Document Processing Capabilities

- PDF page processing and image extraction
- Word document format preservation and table recognition
- Excel structured data extraction
- PowerPoint slide content analysis
- Intelligent text file format recognition

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🔄 Changelog

### v0.1.0 (2025-02-23)
- Initial release
- Multi-format document support
- OpenAI Vision API integration
- Basic API implementation
- Complete document loader suite
- Async processing and multi-file upload support
- Cloud function deployment support (AWS, GCP, Azure)

## 📞 Contact

- Author: Frank Li <liqila@gmail.com>
- Project Link: [GitHub Repository](https://github.com/liqila/DocuVision)
- Issue Tracker: [Submit via GitHub Issues](https://github.com/liqila/DocuVision/issues)
- Contributing: [Pull requests](https://github.com/liqila/DocuVision/pulls) are welcome

## 🙏 Acknowledgments

- OpenAI - For Vision API support
- FastAPI - Excellent web framework
- LangChain - Powerful LLM application framework
- All contributors and users

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [AWS Lambda Python Runtime](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- [Google Cloud Functions Python Runtime](https://cloud.google.com/functions/docs/concepts/python-runtime)
- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)