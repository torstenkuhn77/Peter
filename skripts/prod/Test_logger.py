import traceback
import logging
import logging.config
# pip install colorlog
from colorlog import ColoredFormatter

# from Logger import Logger

# logScreen = Logger().GetLogger("Screen")

SoLo_Text = "SolarLog "
PVmin = 100

# logScreen.log(logging.INFO, SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)

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

logging.debug(SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)
logging.info(SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)
logging.error(SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)
logging.fatal(SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)
logging.warn(SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)
logging.critical(SoLo_Text,'Tagbetrieb erst ab PVmin', PVmin)

log = logging.getLogger("Relais")   # named logger Relais
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

log.debug("Sensor")
log.info("misst")
log.error("gerade")
log.fatal("die")
log.warn("Temperatur")
log.critical("und die Luftfeuchte")
