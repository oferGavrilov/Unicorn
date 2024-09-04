import os
import logging
from datetime import datetime

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def configure_failed_logger(platform_name):
    os.makedirs('logs', exist_ok=True)
    current_date = datetime.now().strftime('%d%m%y')
    log_file_name = f'logs/failed-{platform_name}-{current_date}.log'

    failed_logger = logging.getLogger('failed_jobs')
    failed_logger.setLevel(logging.WARNING)

    if failed_logger.hasHandlers():
        failed_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_name, mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M'))
    failed_logger.addHandler(file_handler)

    return failed_logger
