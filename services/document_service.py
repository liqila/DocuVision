from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
from langchain_core.documents import Document
from loaders.factory import DocumentLoaderFactory

logger = logging.getLogger(__name__)

class DocumentService:
    """Document processing service"""
    
    def __init__(self):
        self.loader_factory = DocumentLoaderFactory()
    
    def process_document(self, file_path: str) -> List[Document]:
        """Process a single document"""
        logger.info(f"Processing document: {file_path}")
        try:
            loader = self.loader_factory.get_loader(file_path)
            documents = loader.load()
            logger.info(f"Successfully processed document: {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Failed to process document: {file_path}", exc_info=True)
            raise
    
    def process_documents(self, file_paths: List[str], config: Optional[Dict[str, Any]] = None) -> Dict[str, List[Document]]:
        """
        Process multiple documents
        
        Args:
            file_paths: List of paths to document files
            config: Optional configuration for document processing
            
        Returns:
            Dict[str, List[Document]]: Mapping of file paths to their processed documents
        """
        results = {}
        
        for file_path in file_paths:
            try:
                results[file_path] = self.process_document(file_path)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {str(e)}")
                results[file_path] = [Document(
                    page_content=f"Failed to process document: {str(e)}",
                    metadata={
                        "source": file_path,
                        "extraction_status": "failed",
                        "error": str(e)
                    }
                )]
        
        return results 