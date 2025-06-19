#!/usr/bin/env python3
"""
Terminal Snake Game
A classic Snake game implemented using Python's curses library.

Controls:
- Arrow keys or WASD to move
- Q to quit
- R to restart after game over
"""

import curses
import random
import time
from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Game boundaries (leave space for borders and score)
        self.game_height = self.height - 4
        self.game_width = self.width - 2
        
        # Initialize game state
        self.reset_game()
        
        # Configure curses
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True)  # Non-blocking input
        stdscr.timeout(100)  # Refresh rate (milliseconds)
        
        # Initialize colors if supported
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
            curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)    # Game Over
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Snake starts in the middle
        start_y = self.game_height // 2
        start_x = self.game_width // 2
        
        self.snake = [(start_y, start_x), (start_y, start_x - 1), (start_y, start_x - 2)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # Place first food
        self.place_food()
    
    def place_food(self):
        """Place food at a random location not occupied by snake"""
        while True:
            food_y = random.randint(1, self.game_height - 1)
            food_x = random.randint(1, self.game_width - 1)
            if (food_y, food_x) not in self.snake:
                self.food = (food_y, food_x)
                break
    
    def draw_border(self):
        """Draw game border"""
        # Top border
        self.stdscr.addstr(0, 0, "+" + "-" * self.game_width + "+")
        
        # Side borders
        for y in range(1, self.game_height + 1):
            self.stdscr.addstr(y, 0, "|")
            self.stdscr.addstr(y, self.game_width + 1, "|")
        
        # Bottom border
        self.stdscr.addstr(self.game_height + 1, 0, "+" + "-" * self.game_width + "+")
    
    def draw_snake(self):
        """Draw the snake"""
        for i, (y, x) in enumerate(self.snake):
            if curses.has_colors():
                self.stdscr.addstr(y + 1, x + 1, "█", curses.color_pair(1))
            else:
                char = "@" if i == 0 else "o"  # Head is @, body is o
                self.stdscr.addstr(y + 1, x + 1, char)
    
    def draw_food(self):
        """Draw the food"""
        y, x = self.food
        if curses.has_colors():
            self.stdscr.addstr(y + 1, x + 1, "●", curses.color_pair(2))
        else:
            self.stdscr.addstr(y + 1, x + 1, "*")
    
    def draw_score(self):
        """Draw the score and instructions"""
        score_text = f"Score: {self.score}"
        if curses.has_colors():
            self.stdscr.addstr(self.game_height + 2, 0, score_text, curses.color_pair(3))
        else:
            self.stdscr.addstr(self.game_height + 2, 0, score_text)
        
        # Instructions
        instructions = "Arrow keys/WASD: Move | Q: Quit | R: Restart"
        self.stdscr.addstr(self.game_height + 3, 0, instructions[:self.width-1])
    
    def draw_game_over(self):
        """Draw game over screen"""
        messages = [
            "GAME OVER!",
            f"Final Score: {self.score}",
            "Press R to restart or Q to quit"
        ]
        
        start_y = self.game_height // 2 - 1
        for i, message in enumerate(messages):
            x = (self.width - len(message)) // 2
            if curses.has_colors():
                self.stdscr.addstr(start_y + i, x, message, curses.color_pair(4))
            else:
                self.stdscr.addstr(start_y + i, x, message)
    
    def handle_input(self):
        """Handle user input"""
        try:
            key = self.stdscr.getch()
        except Exception:
            return True
        
        if key == -1:  # No input
            return True
        
        # Convert key to lowercase for case-insensitive input
        if 0 <= key <= 255:
            key_char = chr(key).lower()
        else:
            key_char = None
        
        # Quit game
        if key_char == 'q':
            return False
        
        # Restart game
        if key_char == 'r':
            self.reset_game()
            return True
        
        # Don't change direction if game is over
        if self.game_over:
            return True
        
        # Movement controls
        new_direction = None
        
        # Arrow keys
        if key == curses.KEY_UP:
            new_direction = Direction.UP
        elif key == curses.KEY_DOWN:
            new_direction = Direction.DOWN
        elif key == curses.KEY_LEFT:
            new_direction = Direction.LEFT
        elif key == curses.KEY_RIGHT:
            new_direction = Direction.RIGHT
        # WASD keys
        elif key_char == 'w':
            new_direction = Direction.UP
        elif key_char == 's':
            new_direction = Direction.DOWN
        elif key_char == 'a':
            new_direction = Direction.LEFT
        elif key_char == 'd':
            new_direction = Direction.RIGHT
        
        # Prevent snake from going backwards into itself
        if new_direction and self.is_valid_direction_change(new_direction):
            self.direction = new_direction
        
        return True
    
    def is_valid_direction_change(self, new_direction: Direction) -> bool:
        """Check if direction change is valid (not backwards)"""
        current_dy, current_dx = self.direction.value
        new_dy, new_dx = new_direction.value
        
        # Can't go in opposite direction
        return not (current_dy == -new_dy and current_dx == -new_dx)
    
    def update_game(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Get current head position
        head_y, head_x = self.snake[0]
        
        # Calculate new head position
        dy, dx = self.direction.value
        new_head = (head_y + dy, head_x + dx)
        new_y, new_x = new_head
        
        # Check wall collision
        if (new_y < 0 or new_y >= self.game_height or 
            new_x < 0 or new_x >= self.game_width):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 10
            self.place_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw(self):
        """Draw the entire game"""
        self.stdscr.clear()
        
        self.draw_border()
        self.draw_snake()
        self.draw_food()
        self.draw_score()
        
        if self.game_over:
            self.draw_game_over()
        
        self.stdscr.refresh()
    
    def run(self):
        """Main game loop"""
        while True:
            # Handle input
            if not self.handle_input():
                break
            
            # Update game state
            self.update_game()
            
            # Draw everything
            self.draw()
            
            # Small delay to control game speed
            time.sleep(0.05)

def main():
    """Main function to start the game"""
    def game_wrapper(stdscr):
        # Check terminal size
        height, width = stdscr.getmaxyx()
        if height < 10 or width < 30:
            stdscr.addstr(0, 0, "Terminal too small! Need at least 30x10")
            stdscr.addstr(1, 0, "Press any key to exit...")
            stdscr.getch()
            return
        
        # Start the game
        game = SnakeGame(stdscr)
        game.run()
    
    try:
        curses.wrapper(game_wrapper)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Thanks for playing Snake!")


if __name__ == "__main__":
    main()
