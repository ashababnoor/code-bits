from utilities.classes.color import Color
import logging


old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    
    record.datetime_color=Color.chartreuse
    record.file_name_color=Color.grey
    record.file_number_color=Color.grey_bold
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
    BASE_TEMPLATE = "{asctime} [{levelname}]: {message} ({filename}:{lineno})"
    STYLE = "{"
    DATEFMT = "%a %Y-%m-%d %H:%M:%S %z"
    
    _ASCTIME = "{datetime_color}{asctime}{reset}"
    _FILEINFO = "({file_name_color}{filename}{reset}:{file_number_color}{lineno}{reset})"
    
    FORMATS = {
        logging.DEBUG:    _ASCTIME + " [{debug_color}{levelname}{reset}]: {message} "    + _FILEINFO,
        logging.INFO:     _ASCTIME + " [{info_color}{levelname}{reset}]: {message} "     + _FILEINFO,
        logging.WARNING:  _ASCTIME + " [{warning_color}{levelname}{reset}]: {message} "  + _FILEINFO,
        logging.ERROR:    _ASCTIME + " [{error_color}{levelname}{reset}]: {message} "    + _FILEINFO,
        logging.CRITICAL: _ASCTIME + " [{critical_color}{levelname}{reset}]: {message} " + _FILEINFO,
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
    CustomFormatter.BASE_TEMPLATE,
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