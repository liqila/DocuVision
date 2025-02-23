from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseDocumentLoader(ABC):
    """文档加载器基类"""
    
    def __init__(self, file_path: str):
        """初始化加载器
        
        Args:
            file_path: 文档文件路径
        """
        self.file_path = file_path
    
    @abstractmethod
    def load(self) -> List[Document]:
        """加载文档
        
        Returns:
            List[Document]: Document对象列表
        """
        pass 