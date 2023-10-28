import logging

logging_level = logging.DEBUG
logging_file = ".log"

logging.basicConfig(
    level=logging_level,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt="%a %Y-%m-%d %H:%M:%S %z",
    handlers=[
        logging.FileHandler(logging_file),  # Save log messages to a file
        logging.StreamHandler()             # Print log messages to the console
    ]
)

logger = logging.getLogger(__name__)