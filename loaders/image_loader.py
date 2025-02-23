from typing import List
import logging
from pathlib import Path
from langchain_core.documents import Document
from .base import BaseDocumentLoader
from processors.image_extractor import ImageExtractor

logger = logging.getLogger(__name__)

class ImageLoader(BaseDocumentLoader):
    """Image document loader - extracts information from images"""
    
    def __init__(self, file_path: str):
        """Initialize loader"""
        super().__init__(file_path)
        self.image_extractor = ImageExtractor()
        
    def load(self) -> List[Document]:
        """Load image and extract information"""
        try:
            # Check file exists
            image_path = Path(self.file_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            # Process image
            logger.info(f"Processing image: {image_path}")
            extraction_result = self.image_extractor.extract_info(image_path)
            
            if extraction_result["status"] == "success":
                # Create Document object
                doc = Document(
                    page_content=extraction_result["content"],
                    metadata={
                        "source": str(image_path),
                        "file_type": "image",
                        "file_name": image_path.name,
                        "extraction_status": "success"
                    }
                )
                return [doc]
            else:
                # Handle extraction failure
                error_doc = Document(
                    page_content=f"Image processing failed: {extraction_result.get('error', 'Unknown error')}",
                    metadata={
                        "source": str(image_path),
                        "file_type": "image",
                        "file_name": image_path.name,
                        "extraction_status": "failed",
                        "error": extraction_result.get("error")
                    }
                )
                return [error_doc]
                
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}", exc_info=True)
            # Return error document
            error_doc = Document(
                page_content=f"Failed to load image: {str(e)}",
                metadata={
                    "source": str(self.file_path),
                    "file_type": "image",
                    "extraction_status": "failed",
                    "error": str(e)
                }
            )
            return [error_doc] 