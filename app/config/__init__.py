from .config_app import app_config
from .config_logging import LOGGING_CONFIG
from .config_ui import *

import logging
import logging.config

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING_CONFIG)