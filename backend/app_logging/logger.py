import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from backend.config.settings import settings

LOG_DIR = Path(settings.LOG_DIR)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Standard Log Formatter
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

def setup_logger(name: str = "cih_backend") -> logging.Logger:
    """
    Creates and configures a rotating file + console logger.
    """
    logger_inst = logging.getLogger(name)
    logger_inst.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    # Avoid duplicate handlers
    if logger_inst.hasHandlers():
        return logger_inst

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger_inst.addHandler(console_handler)

    # File Handler (Max 10MB per file, max 5 backup files)
    log_file_path = LOG_DIR / f"{name}.log"
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger_inst.addHandler(file_handler)

    return logger_inst

logger = setup_logger("cih_app")
db_logger = setup_logger("cih_database")
auth_logger = setup_logger("cih_auth")
ai_logger = setup_logger("cih_ai")

def get_logger(module_name: str) -> logging.Logger:
    return setup_logger(module_name)
