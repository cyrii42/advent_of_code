from loguru import logger
import sys

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
        sink="app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
        rotation="100 MB",
        retention="30 days",
        serialize=False,
        diagnose=True,
        level='INFO'
    )

