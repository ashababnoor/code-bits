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
    chartreuse: str = '\033[38;5;76m'             # Chartreuse
    violet: str = '\033[38;5;177m'                # Violet
    dark_violet: str = '\033[38;5;92m'            # Dark Violet
    grey: str = '\033[38;5;244m'                  # Grey
    
    # Define 8-bit color bold codes
    orage_bold: str = '\033[1;38;5;214m'          # Bold Orange
    dark_orange_bold: str = '\033[1;38;5;208m'    # Bold Dark Orange
    orange_red_bold: str = '\033[1;38;5;202m'     # Bold Orange Red
    light_sea_green_bold: str = '\033[1;38;5;37m' # Bold Light Sea Green
    dodger_blue_bold: str = '\033[1;38;5;33m'     # Bold Dodger Blue
    chartreuse_bold: str = '\033[1;38;5;76m'      # Bold Chartreuse
    violet_bold: str = '\033[1;38;5;177m'         # Violet
    dark_violet_bold: str = '\033[1;38;5;92m'     # Dark Violet
    grey_bold: str = '\033[1;38;5;244m'           # Grey
    
    @staticmethod
    def show_colors():
        color_object = Color()
        colors = [
            attr 
            for attr in dir(color_object) 
            if not callable(getattr(color_object, attr)) and not attr.startswith('__')
        ]
        
        for color in colors:
            print(f"{eval(f'Color.{color}')}{color = }{color_object.reset}")