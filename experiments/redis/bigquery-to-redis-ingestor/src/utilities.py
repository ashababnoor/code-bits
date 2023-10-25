from datetime import datetime


# Utility classes
class Color:
    # Define bold text and reset color and formatting
    bold: str = '\033[1m'  # bold text
    reset: str = '\033[0m' # reset color and formatting

    # Define 3-bit non-bold color codes
    black: str = '\033[0;30m'         # Black
    red: str = '\033[0;31m'           # Red
    green: str = '\033[0;32m'         # Green
    yellow: str = '\033[0;33m'        # Yellow
    blue: str = '\033[0;34m'          # Blue
    magenta: str = '\033[0;35m'       # Magenta
    cyan: str = '\033[0;36m'          # Cyan
    white: str = '\033[0;37m'         # White

    # Define 3-bit background codes
    black_bg: str = '\033[0;40m'      # Black Background
    red_bg: str = '\033[0;41m'        # Red Background
    green_bg: str = '\033[0;42m'      # Green Background
    yellow_bg: str = '\033[0;43m'     # Yellow Background
    blue_bg: str = '\033[0;44m'       # Blue Background
    magenta_bg: str = '\033[0;45m'    # Magenta Background
    cyan_bg: str = '\033[0;46m'       # Cyan Background
    white_bg: str = '\033[0;47m'      # White Background

    # Define 3-bit bold color color codes
    black_bold: str = '\033[1;30m'    # Bold Black
    red_bold: str = '\033[1;31m'      # Bold Red
    green_bold: str = '\033[1;32m'    # Bold Green
    yellow_bold: str = '\033[1;33m'   # Bold Yellow
    blue_bold: str = '\033[1;34m'     # Bold Blue
    magenta_bold: str = '\033[1;35m'  # Bold Magenta
    cyan_bold: str = '\033[1;36m'     # Bold Cyan
    white_bold: str = '\033[1;37m'    # Bold White

    # Define 8-bit color non-bold codes
    orage: str = '\033[38;5;214m'                 # Orange
    dark_orange: str = '\033[38;5;208m'           # Dark Orange
    orange_red: str = '\033[38;5;202m'            # Orange Red
    light_sea_green: str = '\033[38;5;37m'        # Light Sea Green
    dodger_blue: str = '\033[38;5;33m'            # Dodger Blue

    # Define 8-bit color bold codes
    orage_bold: str = '\033[1;38;5;214m'          # Bold Orange
    dark_orange_bold: str = '\033[1;38;5;208m'    # Bold Dark Orange
    orange_red_bold: str = '\033[1;38;5;202m'     # Bold Orange Red
    light_sea_green_bold: str = '\033[1;38;5;37m' # Bold Light Sea Green
    dodger_blue_bold: str = '\033[1;38;5;33m'     # Bold Dodger Blue
    
    @staticmethod
    def show_colors():
        color_object = Color()
        colors = get_attributes(color_object)
        
        for color in colors:
            print(f"{eval(f'Color.{color}')}{color = }{color_object.reset}")

class Print():
    info_keyword_color:str = Color.light_sea_green
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

class CodeBlock:
    declaration_message: str = "Inside CodeBlock"
    
    def __init__(
            self, 
            message: str="", 
            format: str=Color.bold, 
            declarative: bool=False,
            *, # Rest are kwargs 
            pretty: bool=False, 
            separation: int=1
        ):
        if message is not None:
            message = str(message).strip()
            self.message = message if not message == "" else None
        else:
            self.message = message
                                
        self.format = format
        self.pretty = pretty
        self.declarative = declarative
        self.separation = separation
    
    def __enter__(self):
        if self.message is None and not self.declarative:
            return

        if self.declarative:
            core_header = self.declaration_message
            if self.message is not None: core_header +=  f": {self.message}"
        else:
            core_header = f"{self.message}"
        
        header = self.format + core_header + Color.reset
        print(header)

        if self.pretty:
            horizontal_line = self.format + ("-" * len(core_header)) + Color.reset
            print(horizontal_line)
        
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.separation < 1:
            return
        print("\n" * (self.separation-1))

