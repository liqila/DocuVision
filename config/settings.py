import os
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 环境配置
ENV = os.getenv('ENV', 'development')

# API配置
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))

# OpenAI API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 视觉模型配置
VISION_MODEL_CONFIG = {
    "api_key": OPENAI_API_KEY,
    "default_model": os.getenv("VISION_MODEL", "gpt-4o-mini"),
    "models": {
        "gpt-4o-mini": {
            "name": "gpt-4o-mini",
            "max_tokens": 1000,
            "temperature": 0
        },
        "gpt-4o": {
            "name": "gpt-4o",
            "max_tokens": 1000,
            "temperature": 0
        }
    }
}

# 图像提取器配置
IMAGE_EXTRACTOR_CONFIG = {
    "DEFAULT_PROMPT_LANGUAGE": "auto",  # 自动检测语言
    "EXTRACTION_MODES": {
        "strict": {
            "extract_all_text": True,    # 提取所有文字
            "maintain_format": True,      # 保持原格式
            "include_description": False  # 不包含描述性文字
        },
        "detailed": {
            "extract_all_text": True,    # 提取所有文字
            "maintain_format": True,      # 保持原格式
            "include_description": True   # 包含描述性文字
        }
    }
}

# 日志配置
LOG_CONFIG = {
    'development': {
        'level': 'DEBUG',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'production': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'lambda': {
        'level': 'INFO',
        'format': '%(levelname)s - %(message)s'  # AWS Lambda 已包含时间戳
    }
} 