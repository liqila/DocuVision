import logging
from pathlib import Path
from typing import Type
from .base import BaseDocumentLoader
from .pdf_loader import PDFLoader
from .image_loader import ImageLoader
from .word_loader import WordLoader
from .ppt_loader import PPTLoader
from .excel_loader import ExcelLoader
from .text_loader import TextLoader

logger = logging.getLogger(__name__)

class DocumentLoaderFactory:
    """Factory for creating document loaders based on file type"""
    
    # Map file extensions to loader classes
    LOADER_MAP = {
        ".pdf": PDFLoader,
        ".png": ImageLoader,
        ".jpg": ImageLoader,
        ".jpeg": ImageLoader,
        ".gif": ImageLoader,
        ".bmp": ImageLoader,
        ".webp": ImageLoader,
        ".doc": WordLoader,
        ".docx": WordLoader,
        ".ppt": PPTLoader,
        ".pptx": PPTLoader,
        ".xls": ExcelLoader,
        ".xlsx": ExcelLoader,
        ".txt": TextLoader,
        ".log": TextLoader,
        ".csv": TextLoader,
        ".json": TextLoader,
        ".yaml": TextLoader,
        ".yml": TextLoader,
        ".xml": TextLoader,
        ".md": TextLoader,
        ".markdown": TextLoader,
    }
    
    @classmethod
    def get_loader(cls, file_path: str) -> BaseDocumentLoader:
        """
        Get appropriate loader for the file
        
        Args:
            file_path: Path to the document file
            
        Returns:
            BaseDocumentLoader: Appropriate loader instance
            
        Raises:
            ValueError: If file type is not supported
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext not in cls.LOADER_MAP:
            raise ValueError(f"Unsupported file type: {ext}")
            
        loader_class = cls.LOADER_MAP[ext]
        return loader_class(file_path) 