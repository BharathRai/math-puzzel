import random

def generate_puzzle(difficulty):
    """Generates a math puzzle based on difficulty level."""
    if difficulty == "Easy":
        # Simple addition/subtraction, numbers 1-10
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(['+', '-'])
    elif difficulty == "Medium":
        # Addition/subtraction up to 50, simple multiplication
        num1 = random.randint(10, 50)
        num2 = random.randint(1, 20)
        operator = random.choice(['+', '-', '*'])
    else: # Hard
        # Larger numbers, includes division
        num1 = random.randint(20, 100)
        num2 = random.randint(5, 20)
        operator = random.choice(['+', '-', '*', '/'])
        # Ensure division results in integer
        if operator == '/':
            num1 = num1 - (num1 % num2) 

    # Calculate answer
    if operator == '+': answer = num1 + num2
    elif operator == '-': answer = num1 - num2
    elif operator == '*': answer = num1 * num2
    elif operator == '/': answer = num1 // num2

    problem_str = f"{num1} {operator} {num2}"
    return problem_str, answer