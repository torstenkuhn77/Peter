import os
import traceback
import logging
from Logger import Logger

logMain = Logger().GetLogger("Main")

logMain.log(logging.INFO, "Test")
logMain.log(logging.ERROR, "Test1")
logMain.log(logging.WARNING, "Test2")

