import logging
import os
from pathlib import Path
from config.settings import PROJECT_ROOT, ENV, LOG_CONFIG

def setup_logging():
    """
    Setup logging configuration based on environment
    
    - Local: Console + File logging
    - Lambda: Console logging (CloudWatch)
    - GCP: Console logging (Cloud Logging)
    - Azure: Console logging (Application Insights)
    """
    config = LOG_CONFIG[ENV]
    
    # 基础配置
    logging.basicConfig(
        level=config['level'],
        format=config['format'],
        handlers=[logging.StreamHandler()]
    )

    # 云环境特定配置
    if ENV == 'lambda':
        # AWS Lambda automatically logs to CloudWatch
        pass
    elif ENV == 'gcp':
        # Import google-cloud-logging if needed
        try:
            import google.cloud.logging
            client = google.cloud.logging.Client()
            client.setup_logging()
        except ImportError:
            pass
    elif ENV == 'azure':
        # Import azure-logging if needed
        try:
            from opencensus.ext.azure.log_exporter import AzureLogHandler
            logging.getLogger().addHandler(
                AzureLogHandler(connection_string=os.getenv("AZURE_MONITOR_CONNECTION_STRING"))
            )
        except ImportError:
            pass

    # 设置第三方库的日志级别
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING) 