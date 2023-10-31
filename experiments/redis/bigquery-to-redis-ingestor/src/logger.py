from utilities.classes.color import Color
import logging


old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    
    record.accent_color=Color.chartreuse
    record.file_name_color=Color.dark_violet
    record.text_color=Color.white
    record.background_color=Color.black_bg
    record.reset=Color.reset
    record.debug_color=Color.cyan
    record.info_color=Color.dodger_blue
    record.warning_color=Color.yellow
    record.error_color=Color.red
    record.critical_color=Color.orange_red
    
    return record

logging.setLogRecordFactory(record_factory)

class CustomFormatter(logging.Formatter):
    TEMPLATE = "{asctime} [{levelname}]: {message} ({filename}:{lineno})"
    STYLE = "{"
    DATEFMT = "%a %Y-%m-%d %H:%M:%S %z"
    
    FORMATS = {
        logging.DEBUG: "{accent_color}{asctime}{reset} [{debug_color}{levelname}{reset}]: {message} ({file_name_color}{filename}{reset}:{accent_color}{lineno}{reset})",
        logging.INFO:"{accent_color}{asctime}{reset} [{info_color}{levelname}{reset}]: {message} ({file_name_color}{filename}{reset}:{accent_color}{lineno}{reset})",
        logging.WARNING: "{accent_color}{asctime}{reset} [{warning_color}{levelname}{reset}]: {message} ({file_name_color}{filename}{reset}:{accent_color}{lineno}{reset})",
        logging.ERROR: "{accent_color}{asctime}{reset} [{error_color}{levelname}{reset}]: {message} ({file_name_color}{filename}{reset}:{accent_color}{lineno}{reset})",
        logging.CRITICAL: "{accent_color}{asctime}{reset} [{critical_color}{levelname}{reset}]: {message} ({file_name_color}{filename}{reset}:{accent_color}{lineno}{reset})",
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno, "{message}")
        formatter = logging.Formatter(
            fmt=log_format, 
            datefmt=CustomFormatter.DATEFMT,
            style='{', 
        )
        return formatter.format(record)


logging_level = logging.DEBUG
logging_file = ".log"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging_level)
console_handler.setFormatter(CustomFormatter())

file_handler = logging.FileHandler(filename=logging_file)
file_handler.setLevel(logging_level)
_formatter = logging.Formatter(
    CustomFormatter.TEMPLATE,
    style=CustomFormatter.STYLE,
    datefmt=CustomFormatter.DATEFMT
)
file_handler.setFormatter(_formatter)


logging.basicConfig(
    level=logging_level,
    datefmt="%a %Y-%m-%d %H:%M:%S %z",
    handlers=[
        console_handler,
        file_handler
    ]
)

logger = logging.getLogger()