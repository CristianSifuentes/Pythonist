import math
import sys

def factorial_fast(n: int) -> int:
    """Thin wrapper around math.factorial with input validation."""
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Factorial is undefined for negative integers.")
    return math.factorial(n)

if __name__ == "__main__":
    try:
        n = int(input("Enter a non-negative integer: "))
        print(f"{n}! = {factorial_fast(n):,}") 
    except (ValueError, TypeError) as e:
        print("Error:", e, file=sys.stderr)
