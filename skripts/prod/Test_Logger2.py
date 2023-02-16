import logging
from Logger import Logger 

log = Logger()

log.Log("Sensor", logging.CRITICAL, "Hier eine kritische Meldung")
log.Log("Sensor", logging.WARNING, "Hier eine Warn Meldung")

