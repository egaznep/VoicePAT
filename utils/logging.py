import logging
import utils.logging
# Define a new logging level between INFO and WARNING
NOTICE = logging.INFO + 5
logging.addLevelName(NOTICE, "NOTICE")