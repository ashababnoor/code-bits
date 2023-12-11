#!/bin/sh

# Define Unicode code points for emojis
emoji_party_popper="\U0001F389"   # 🎉
emoji_confetti_ball="\U0001F38A"  # 🎊
emoji_sparkles="\U00002728"       # ✨

# Define bold text and reset color and formatting
style_bold=$(echo -e '\033[1m')  # bold text
style_reset=$(echo -e '\033[0m') # reset color and formatting

# Define 3-bit non-bold color codes
black=$(echo -e '\033[0;30m')         # Black
red=$(echo -e '\033[0;31m')           # Red
green=$(echo -e '\033[0;32m')         # Green
yellow=$(echo -e '\033[0;33m')        # Yellow
blue=$(echo -e '\033[0;34m')          # Blue
magenta=$(echo -e '\033[0;35m')       # Magenta
cyan=$(echo -e '\033[0;36m')          # Cyan
white=$(echo -e '\033[0;37m')         # White

# Define 3-bit background codes
black_bg=$(echo -e '\033[0;40m')      # Black Background
red_bg=$(echo -e '\033[0;41m')        # Red Background
green_bg=$(echo -e '\033[0;42m')      # Green Background
yellow_bg=$(echo -e '\033[0;43m')     # Yellow Background
blue_bg=$(echo -e '\033[0;44m')       # Blue Background
magenta_bg=$(echo -e '\033[0;45m')    # Magenta Background
cyan_bg=$(echo -e '\033[0;46m')       # Cyan Background
white_bg=$(echo -e '\033[0;47m')      # White Background

# Define 3-bit bold color color codes
black_bold=$(echo -e '\033[1;30m')    # Bold Black
red_bold=$(echo -e '\033[1;31m')      # Bold Red
green_bold=$(echo -e '\033[1;32m')    # Bold Green
yellow_bold=$(echo -e '\033[1;33m')   # Bold Yellow
blue_bold=$(echo -e '\033[1;34m')     # Bold Blue
magenta_bold=$(echo -e '\033[1;35m')  # Bold Magenta
cyan_bold=$(echo -e '\033[1;36m')     # Bold Cyan
white_bold=$(echo -e '\033[1;37m')    # Bold White

# Define 8-bit color non-bold codes
orage=$(echo -e '\033[38;5;214m')          # Orange
dark_orange=$(echo -e '\033[38;5;208m')    # Dark Orange
orange_red=$(echo -e '\033[38;5;202m')     # Orange Red
light_sea_green=$(echo -e '\033[38;5;37m') # Light Sea Green
dodger_blue=$(echo -e '\033[38;5;33m')     # Dodger Blue

# Define 8-bit color bold codes
orage_bold=$(echo -e '\033[1;38;5;214m')          # Bold Orange
dark_orange_bold=$(echo -e '\033[1;38;5;208m')    # Bold Dark Orange
orange_red_bold=$(echo -e '\033[1;38;5;202m')     # Bold Orange Red
light_sea_green_bold=$(echo -e '\033[1;38;5;37m') # Bold Light Sea Green
dodger_blue_bold=$(echo -e '\033[1;38;5;33m')     # Bold Dodger Blue

# Read more: 
#   1) https://en.wikipedia.org/wiki/ANSI_escape_code
#   2) https://www.ditig.com/256-colors-cheat-sheet 