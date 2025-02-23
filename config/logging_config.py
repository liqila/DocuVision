import logging
import os
from pathlib import Path
from config.settings import PROJECT_ROOT, ENV, LOG_CONFIG

def setup_logging():
    """
    Setup logging configuration based on environment
    
    - Local: Console + File logging
    - Lambda: Console logging (automatically goes to CloudWatch)
    - Production: Console logging (can be captured by container logs)
    """
    config = LOG_CONFIG[ENV]
    
    logging.basicConfig(
        level=config['level'],
        format=config['format'],
        handlers=[
            logging.StreamHandler()
        ]
    )

    # 设置第三方库的日志级别
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING) 