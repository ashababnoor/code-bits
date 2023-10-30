from utilities.classes.color import Color
import logging


class CustomFormatter(logging.Formatter):
    TEMPLATE = "{asctime} [{level_color}{levelname}{reset}]: {message} ({filename}:{lineno})"
    
    FORMATS = {
        logging.DEBUG: "{asctime} [" + Color.cyan + "{levelname}" + Color.reset + "]: {message} ({filename}:{lineno})"
        # logging.DEBUG: TEMPLATE.format(levelname="DEBUG", level_color=Color.cyan, reset=Color.reset),
        # logging.INFO: TEMPLATE.format(levelname="INFO", level_color=Color.light_sea_green, reset=Color.reset),
        # logging.WARNING: TEMPLATE.format(levelname="WARNING", level_color=Color.yellow, reset=Color.reset),
        # logging.ERROR: TEMPLATE.format(levelname="ERROR", level_color=Color.red, reset=Color.reset),
        # logging.CRITICAL: TEMPLATE.format(levelname="CRITICAL", level_color=Color.dark_orange, reset=Color.reset),
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno, "{message}")
        formatter = logging.Formatter(log_format, style='{')
        return formatter.format(record)


# Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging_level = logging.DEBUG
logging_file = ".log"

logging.basicConfig(
    format='{asctime} [{levelname}]: {message} ({filename}:{lineno})',
    style="{",
    datefmt="%a %Y-%m-%d %H:%M:%S %z",
    handlers=[
        logging.FileHandler(logging_file),  # Save log messages to a file
        logging.StreamHandler()             # Print log messages to the console
    ]
)

logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(CustomFormatter())

file_handler = logging.FileHandler(filename=logging_file)

logger.addHandler(console_handler)
logger.addHandler(file_handler)