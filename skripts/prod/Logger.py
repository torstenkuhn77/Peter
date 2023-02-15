import logging
import logging.config
# pip install colorlog
from colorlog import ColoredFormatter

class Logger:
    def __init__(self):
#        logging.config.fileConfig('Logging.conf')
#        print(logging.config.dictConfig())

        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        log = logging.getLogger()
        log.setLevel(LOG_LEVEL)
        log.addHandler(stream)

    def GetLogger(name):
        return logging.getLogger(name)

    def Log(level , *args):
        log = logging.getLogger()
        if log.level == level:
            if level == logging.DEBUG:
                logging.debug(args)
            if level == logging.INFO:
                logging.info(args)
            if level == logging.ERROR:
                logging.error(args)
            if level == logging.FATAL:
                logging.fatal(args)
            if level == logging.WARN:
                logging.warn(args)
            if level == logging.CRITICAL:
                logging.critical(args)
                 