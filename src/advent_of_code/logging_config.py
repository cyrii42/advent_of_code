from loguru import logger
from pathlib import Path
from advent_of_code.constants import LOGS_DIR
import sys
import os

def setup_logging():
    logger.remove()

    logger.add(
        sink=sys.stdout, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{file}:{line}</cyan> | {message}",
        diagnose=True,
        colorize=True, 
        level='INFO',
    )
    
    logger.add(
        sink=LOGS_DIR / 'app.log',
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
        rotation="100 MB",
        retention="30 days",
        serialize=False,
        diagnose=True,
        level='DEBUG'
    )

