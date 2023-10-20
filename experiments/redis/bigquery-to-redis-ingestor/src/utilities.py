from datetime import datetime
from dataclasses import dataclass


# Utility classes
@dataclass
class Color:
    # Define bold text and reset color and formatting
    bold: str = '\033[1m'               # bold text
    reset: str = '\033[0m'              # reset color and formatting

    # Define non-bold color codes
    blue: str = '\033[0;34m'            # Blue
    light_blue: str = '\033[0;36m'      # Light Blue
    green: str = '\033[0;32m'           # Green
    red: str = '\033[0;31m'             # Red
    yellow: str = '\033[0;33m'          # Yellow
    purple: str = '\033[0;35m'          # Purple

    # Define bold color codes
    blue_bold: str = '\033[1;34m'       # Bold Blue
    light_blue_bold: str = '\033[1;36m' # Bold Light Blue
    green_bold: str = '\033[1;32m'      # Bold Green
    red_bold: str = '\033[1;31m'        # Bold Red
    yellow_bold: str = '\033[1;33m'     # Bold Yellow
    purple_bold: str = '\033[1;35m'     # Bold Purple

class Print():
    log_keyword_color: str = Color.light_blue
    success_keyword_color: str = Color.green
    warning_keyword_color: str = Color.yellow
    error_keyword_color: str = Color.red
    
    log_keyword: str = "Log"
    success_keyword: str = "Success"
    warning_keyword: str = "Warning"
    error_keyword: str = "Error"
    
    @staticmethod
    def __message_builder(keyword: str, keyword_color: str, message: str):
        print(f"{keyword_color}{keyword}:{Color.reset} {message}")
    
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

class CodeBlock():
    declaration_message: str = "Inside CodeBlock"
    
    def __init__(self, message: str, format: str=Color.bold, pretty: bool=True, declarative: bool=False):
        self.message = message
        self.format = format
        self.pretty = pretty
        self.declarative = declarative
    
    def __enter__(self):
        if self.declarative:
            core_header = f"{self.declaration_message}: {self.message}"
        else:
            core_header = f"{self.message}"
        
        header = self.format + core_header + Color.reset
        print(header)

        if self.pretty:
            horizontal_line = self.format + ("-" * len(core_header)) + Color.reset
            print(horizontal_line)
        
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print()


# Utility lambdas
now: str = lambda: datetime.now().strftime('%H:%M:%S')


# Utility functions
def get_attributes(object: any) -> list:
    return [
        attr 
        for attr in dir(object) 
        if not callable(getattr(object, attr)) and not attr.startswith('__')
    ]

def get_regular_methods(object: any) -> list:
    return [
        method 
        for method in dir(object) 
        if callable(getattr(object, method)) and not method.startswith('__')
    ]

def get_dunder_methods(object: any) -> list:
    return [
        method 
        for method in dir(object) 
        if callable(getattr(object, method)) and method.startswith('__')
    ]    


# Driver code
if __name__ == "__main__":    
    with CodeBlock("Utility functions") as block:
        from models import Query
                
        query = Query("popular_search_terms", seeds=2, limit=1)
        print(f"{get_attributes(query) = }")       
        print(f"{get_regular_methods(query) = }") 
    
    
    with CodeBlock("Utility lambdas") as block:
        print(f"{now() = }")
    
    
    with CodeBlock("Utility classes") as block:
        Print.log("log message using Print class")
        Print.success("success message using Print class")
        Print.warning("warning message using Print class")
        Print.error("error message using Print class")