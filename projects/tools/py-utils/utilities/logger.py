from .classes.color import Color
import logging
import sys


SUCCESS = 25
def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)

logging.addLevelName(SUCCESS, "SUCCESS")
logging.Logger.success = success
logging.SUCCESS: int = SUCCESS

CAUTION = 32
def caution(self, message, *args, **kwargs):
    if self.isEnabledFor(CAUTION):
        self._log(CAUTION, message, args, **kwargs)

logging.addLevelName(CAUTION, "CAUTION")
logging.Logger.caution = caution
logging.CAUTION: int = CAUTION


old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    
    record.datetime_color=""
    record.file_name_color=""
    record.file_number_color=""
    record.text_color=""
    record.background_color=""
    record.reset=Color.reset
    
    record.debug_color=Color.cyan
    record.info_color=Color.dodger_blue
    record.success_color=Color.green
    record.caution_color=Color.orange
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
        logging.SUCCESS:  _ASCTIME + _LEVELNAME.format(_color="{success_color}")  + _MESSAGE + _FILEINFO,
        logging.CAUTION:  _ASCTIME + _LEVELNAME.format(_color="{caution_color}")  + _MESSAGE + _FILEINFO,
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno, "{message}")
        formatter = logging.Formatter(
            fmt=log_format, 
            datefmt=CustomFormatter.DATEFMT,
            style=CustomFormatter.STYLE,
        )
        return formatter.format(record)


def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(CustomFormatter())
   return console_handler

def get_file_handler(filename):
    if filename is None:
        filename = ".log"
    file_handler = logging.FileHandler(filename=filename)
    
    _formatter = logging.Formatter(
        fmt=CustomFormatter.FORMAT,
        datefmt=CustomFormatter.DATEFMT,
        style=CustomFormatter.STYLE,
    )
    file_handler.setFormatter(_formatter)
    return file_handler

def get_logger(
        logger_name: str=None,
        log_level: int=logging.INFO,
        add_console_handler: bool=True, 
        add_file_handler: bool=True,
        filename: str=None,
    ):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    if add_console_handler:
        logger.addHandler(get_console_handler())
    if add_file_handler:
        logger.addHandler(get_file_handler(filename=filename))

    logger.propagate = False
    return logger


def main():
    logger = get_logger(
        logger_name="Logger",
        log_level=logging.DEBUG,
        add_console_handler=True,
        add_file_handler=False
    )
    logger.debug("Logger debug message")
    logger.info("Logger info message")
    logger.success("Logger success message")
    logger.warning("Logger warning message")
    logger.caution("Logger caution message")
    logger.error("Logger error message")
    logger.critical("Logger critical message")

if __name__ == "__main__":
    main()