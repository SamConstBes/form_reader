#config_logging.py
from pathlib import Path


LOG_PATH = Path(__file__).parent.parent / "logs" / "app.log"
Path(LOG_PATH).mkdir(exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'json': {'format': '%(asctime)s [%(levelname)s] %(message)s'},
            # 'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s %(exc_text)s', 
            # 'stack_trace_as_array': True
        'console': { 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s' },
    },
    
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH,
            'maxBytes': 50 * 1024 * 1024,  # 50 МБ на файл
            'backupCount': 5,              # Хранить 5 старых файлов
            'encoding': 'utf-8',
            'formatter': 'json',
        },
        'console': {
            'level': 'INFO',  
            'class': 'logging.StreamHandler', 
            'formatter': 'console', 
            },
    },
    
    'loggers': {
        'apscheduler.scheduler': {'level': 'ERROR', 'propagate': True},
        'apscheduler.executors.default': {'level': 'ERROR', 'propagate': True},
        
        'run': {'level': 'INFO', 'propagate': True},
        'core_bot': {'level': 'INFO', 'propagate': True},
    },
    
    'root': {
        'level': 'DEBUG',
        'handlers': ['file', 'console']
    },
}