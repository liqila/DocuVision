from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document
from pathlib import Path
from typing import Any

class BaseProcessor(ABC):
    """
    处理器基类
    
    所有处理器都应该继承这个基类并实现其抽象方法
    """
    
    @abstractmethod
    def process(self, *args, **kwargs) -> Any:
        """
        处理方法，需要被子类实现
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            Any: 处理结果
        """
        pass
        
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        """
        调用方法，使处理器可以像函数一样被调用
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            Any: 处理结果
        """
        pass

class BaseDocumentProcessor(ABC):
    """文档处理器基类"""
    
    @abstractmethod
    def process(self, documents: List[Document]) -> str:
        """处理文档并返回Markdown格式的结果"""
        pass 