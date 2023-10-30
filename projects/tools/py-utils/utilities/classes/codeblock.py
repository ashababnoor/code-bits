from .color import Color

class CodeBlock():
    declaration_message: str = "Inside CodeBlock"
    
    def __init__(
            self, 
            message: str="",
            format: str=Color.bold,
            declarative: bool=False,
            *, # Rest are kwargs
            pretty: bool=False,
            add_separation: bool=True,
            top_separation: int=1,
            bottom_separation: int=1
        ):
        if message is not None:
            message = str(message).strip()
            self.message = message if not message == "" else None
        else:
            self.message = message
        
        self.format = format
        self.pretty = pretty
        self.declarative = declarative
        self.add_separation = add_separation
        self.top_separation = top_separation
        self.bottom_separation = bottom_separation
    
    @staticmethod
    def check_global_last_codeblock_bottom_separation():
        global global_last_codeblock_has_bottom_separation
        global global_last_codeblock_bottom_separation_val
        if "global_last_codeblock_has_bottom_separation" not in globals() or not isinstance(global_last_codeblock_has_bottom_separation, bool):
            global_last_codeblock_has_bottom_separation = False
        if "global_last_codeblock_bottom_separation_val" not in globals() or not isinstance(global_last_codeblock_bottom_separation_val, int):
            global_last_codeblock_bottom_separation_val = 0
        return global_last_codeblock_has_bottom_separation, global_last_codeblock_bottom_separation_val
    
    def __enter__(self):
        last_codeblock_has_bottom_separation, last_codeblock_has_bottom_separation = CodeBlock.check_global_last_codeblock_bottom_separation()

        if self.add_separation and isinstance(self.top_separation, int) and self.top_separation > 0:
            effective_top_separation = self.top_separation
            if last_codeblock_has_bottom_separation:
                if self.top_separation >= last_codeblock_has_bottom_separation:
                    effective_top_separation = self.top_separation - last_codeblock_has_bottom_separation
                    
            print("\n" * (effective_top_separation), end='')
        
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
        global global_last_codeblock_has_bottom_separation
        global global_last_codeblock_bottom_separation_val
        
        if self.add_separation and isinstance(self.bottom_separation, int) and self.bottom_separation > 0:
            print("\n" * (self.bottom_separation), end='') 
            global_last_codeblock_has_bottom_separation = True
            global_last_codeblock_bottom_separation_val = self.bottom_separation
        else:
            global_last_codeblock_has_bottom_separation = False
            global_last_codeblock_bottom_separation_val = 0