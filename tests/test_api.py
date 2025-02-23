import sys
from pathlib import Path
import requests
from loaders.factory import DocumentLoaderFactory
import logging

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

logger = logging.getLogger(__name__)

def test_document_processing():
    """Test processing of all supported documents in samples directory"""
    # API endpoint
    url = "http://localhost:8000/process"
    
    # Sample documents directory
    samples_dir = project_root / "sampledocs"  # 使用绝对路径
    if not samples_dir.exists():
        raise FileNotFoundError(f"Samples directory not found: {samples_dir}")
    
    # Get supported file extensions
    supported_extensions = DocumentLoaderFactory.LOADER_MAP.keys()
    
    # Find all supported files
    files_to_test = []
    for ext in supported_extensions:
        files_to_test.extend(samples_dir.glob(f"*{ext}"))
    
    if not files_to_test:
        print(f"No supported files found in {samples_dir}")
        return
        
    print(f"Found {len(files_to_test)} files to test:")
    for f in files_to_test:
        print(f"- {f.name}")
    print("\nStarting tests...\n")
    
    # Prepare files for request
    files = [("files", open(f, "rb")) for f in files_to_test]
    
    try:
        # Send request
        print("Sending request to API...")
        response = requests.post(url, files=files)
        
        # Check response
        assert response.status_code == 200, f"API request failed with status code: {response.status_code}"
        
        # Parse results
        results = response.json()
        
        # Print results
        for filename, docs in results.items():
            print(f"\n{'='*50}")
            print(f"Results for {filename}:")
            print(f"{'='*50}")
            
            for i, doc in enumerate(docs, 1):
                print(f"\nDocument {i}:")
                print("-" * 30)
                
                # Print content preview
                content = doc["content"]
                preview = content[:500] + "..." if len(content) > 500 else content
                print("\nContent Preview:")
                print(preview)
                
                # Print metadata
                print("\nMetadata:")
                for key, value in doc["metadata"].items():
                    print(f"{key}: {value}")
                
        logger.debug(f"API response: {results}")
                
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise
        
    finally:
        # Close all files
        print("\nCleaning up...")
        for _, f in files:
            try:
                f.close()
            except:
                pass

if __name__ == "__main__":
    test_document_processing() 