from redis import exceptions
from redis import Redis
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
import textwrap

import random


# Quiz Configuration 
number_lower_range = 1
number_upper_range = 10
question_template = "What is {number1} {operand} {number2}?"

question_counter = 0
score_counter = 0
first_attempt_failed = False


# Define bold text and reset color and formatting
bold='\033[1m'  # bold text
reset='\033[0m' # reset color and formatting

# Define color codes (non-bold)
blue='\033[0;34m'       # Blue
light_blue='\033[0;36m' # Light Blue
green='\033[0;32m'      # Green
red='\033[0;31m'        # Red
yellow='\033[0;33m'     # Yellow
purple='\033[0;35m'     # Purple

# Define bold color codes
blue_bold='\033[1;34m'       # Bold Blue
light_blue_bold='\033[1;36m' # Bold Light Blue
green_bold='\033[1;32m'      # Bold Green
red_bold='\033[1;31m'        # Bold Red
yellow_bold='\033[1;33m'     # Bold Yellow
purple_bold='\033[1;35m'     # Bold Purple


# Custom Function
std_print = print

def custom_print(message: str) -> None:
    '''
    This function is a custom print function that overrides the standard print function.
    
    Args:
        message (str): The message to be printed
    
    Returns:
        None
    '''
    custom_print_prefix = "math-quiz >>"
    std_print(f"{blue_bold}{custom_print_prefix}{reset} {message}")

print = custom_print


def get_question() -> float:
    '''
    This function generates a question, prints the question in stdout and returns the correct answer.
    
    Args:
        None
    
    Returns:
        answer (float)
    '''
    global question_counter, first_attempt_failed
    
    question_counter += 1
    first_attempt_failed = False
    
    number1 = random.randint(number_lower_range, number_upper_range)
    number2 = random.randint(number_lower_range, number_upper_range)
    operands = ["+", "-", "*", "/"]

    operand = random.choice(operands)
    answer = round(eval(f"{number1} {operand} {number2}"), 2)
    
    print(
        question_template.format(
            number1=number1, 
            operand=operand,
            number2=number2
        )
    )
    return float(answer)


def get_answer(answer: float, history: InMemoryHistory, bindings: KeyBindings) -> bool:
    '''
    This function checks if user has given the correct answer or not; or wether the user wants to exit.
    
    Args:
        answer (float): The correct answer to the question
    
    Returns:
        keep_playing (bool): Weather player wants to keep playing or not
    '''
    global score_counter, first_attempt_failed
    
    user_wants_to_exit, user_input = take_user_input(history=history, bindings=bindings)
    keep_playing = True
    
    if user_wants_to_exit:
        keep_playing = False
        print_exit_message()
        return keep_playing
    
    if user_input == answer:
        if not first_attempt_failed:
            score_counter += 1
        
        print_correct_answer_message()
        return keep_playing
    else:
        first_attempt_failed = True
        
        print_wrong_answer_message()
        return get_answer(answer=answer, history=history, bindings=bindings)


def take_user_input(history: InMemoryHistory, bindings: KeyBindings) -> tuple[bool, float]:
    '''
    This function takes user input and checks wether user wants to exit or not
    
    Args:
        None
    
    Returns:
        tuple[bool, float]:
            bool: Users wants to keep playing or not
            float: User input if user wants to keep playing, 0 if they don't
    '''
    exit_statement = "exit"
    
    user_input = prompt(history=history, key_bindings=bindings).strip()
    if user_input == exit_statement:
        return True, 0        

    try:
        return False, float(user_input)
    except:
        print_not_a_number_message()
        return take_user_input(history=history, bindings=bindings)


def print_not_a_number_message() -> None:
    print(f"{yellow}Not a number.{reset} Try again.")

    
def print_wrong_answer_message() -> None:
    print(f"{red}Wrong Answer!{reset} Try again.")


def print_correct_answer_message() -> None:
    global question_counter, score_counter
    
    print(f"{green}Correct answer!{reset} Score: {score_counter}/{question_counter}")


def print_exit_message() -> None:
    global question_counter, score_counter
    
    print(f"You have answered {score_counter} questions correctly on your first try out of {question_counter-1}!")
    print(f"{light_blue_bold}Good bye!{reset}")
    std_print()
    
    
def print_welcome_message() -> None:
    std_print()
    std_print(f"{light_blue_bold}Welcome to Math Quiz!{reset}")
    instructions = f"""
    {bold}Instructions:{reset}
        Answer each question on your first try to get a point.
        Type "exit" at any time to end the game and exit.
    """
    std_print(textwrap.dedent(instructions))
    std_print()


def main():
    print_welcome_message()
    history = InMemoryHistory()
    bindings = KeyBindings()
    
    keep_playing = True
    while (keep_playing):
        answer = get_question()
        keep_playing = get_answer(answer=answer, history=history, bindings=bindings)


# Main driver code
if __name__ == "__main__":
    main()