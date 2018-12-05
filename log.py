# coding : utf-8
import logging
import time
from logging.handlers import TimedRotatingFileHandler

def setup_custom_logger(log_path,name):

    formatter = logging.Formatter(fmt='%(asctime)s:%(levelname)s:%(message)s')
    formatter.converter = time.gmtime
    handler = TimedRotatingFileHandler(log_path, utc=True,
                                       when='midnight')
    handler.suffix = '%Y%m%d.log'
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
