"""
Calculator Tool for Agentic AI System
Handles basic arithmetic operations: addition and multiplication
"""

def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers and return the result.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Sum of the two numbers
    """
    try:
        result = float(a) + float(b)
        return result
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input for addition: {a}, {b}. Error: {e}")

def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers and return the result.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Product of the two numbers
    """
    try:
        result = float(a) * float(b)
        return result
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input for multiplication: {a}, {b}. Error: {e}")

def calculate(operation: str, a: float, b: float) -> float:
    """
    Perform calculation based on operation type.
    
    Args:
        operation (str): 'add' or 'multiply'
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Result of the calculation
        
    Raises:
        ValueError: If operation is not supported
    """
    operation = operation.lower().strip()
    
    if operation in ['add', 'addition', '+']:
        return add_numbers(a, b)
    elif operation in ['multiply', 'multiplication', '*']:
        return multiply_numbers(a, b)
    else:
        raise ValueError(f"Unsupported operation: {operation}. Supported operations: add, multiply")

if __name__ == "__main__":
    # Test the calculator functions
    print("Testing Calculator Tool:")
    print(f"Add 5 + 3 = {add_numbers(5, 3)}")
    print(f"Multiply 4 * 7 = {multiply_numbers(4, 7)}")
    print(f"Calculate add 10 + 20 = {calculate('add', 10, 20)}")
    print(f"Calculate multiply 6 * 8 = {calculate('multiply', 6, 8)}")