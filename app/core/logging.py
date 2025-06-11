import logging
import sys
from pathlib import Path
from typing import Optional

from app.core.config import settings


def setup_logging(
    log_file: Optional[str] = None,
    log_level: Optional[str] = None
) -> logging.Logger:
    """Configure logging for the application.
    
    Args:
        log_file (Optional[str]): Path to log file. If None, logs to stdout.
        log_level (Optional[str]): Logging level. If None, uses 
            settings.LOG_LEVEL.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Get logger
    logger = logging.getLogger("library_api")
    logger.setLevel(log_level or settings.LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is provided
    if log_file:
        try:
            # Create log directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to setup file logging: {str(e)}")
    
    return logger


# Create default logger
logger = setup_logging()


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name) 