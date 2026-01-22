# Variable is a container for storing data values.
# In Python, you don't need to declare the type of variable explicitly.
# Memory space is allocated dynamically based on the value assigned.

# Temporal memory allocation example:
a = 10          # Integer variable
b = 3.14        # Float variable
c = "Hello"     # String variable
name = "Cristian" # String variable
last_name = "Sifuentes" # String variable
full_name = name + " " + last_name # Concatenation of strings
print("Full Name:", full_name) # Output: Full Name: Cristian Sifuentes  
print(a, b, c) # Output: 10 3.14 Hello
is_active = True  # Boolean variable
# Python is dynamically typed, so you can reassign variables to different types.
a = "Now I'm a string"
# Variable naming rules:
# 1. Variable names must start with a letter (a-z, A-Z) or
#    an underscore (_). They cannot start with a number.
# 2. Variable names can only contain alphanumeric characters (a-z, A-Z, 0-9) and underscores (_).
# 3. Variable names are case-sensitive (e.g., myVar and myvar are different variables).
# 4. Avoid using Python reserved keywords as variable names (e.g., if, else, while, for, etc.). 
# 5. Use meaningful names that reflect the purpose of the variable.
import unittest
from xml.etree.ElementTree import PI     

#PEP 8 recommends using lowercase letters with words separated by underscores for variable names (snake_case).
# Example: my_variable_name = 10
# Alternatively, camelCase is also used in some contexts.
# Example: myVariableName = 10
# Both styles are acceptable, but consistency within a project is important.
# Choose one style and stick to it throughout your codebase.
# Here, we will use snake_case for variable names.
# Unit tests to verify variable behavior
# Using unittest framework

# _name is a valid private variable name starting with an underscore
# name = "ValidName"
# 1invalid = 10  # Invalid: starts with a number
# invalid-var = 20  # Invalid: contains hyphen

# for = 30  # Invalid: reserved keyword

PI = 3.14159  # Constant variable (by convention, constants are in uppercase)

class TestVariables(unittest.TestCase):
    def test_variable_types(self):
        x = 5
        y = 3.5
        z = "Test"
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, float)
        self.assertIsInstance(z, str)

    def test_variable_reassignment(self):
        var = 10
        self.assertIsInstance(var, int)
        var = "Now a string"
        self.assertIsInstance(var, str)

    def test_variable_naming_rules(self):
        valid_var1 = 100
        _validVar2 = 200
        validVar3 = 300
        self.assertEqual(valid_var1, 100)
        self.assertEqual(_validVar2, 200)
        self.assertEqual(validVar3, 300)
        with self.assertRaises(SyntaxError):
            exec("1invalidVar = 10")  # Invalid: starts with a number   
        with self.assertRaises(SyntaxError):
            exec("invalid-var = 20")  # Invalid: contains hyphen    
        with self.assertRaises(SyntaxError):
            exec("for = 30")  
# Invalid: reserved keyword
if __name__ == "__main__":
    unittest.main()