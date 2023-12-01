from color import Color


class Print():
    info_keyword_color:str = Color.dodger_blue
    log_keyword_color: str = Color.cyan
    success_keyword_color: str = Color.green
    warning_keyword_color: str = Color.yellow
    error_keyword_color: str = Color.red
    
    info_keyword: str = "Info"
    log_keyword: str = "Log"
    success_keyword: str = "Success"
    warning_keyword: str = "Warning"
    error_keyword: str = "Error"
    
    @staticmethod
    def __message_builder(keyword: str, keyword_color: str, message: str):
        print(f"{keyword_color}{keyword}:{Color.reset} {message}")
    
    @staticmethod
    def info(message: str):
        Print.__message_builder(Print.info_keyword, Print.info_keyword_color, message)
    
    @staticmethod
    def log(message: str):
        Print.__message_builder(Print.log_keyword, Print.log_keyword_color, message)
    
    @staticmethod
    def success(message: str):
        Print.__message_builder(Print.success_keyword, Print.success_keyword_color, message)
    
    @staticmethod
    def warning(message: str):
        Print.__message_builder(Print.warning_keyword, Print.warning_keyword_color, message)
    
    @staticmethod
    def error(message: str):
        Print.__message_builder(Print.error_keyword, Print.error_keyword_color, message)
    
    @staticmethod
    def keyword(keyword: str, message: str, keyword_color: str = log_keyword_color):
        Print.__message_builder(keyword, keyword_color, message)
    
    @staticmethod
    def bold(message: str):
        print(Color.bold + message + Color.reset)