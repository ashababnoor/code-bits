import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .color import Color
from .print import Print
from .codeblock import CodeBlock
from functions import to_human_readable_time

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