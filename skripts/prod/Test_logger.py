import traceback
import logging
import logging.config
# pip install colorlog
from colorlog import ColoredFormatter

try:
    logging.config.fileConfig('Logging.conf')
except:
    print(traceback.format_exc())

# überschreibt den Consolen Handler mit einem Colored Formatter
LOG_LEVEL = logging.DEBUG
LOGFORMAT_CONSOLE = "%(log_color)s%(asctime)s-%(name)s-%(levelname)s: %(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT_CONSOLE)
stream = logging.StreamHandler()
stream.setFormatter(formatter)
log = logging.getLogger()       # root logger
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

logging.debug("Hallo")
logging.info("Torsten")
logging.error("dies")
logging.fatal("ist")
logging.warn("ein")
logging.critical("Test")

log = logging.getLogger("Sensor")   # named logger Sensor
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

log.debug("Sensor")
log.info("misst")
log.error("gerade")
log.fatal("die")
log.warn("Temperatur")
log.critical("und die Luftfeuchte")
