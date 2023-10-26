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