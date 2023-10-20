from datetime import datetime


# Utility classes
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
    
    @staticmethod
    def bold(message: str):
        print(Color.bold + message + Color.reset)

class CodeBlock():
    declaration_message: str = "Inside CodeBlock"
    
    def __init__(
            self, 
            message: str="", 
            format: str=Color.bold, 
            declarative: bool=False,
            *, # Rest are kwargs 
            pretty: bool=True, 
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
        print(f"{Color.light_blue}Elapsed time:{Color.reset} {human_readable_time}")
        
        self.__add_to_global_records()
        super().__exit__(exc_type, exc_value, traceback)
    
    @staticmethod
    def timing_summary(*, declarative: bool=True, use_padding: bool=True, pretty: bool=False,) -> None:
        global global_code_execution_records
        if "global_code_execution_records" not in globals() or not type(global_code_execution_records) == dict:
            Print.error("No execution timing record found!")
            return
        
        padding = 0
        if declarative:
            header = "Execution Time Reocrds"
            print(f"{Color.bold}{header}{Color.reset}")
        
        if use_padding:
            padding += len(max(global_code_execution_records))
        
        if declarative and pretty:
            horizontal_line = "-" * len(declarative)
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
    
def to_human_readable_time(seconds: int, use_short_names=True) -> str:
    import humanize
    from datetime import timedelta
    short_names = {" minutes": "min", " seconds": "s", " milli": "m", " micro": "μ", "seconds": "s"}

    delta = timedelta(seconds=seconds)
    human_readable_time = humanize.precisedelta(delta, minimum_unit="microseconds")
    if use_short_names:
        for name, short_name in short_names.items(): human_readable_time = human_readable_time.replace(name, short_name)
    return human_readable_time

        
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