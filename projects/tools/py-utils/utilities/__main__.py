from color import Color
from print import Print
from codeblock import CodeBlock
from timerblock import TimerBlock
from miscellaneous import *
from lambdas import *


if __name__ == "__main__":
    
    with CodeBlock("Utility functions") as block:
        color = Color()
        print(f"{get_attributes(color) = }")       
        print(f"{get_regular_methods(color) = }") 
    
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

    with CodeBlock("Color Utility Class", collapse_separation=False) as _:
        Color.show_colors()