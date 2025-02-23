from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import json
import csv
import yaml
import xml.etree.ElementTree as ET
from langchain_core.documents import Document
from .base import BaseDocumentLoader

logger = logging.getLogger(__name__)

class TextLoader(BaseDocumentLoader):
    """Text document loader - handles various text formats"""
    
    # 文档类型分类
    DOCUMENT_TYPES = {
        # 纯文本类
        'plain_text': ['.txt', '.log', '.md', '.markdown'],
        # 结构化文本类
        'structured': {
            'csv': ['.csv'],
            'json': ['.json'],
            'yaml': ['.yaml', '.yml'],
            'xml': ['.xml']
        }
    }
    
    def __init__(self, file_path: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize loader
        
        Args:
            file_path: Path to text file
            config: Optional configuration for text processing
                - encoding: File encoding (default: utf-8)
                - csv_delimiter: CSV field delimiter (default: ,)
                - json_indent: JSON formatting indent (default: 2)
                - preserve_format: Keep original formatting (default: True)
        """
        super().__init__(file_path)
        self.config = {
            'encoding': 'utf-8',
            'csv_delimiter': ',',
            'json_indent': 2,
            'preserve_format': True
        }
        if config:
            self.config.update(config)
    
    def _get_document_type(self, ext: str) -> str:
        """Determine document type from extension"""
        # 检查纯文本类型
        if ext in self.DOCUMENT_TYPES['plain_text']:
            return 'plain_text'
        
        # 检查结构化文本类型
        for format_type, extensions in self.DOCUMENT_TYPES['structured'].items():
            if ext in extensions:
                return format_type
        
        raise ValueError(f"Unsupported text file type: {ext}")
    
    def _load_plain_text(self, file_path: Path) -> str:
        """Load plain text file"""
        with open(file_path, 'r', encoding=self.config['encoding']) as f:
            return f.read()
    
    def _load_csv(self, file_path: Path) -> str:
        """Load CSV file"""
        content_parts = []
        with open(file_path, 'r', encoding=self.config['encoding']) as f:
            reader = csv.reader(f, delimiter=self.config['csv_delimiter'])
            for row in reader:
                content_parts.append(" | ".join(row))
        return "\n".join(content_parts)
    
    def _load_json(self, file_path: Path) -> str:
        """Load JSON file"""
        with open(file_path, 'r', encoding=self.config['encoding']) as f:
            data = json.load(f)
            if self.config['preserve_format']:
                return json.dumps(data, indent=self.config['json_indent'], 
                                ensure_ascii=False)
            return str(data)
    
    def _load_yaml(self, file_path: Path) -> str:
        """Load YAML file"""
        with open(file_path, 'r', encoding=self.config['encoding']) as f:
            data = yaml.safe_load(f)
            if self.config['preserve_format']:
                return yaml.dump(data, allow_unicode=True)
            return str(data)
    
    def _load_xml(self, file_path: Path) -> str:
        """Load XML file"""
        tree = ET.parse(file_path)
        if self.config['preserve_format']:
            return ET.tostring(tree.getroot(), encoding='unicode', method='xml')
        return ET.tostring(tree.getroot(), encoding='unicode', method='text')
    
    def load(self) -> List[Document]:
        """Load text document"""
        try:
            # Check file exists
            file_path = Path(self.file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Determine document type
            ext = file_path.suffix.lower()
            doc_type = self._get_document_type(ext)
            
            # Load content based on type
            if doc_type == 'plain_text':
                content = self._load_plain_text(file_path)
            elif doc_type == 'csv':
                content = self._load_csv(file_path)
            elif doc_type == 'json':
                content = self._load_json(file_path)
            elif doc_type == 'yaml':
                content = self._load_yaml(file_path)
            elif doc_type == 'xml':
                content = self._load_xml(file_path)
            
            # Create Document object
            doc = Document(
                page_content=content,
                metadata={
                    "source": str(file_path),
                    "file_type": doc_type,
                    "file_name": file_path.name,
                    "encoding": self.config['encoding']
                }
            )
            
            return [doc]
            
        except Exception as e:
            logger.error(f"Error loading text document: {str(e)}", exc_info=True)
            return [Document(
                page_content=f"Failed to load text document: {str(e)}",
                metadata={
                    "source": str(self.file_path),
                    "extraction_status": "failed",
                    "error": str(e)
                }
            )] 