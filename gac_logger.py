import  logging
import  logging.handlers
from gac_config import config

def init_logger():
    '''
    初始化日志
    :return: logger
    '''

    #获取日志配置
    level = logging.getLevelName(config.get('log', 'level'))
    filename = config.get('log', 'filename')
    fileMaxSize = int(config.get('log', 'fileMaxSize'))
    fmt = config.get('log', 'fmt')
    fileCount = int(config.get('log', 'fileCount'))

    log = logging.getLogger()
    log.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt))
    log.addHandler(console_handler)
    file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxSize, backupCount=fileCount, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt))
    log.addHandler(file_handler)
    return log

logger = init_logger()

