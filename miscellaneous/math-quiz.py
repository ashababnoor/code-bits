import random

# Quiz Configuration 
number_lower_range = 1
number_upper_range = 10
question_template = "What is {number1} {operand} {number2}?"

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
    std_print(f"{custom_print_prefix} {message}")

print = custom_print

def get_question() -> float:
    '''
    This function generates a question, prints the question in stdout and returns the correct answer.
    
    Args:
        None
    
    Returns:
        answer (float)
    '''
    number1 = random.randint(number_lower_range, number_upper_range)
    number2 = random.randint(number_lower_range, number_upper_range)
    answer = number1 + number2
    
    print(
        question_template.format(
            number1=number1, 
            operand="+",
            number2=number2
        )
    )
    
    return float(answer)

def get_answer(answer: float) -> bool:
    '''
    This function checks if user has given the correct answer or not; or wether the user wants to exit.
    
    Args:
        answer (float): The correct answer to the question
    
    Returns:
        keep_playing (bool): Weather player wants to keep playing or not
    '''
    user_wants_to_exit, user_input = check_for_exit_statement()
    keep_playing = True
    
    if user_wants_to_exit:
        keep_playing = False
        return keep_playing
    
    if user_input == answer:
        return keep_playing
    else:
        return get_answer(answer)

def check_for_exit_statement() -> tuple[bool, float]:
    exit_statement = "exit"
    
    user_input = input()
    if user_input == exit_statement:
        return True, 0
    
    return False, float(user_input)


# Main driver code
if __name__ == "__main__":
    keep_playing = True
    while (keep_playing):
        answer = get_question()
        keep_playing = get_answer(answer)

