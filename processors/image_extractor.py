from typing import Union, Optional
import base64
import logging
import io
from pathlib import Path
from openai import OpenAI
from config.settings import VISION_MODEL_CONFIG

logger = logging.getLogger(__name__)

# 使用新的配置结构
model_config = VISION_MODEL_CONFIG["models"][VISION_MODEL_CONFIG["default_model"]]

class ImageExtractor:
    """Image information extractor using OpenAI Vision API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize extractor with API key"""
        self.api_key = api_key or VISION_MODEL_CONFIG["api_key"]
        self.client = OpenAI(api_key=self.api_key)
    
    def _encode_image_data(self, image_data: Union[Path, io.BytesIO]) -> str:
        """Encode image data to base64 format"""
        if isinstance(image_data, Path):
            with open(image_data, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        elif isinstance(image_data, io.BytesIO):
            return base64.b64encode(image_data.getvalue()).decode("utf-8")
        else:
            raise ValueError(f"Unsupported image data type: {type(image_data)}")
    
    def extract_info(self, image_input: Union[str, Path, io.BytesIO]) -> dict:
        """Extract information from image"""
        try:
            # Handle input based on type
            if isinstance(image_input, (str, Path)):
                image_path = Path(image_input)
                if not image_path.exists():
                    raise FileNotFoundError(f"Image file not found: {image_path}")
                image_data = image_path
                image_name = image_path.name
            elif isinstance(image_input, io.BytesIO):
                image_data = image_input
                image_name = "memory_image"
            else:
                raise ValueError(f"Unsupported image input type: {type(image_input)}")
            
            try:
                # Encode image
                base64_image = self._encode_image_data(image_data)
                
                # Universal prompt that covers all scenarios
                system_prompt = """You are an expert image analyzer. Your task is to:

1. Identify and extract all text content in the image, maintaining:
   - Original language
   - Exact formatting
   - Numbers and dates accuracy
   
2. For documents (IDs, passports, certificates):
   - Extract all key information
   - Maintain field names and values
   - Preserve data structure
   
3. For tables and forms:
   - Preserve table structure
   - Extract headers and data
   - Maintain relationships between fields
   
4. For charts and graphs:
   - Describe visual elements
   - Extract data points
   - Explain trends and relationships
   
5. For general images:
   - Describe visual content
   - Note any text overlays
   - Explain context and relationships

Always maintain the original language of any text found in the image.
For pure visual content, use English for descriptions."""

                # Build messages
                messages = [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please analyze this image and extract all relevant information."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ]
                
                # Call API
                logger.info(f"Processing image: {image_name}")
                try:
                    response = self.client.chat.completions.create(
                        model=VISION_MODEL_CONFIG["default_model"],
                        messages=messages,
                        max_tokens=model_config["max_tokens"],
                        temperature=model_config["temperature"]
                    )
                    
                    # Return results
                    return {
                        "status": "success",
                        "content": response.choices[0].message.content,
                    }
                    
                except Exception as api_error:
                    logger.error(f"OpenAI API call failed: {str(api_error)}", exc_info=True)
                    raise Exception(f"API call failed: {str(api_error)}")
                
            except Exception as process_error:
                logger.error(f"Image processing error: {str(process_error)}", exc_info=True)
                raise Exception(f"Image processing failed: {str(process_error)}")
                
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            } 