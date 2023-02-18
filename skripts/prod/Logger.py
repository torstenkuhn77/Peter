import logging
import logging.config
# pip install colorlog
from colorlog import ColoredFormatter

class Logger:

    def __init__(self, level = logging.DEBUG, config = 'Logging.conf'):
        self.logLevel = logging.DEBUG       
        logging.config.fileConfig(config)
        # überschreibt den root Consolen Handler mit einem Colored Formatter
        logLevel = level
        LOGFORMAT_CONSOLE = "%(log_color)s%(asctime)s-%(name)s-%(levelname)s: %(message)s%(reset)s"
        logging.root.setLevel(logLevel)
        formatter = ColoredFormatter(LOGFORMAT_CONSOLE)
        self.stream = logging.StreamHandler()
        self.stream.setFormatter(formatter)
        log = logging.getLogger()               # returns root logger
        log.setLevel(logLevel)
        log.addHandler(self.stream)

    def GetLogger(self, name):
        log = logging.getLogger(name)
        log.setLevel(self.logLevel)
        log.addHandler(self.stream)
        return log

    def Log(self, level, msg, *args):
        logging.log(level, msg, args)

    def Log(self, name, level, msg, *args):
        log = self.GetLogger(name)
        if level == logging.DEBUG:
            log.debug(msg, args)
        if level == logging.INFO:
            log.info(msg, args)
        if level == logging.ERROR:
            log.error(msg, args)
        if level == logging.FATAL:
            log.fatal(msg, args)
        if level == logging.WARN:
            log.warn(msg, args)
        if level == logging.CRITICAL:
            log.critical(msg, args)
                 