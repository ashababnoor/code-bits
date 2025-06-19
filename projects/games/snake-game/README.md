# Terminal Snake Game

A classic Snake game implemented in Python using the curses library for terminal-based gameplay.

## Features

- 🐍 Classic Snake gameplay
- 🎮 Multiple control schemes (Arrow keys or WASD)
- 🎨 Colorful graphics (if your terminal supports colors)
- 🏆 Score tracking
- 🔄 Restart functionality
- 📱 Responsive to terminal size

## Requirements

- Python 3.6+
- Terminal with at least 30x10 character display
- curses library (included with Python on macOS/Linux)

## How to Play

1. **Start the game:**
   ```bash
   python3 snake_game.py
   ```
   or
   ```bash
   ./snake_game.py
   ```

2. **Controls:**
   - **Move**: Arrow keys or WASD keys
   - **Quit**: Press 'Q'
   - **Restart**: Press 'R' (after game over)

3. **Objective:**
   - Control the snake to eat the food (red dots/asterisks)
   - Each food eaten increases your score by 10 points
   - Avoid hitting the walls or the snake's own body
   - The snake grows longer each time it eats food

## Game Elements

- **Snake**: Green blocks (█) or @ for head, o for body
- **Food**: Red dot (●) or asterisk (*)
- **Borders**: ASCII art borders around the play area
- **Score**: Displayed at the bottom of the screen

## Tips

- The snake moves continuously, so plan your moves ahead
- You cannot reverse direction directly (e.g., can't go left if moving right)
- Try to keep the snake in open areas as it grows longer
- Use the borders to help navigate tight spaces

## Troubleshooting

- **Terminal too small**: Resize your terminal window to at least 30 characters wide and 10 lines tall
- **No colors**: The game works fine without color support, using ASCII characters instead
- **Controls not working**: Make sure your terminal is focused and try both arrow keys and WASD

Enjoy the game! 🐍