class TimerBlock(CodeBlock):
    declaration_message: str = "Inside TimerBlock"
    force_record_counter: int = 0
    
    def __init__(
            self, 
            message: str="", 
            format: str=Color.bold, 
            declarative: bool=False,
            *,
            force_record: bool=False,
            **kwargs
        ) -> None:
        super().__init__(
            message, 
            format, 
            declarative, 
            **kwargs
        )
        self.force_record = force_record

    def __add_to_global_records(self):
        if self.message is None and not self.force_record:
            return
        if self.message is None and self.force_record:
            message = f"Untitled task {TimerBlock.force_record_counter}"
            TimerBlock.force_record_counter += 1
        else:
            message = self.message
        
        global global_code_execution_records
        if "global_code_execution_records" not in globals() or not type(global_code_execution_records) == dict:
            global_code_execution_records = {}
        
        global_code_execution_records[message] = self.elapsed_time
        return
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        import time
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        
        human_readable_time = to_human_readable_time(self.elapsed_time)
        Print.keyword(keyword="Elapsed time", message=human_readable_time)
        
        self.__add_to_global_records()
        super().__exit__(exc_type, exc_value, traceback)
    
    @staticmethod
    def timing_summary(*, use_header: bool=True, use_padding: bool=True, pretty: bool=False,) -> None:
        global global_code_execution_records
        if "global_code_execution_records" not in globals() or not type(global_code_execution_records) == dict:
            Print.error("No execution timing record found!")
            return
        
        padding = 0
        if use_header:
            header = "Execution Time Reocrds"
            print(f"{Color.bold}{header}{Color.reset}")
        
        if use_padding:
            padding += len(max(global_code_execution_records))
        
        if use_header and pretty:
            horizontal_line = "-" * len(use_header)
            print(f"{Color.bold}{horizontal_line}{Color.reset}")
        
        for message, elapsed_time in global_code_execution_records.items():
            message = f"{message}"
            human_readable_time = to_human_readable_time(elapsed_time)
            print(f"{message: <{padding}} : {human_readable_time}")


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

def to_human_readable_time(seconds: int, max_depth: int=2, use_short_names=True) -> str:
    import humanize
    from datetime import timedelta
    short_names = {
        " days": "d", " day": "d",
        " hours": "h", " hour": "h",
        " minutes": "min", " minute": "min",
        " seconds": "s", " second": "s",
        " milliseconds": "ms", " millisecond": "ms",
        " microseconds": "μs", " microsecond": "μs"
    }

    delta = timedelta(seconds=seconds)
    human_readable_time = humanize.precisedelta(delta, minimum_unit="microseconds")
    human_readable_time = human_readable_time.replace(" and ", ", ")
    
    if len(human_readable_time.split(", ")) > max_depth:
        units = human_readable_time.split(", ")
        units = units[:max_depth]
        human_readable_time = ", ".join(units)
    
    if use_short_names:
        for name, short_name in short_names.items(): human_readable_time = human_readable_time.replace(name, short_name)
    return human_readable_time



# Driver code
if __name__ == "__main__":    
    with CodeBlock("Utility functions") as block:
        from models import Query
        
        query = Query("popular_search_terms", grain=2, limit=1)
        print(f"{get_attributes(query) = }")       
        print(f"{get_regular_methods(query) = }") 
    
    with CodeBlock("Utility lambdas") as block:
        print(f"{now() = }")
    
    with CodeBlock("Utility classes") as block:
        Print.info("Info message using Print class")
        Print.log("log message using Print class")
        Print.success("success message using Print class")
        Print.warning("warning message using Print class")
        Print.error("error message using Print class")
        Print.keyword("Custom keyword", "Keyword message using Print class")
    
    with TimerBlock(force_record=True) as block:
        start = 1
        finish = 1_000
        print(f"Generating list from {start:,} to {finish:,}")
        list_ = [i for i in range(start, finish+1)]
    
    with TimerBlock(force_record=True) as block:
        start = 1
        finish = 1_000
        print(f"Generating list from {start:,} to {finish:,}")
        list_ = [i for i in range(start, finish+1)]
    
    TimerBlock.timing_summary()
    print()

    with CodeBlock("Color Utility Class") as _:
        Color.show_colors()