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
    FORMAT = "{asctime} [{levelname}]: {message} ({filename}:{lineno})"
    STYLE = "{"
    DATEFMT = "%a %Y-%m-%d %H:%M:%S %z"
    
    _ASCTIME = "{datetime_color}{asctime}{reset} "
    _LEVELNAME = "[{_color}{{levelname}}{{reset}}]: "
    _MESSAGE = "{message} "
    _FILEINFO = "({file_name_color}{filename}{reset}:{file_number_color}{lineno}{reset})"
    
    FORMATS = {
        logging.DEBUG:    _ASCTIME + _LEVELNAME.format(_color="{debug_color}")    + _MESSAGE + _FILEINFO,
        logging.INFO:     _ASCTIME + _LEVELNAME.format(_color="{info_color}")     + _MESSAGE + _FILEINFO,
        logging.WARNING:  _ASCTIME + _LEVELNAME.format(_color="{warning_color}")  + _MESSAGE + _FILEINFO,
        logging.ERROR:    _ASCTIME + _LEVELNAME.format(_color="{error_color}")    + _MESSAGE + _FILEINFO,
        logging.CRITICAL: _ASCTIME + _LEVELNAME.format(_color="{critical_color}") + _MESSAGE + _FILEINFO,
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno, "{message}")
        formatter = logging.Formatter(
            fmt=log_format, 
            datefmt=CustomFormatter.DATEFMT,
            style=CustomFormatter.STYLE,
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
    fmt=CustomFormatter.FORMAT,
    datefmt=CustomFormatter.DATEFMT,
    style=CustomFormatter.STYLE,
)
file_handler.setFormatter(_formatter)


logging.basicConfig(
    level=logging_level,
    handlers=[
        console_handler,
        file_handler
    ]
)

logger = logging.getLogger()