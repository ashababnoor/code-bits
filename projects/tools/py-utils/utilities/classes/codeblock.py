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
    
    def __enter__(self):
        if self.add_separation and isinstance(self.top_separation, int) and self.top_separation > 0:
            print("\n" * (self.top_separation), end='')
        
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
        if self.add_separation and isinstance(self.bottom_separation, int) and self.bottom_separation > 0:
            print("\n" * (self.bottom_separation), end='')
        else:
            return