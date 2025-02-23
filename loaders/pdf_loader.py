from typing import List, Dict, Tuple
import fitz  # PyMuPDF
import logging
from pathlib import Path
import io
from PIL import Image
from langchain_core.documents import Document
from .base import BaseDocumentLoader
from processors.image_extractor import ImageExtractor

logger = logging.getLogger(__name__)

class PDFLoader(BaseDocumentLoader):
    """PDF document loader - extracts text and images"""
    
    def __init__(self, file_path: str):
        """Initialize loader"""
        super().__init__(file_path)
        self.image_extractor = ImageExtractor()
    
    def _get_context_text(self, content_parts: List[Dict], current_idx: int, window: int = 2) -> str:
        """
        Get surrounding text context for an image
        
        Args:
            content_parts: List of content parts (text/images)
            current_idx: Current position index
            window: Number of text blocks to include before and after
            
        Returns:
            str: Combined context text
        """
        start_idx = max(0, current_idx - window)
        end_idx = min(len(content_parts), current_idx + window + 1)
        
        context = []
        for idx in range(start_idx, end_idx):
            if idx == current_idx:
                continue
            if content_parts[idx]["type"] == "text":
                context.append(content_parts[idx]["content"])
        
        return "\n".join(context)
    
    def _extract_page_content(self, page: fitz.Page, page_num: int, start_image_index: int = 1) -> Tuple[str, List[dict]]:
        """Extract text and image content from a page"""
        blocks = page.get_text("dict")["blocks"]
        content_parts = []
        processed_images = []
        
        for block in blocks:
            bbox = block["bbox"]
            y_pos = bbox[1]
            
            if block["type"] == 0:  # Text block
                if "lines" in block:
                    text = ""
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip():
                                text += span["text"] + " "
                    if text.strip():
                        content_parts.append({
                            "type": "text",
                            "content": text.strip(),
                            "position": y_pos
                        })
            
            elif block["type"] == 1:  # Image block
                try:
                    image_index = len(processed_images) + start_image_index
                    content_parts.append({
                        "type": "image",
                        "image_index": image_index,
                        "position": y_pos
                    })
                    
                    # Get context
                    context = self._get_context_text(content_parts, len(content_parts) - 1)
                    
                    try:
                        # Get image in memory
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=bbox)
                        
                        # Convert to bytes stream
                        img_byte_arr = io.BytesIO(pix.tobytes("png"))
                        
                        # Process image with extractor
                        extraction_result = self.image_extractor.extract_info(img_byte_arr)
                        
                        # Record image info
                        image_info = {
                            "bbox": bbox,
                            "context": context,
                            "extraction_status": extraction_result["status"]
                        }
                        
                        if extraction_result["status"] == "success":
                            image_info["extracted_content"] = extraction_result["content"]
                            
                            # Update content with XML-style markup
                            content_parts[-1]["content"] = (
                                f'<image id="{image_index:03d}">\n'
                                f'{extraction_result["content"]}\n'
                                f'</image>'
                            )
                        else:
                            image_info["error"] = extraction_result.get("error")
                            content_parts[-1]["content"] = (
                                f'<image id="{image_index:03d}" status="failed">\n'
                                f'Image processing failed: {extraction_result.get("error", "Unknown error")}\n'
                                f'</image>'
                            )
                            
                        processed_images.append(image_info)
                        
                    except Exception as e:
                        logger.error(f"Failed to process image: {str(e)}")
                        processed_images.append({
                            "bbox": bbox,
                            "context": context,
                            "error": str(e)
                        })
                    
                except Exception as e:
                    logger.warning(f"Failed to extract image: {str(e)}")
        
        # Sort by position
        content_parts.sort(key=lambda x: x["position"])
        
        # Generate final text
        final_text = []
        for part in content_parts:
            if part["type"] == "text":
                final_text.append(part["content"])
            else:  # image
                content = part.get("content", f'<image id="{part["image_index"]:03d}" status="unprocessed"/>')
                final_text.append(content)
        
        return "\n".join(final_text), processed_images

    def load(self) -> List[Document]:
        """Load PDF document, extract text and images"""
        pdf_doc = fitz.open(self.file_path)
        documents = []
        current_image_index = 1
        
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            
            # Extract page content and images
            text, images = self._extract_page_content(
                page, 
                page_num + 1,
                current_image_index
            )
            current_image_index += len(images)
            
            # Create Document object
            doc = Document(
                page_content=text,
                metadata={
                    "source": str(self.file_path),
                    "page": page_num + 1,
                    "total_pages": len(pdf_doc),
                    "images": images
                }
            )
            documents.append(doc)
        
        pdf_doc.close()
        return documents 