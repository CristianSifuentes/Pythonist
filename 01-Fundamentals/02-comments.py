# this is a comment in Python
import unittest


print("This line of code will be executed.")

""" 
This is a multi-line comment
or docstring in Python.
It can span multiple lines.
"""

# Another single-line comment
x = 42  # This comment is inline with code
def example_function():
    # This function does nothing
    pass
class TestComments(unittest.TestCase):
    def test_example_function(self):
        self.assertIsNone(example_function())
        

# Docstring for the module
"""This module demonstrates the use of comments in Python.  
It includes single-line comments, multi-line comments,
and docstrings for functions and classes."""

if __name__ == "__main__":
    unittest.main()