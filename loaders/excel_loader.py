from typing import List
import logging
from pathlib import Path
import pandas as pd
from langchain_core.documents import Document
from .base import BaseDocumentLoader

logger = logging.getLogger(__name__)

class ExcelLoader(BaseDocumentLoader):
    """Excel document loader - extracts data from spreadsheets"""
    
    def __init__(self, file_path: str):
        """Initialize loader"""
        super().__init__(file_path)
    
    def _process_sheet(self, df: pd.DataFrame, sheet_name: str) -> str:
        """Process a single sheet"""
        content_parts = [f"\n=== Sheet: {sheet_name} ===\n"]
        
        # Convert DataFrame to string representation
        if not df.empty:
            # Add column headers
            headers = " | ".join(str(col) for col in df.columns)
            content_parts.append(headers)
            content_parts.append("-" * len(headers))
            
            # Add rows
            for _, row in df.iterrows():
                row_str = " | ".join(str(val) for val in row.values)
                content_parts.append(row_str)
        
        return "\n".join(content_parts)
    
    def load(self) -> List[Document]:
        """Load Excel document and extract content"""
        try:
            # Check file exists
            excel_path = Path(self.file_path)
            if not excel_path.exists():
                raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
            # Load workbook
            logger.info(f"Loading Excel document: {excel_path}")
            
            # Read all sheets
            content_parts = []
            sheet_info = []
            
            excel_file = pd.ExcelFile(excel_path)
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                # Process sheet
                sheet_content = self._process_sheet(df, sheet_name)
                content_parts.append(sheet_content)
                
                # Record sheet info
                sheet_info.append({
                    "name": sheet_name,
                    "rows": len(df),
                    "columns": len(df.columns)
                })
            
            # Create Document object
            doc = Document(
                page_content="\n\n".join(content_parts),
                metadata={
                    "source": str(excel_path),
                    "file_type": "excel",
                    "file_name": excel_path.name,
                    "sheets": sheet_info
                }
            )
            
            return [doc]
            
        except Exception as e:
            logger.error(f"Error loading Excel document: {str(e)}", exc_info=True)
            # Return error document
            error_doc = Document(
                page_content=f"Failed to load Excel document: {str(e)}",
                metadata={
                    "source": str(self.file_path),
                    "file_type": "excel",
                    "extraction_status": "failed",
                    "error": str(e)
                }
            )
            return [error_doc] 