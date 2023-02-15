import logging
import logging.config
# pip install colorlog
from colorlog import ColoredFormatter

class Logger:
    logLevel: int = logging.DEBUG
    stream: any = None

    def __init__(self, level = logging.DEBUG, config = 'Logging.conf'):
        logging.config.fileConfig(config)
        # überschreibt den root Consolen Handler mit einem Colored Formatter
        logLevel = level
        LOGFORMAT_CONSOLE = "%(log_color)s%(asctime)s-%(name)s-%(levelname)s: %(message)s%(reset)s"
        logging.root.setLevel(logLevel)
        formatter = ColoredFormatter(LOGFORMAT_CONSOLE)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        log = logging.getLogger()       # root logger
        log.setLevel(logLevel)
        log.addHandler(stream)

    def GetLogger(self, name):
        log = logging.getLogger(name)
        log.setLevel(self.logLevel)
        log.addHandler(self.stream)
        return log

    def Log(self, name, level, *args):
        log = self.GetLogger(name)
        if level == logging.DEBUG:
            log.debug(args)
        if level == logging.INFO:
            log.info(args)
        if level == logging.ERROR:
            log.error(args)
        if level == logging.FATAL:
            log.fatal(args)
        if level == logging.WARN:
            log.warn(args)
        if level == logging.CRITICAL:
            log.critical(args)
                 