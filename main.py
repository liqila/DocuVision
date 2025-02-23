import logging
from pathlib import Path
from datetime import datetime
import json
import argparse

from loaders.factory import DocumentLoaderFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_document_loader(file_path: str):
    """Test document loader"""
    logger.info("="*50)
    logger.info("Starting document loading test")
    logger.info(f"File: {file_path}")
    logger.info("="*50)
    
    try:
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output")
        timestamp_dir = output_dir / timestamp
        timestamp_dir.mkdir(parents=True, exist_ok=True)
        
        # Get appropriate loader and process document
        loader = DocumentLoaderFactory.get_loader(file_path)
        documents = loader.load()
        
        # Save results
        for idx, doc in enumerate(documents):
            # Save content
            content_file = timestamp_dir / "content.txt"
            with open(content_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- Document {idx+1} ---\n")
                f.write(doc.page_content)
                f.write("\n")
            
            # Save metadata
            metadata_file = timestamp_dir / "metadata.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(doc.metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Processing completed, results saved in: {timestamp_dir}")
        
    except Exception as e:
        logger.error(f"Document loading test failed: {str(e)}", exc_info=True)

def process_directory(dir_path: str):
    """Process all supported documents in a directory"""
    dir_path = Path(dir_path)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
        
    supported_extensions = DocumentLoaderFactory.LOADER_MAP.keys()
    
    for file_path in dir_path.glob("**/*"):  # Recursive search
        if file_path.suffix.lower() in supported_extensions:
            logger.info(f"Processing file: {file_path}")
            test_document_loader(str(file_path))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document processing tool")
    parser.add_argument("path", help="File or directory path to process")
    parser.add_argument("--recursive", "-r", action="store_true", 
                       help="Process directory recursively")
    
    args = parser.parse_args()
    path = Path(args.path)
    
    try:
        if path.is_file():
            # Process single file
            test_document_loader(str(path))
        elif path.is_dir() and args.recursive:
            # Process directory recursively
            process_directory(str(path))
        elif path.is_dir():
            # Process files in directory (non-recursive)
            supported_extensions = DocumentLoaderFactory.LOADER_MAP.keys()
            for file_path in path.glob("*"):
                if file_path.suffix.lower() in supported_extensions:
                    test_document_loader(str(file_path))
        else:
            logger.error(f"Invalid path: {path}")
            
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}", exc_info=True)