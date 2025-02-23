from typing import List, Dict
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path
from services.document_service import DocumentService

app = FastAPI(title="Document Parser API")
doc_service = DocumentService()

@app.post("/process")
async def process_documents(files: List[UploadFile] = File(...)):
    """Process multiple documents"""
    try:
        results = {}
        
        # Create temporary directory for uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            file_paths = []
            for file in files:
                temp_path = Path(temp_dir) / file.filename
                with open(temp_path, "wb") as f:
                    f.write(await file.read())
                file_paths.append(str(temp_path))
            
            # Process documents
            doc_results = doc_service.process_documents(file_paths)
            
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