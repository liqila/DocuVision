from typing import List, Dict
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path
from services.document_service import DocumentService

app = FastAPI(title="Document Parser API")
doc_service = DocumentService()

# 添加云函数处理器
def create_lambda_handler():
    from mangum import Mangum
    return Mangum(app)

def create_gcp_handler():
    from functions_framework import create_app
    return create_app(target=app)

def create_azure_handler():
    import azure.functions as func
    async def main(req: func.HttpRequest) -> func.HttpResponse:
        return await app(req)
    return main

# AWS Lambda handler
handler = create_lambda_handler()

@app.post("/process")
async def process_documents(files: List[UploadFile] = File(...)):
    """Process multiple documents"""
    try:
        results = {}
        
        # 使用/tmp目录用于云函数环境
        temp_dir = "/tmp" if os.getenv("ENV") in ["lambda", "cloud"] else tempfile.gettempdir()
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded files
        file_paths = []
        for file in files:
            temp_path = Path(temp_dir) / file.filename
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            file_paths.append(str(temp_path))
        
        # Process documents
        doc_results = doc_service.process_documents(file_paths)
        
        # Clean up
        for path in file_paths:
            try:
                os.remove(path)
            except:
                pass
            
        # Convert Document objects to dict for JSON response
        for file_path, documents in doc_results.items():
            results[Path(file_path).name] = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documents
            ]
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy"} 