# data types in Python
# Python has several built-in data types, including:
# 1. Numeric Types: int, float, complex
# 2. Sequence Types: list, tuple, range
# 3. Text Type: str
# 4. Mapping Type: dict
# 5. Set Types: set, frozenset
# 6. Boolean Type: bool
import unittest

class TestDataTypes(unittest.TestCase):
    def test_numeric_types(self):
        self.assertIsInstance(10, int)
        self.assertIsInstance(10.5, float)
        self.assertIsInstance(3 + 4j, complex)

    def test_sequence_types(self):
        self.assertIsInstance([1, 2, 3], list)
        self.assertIsInstance((1, 2, 3), tuple)
        self.assertIsInstance(range(5), range)

    def test_text_type(self):
        self.assertIsInstance("Hello, World!", str)

    def test_mapping_type(self):
        self.assertIsInstance({"key": "value"}, dict)
        self.assertIsInstance(dict(a=1, b=2), dict)
        self.assertEqual({"a": 1, "b": 2}["a"], 1)
        self.assertEqual(dict(a=1, b=2)["b"], 2)
        self.assertIn("key", {"key": "value"})

    def test_set_types(self):
        self.assertIsInstance({1, 2, 3}, set)
        self.assertIsInstance(frozenset([1, 2, 3]), frozenset)
        self.assertIn(2, {1, 2, 3})
        self.assertNotIn(4, {1, 2, 3})
        self.assertEqual(len({1, 2, 2, 3}), 3)  # Sets have unique elements
        self.assertEqual(len(frozenset([1, 2, 2, 3])), 3)
        self.assertTrue({1, 2}.issubset({1, 2, 3}))
        self.assertTrue({1, 2, 3}.issuperset({2, 3}))

    def test_boolean_type(self):
        self.assertIsInstance(True, bool)
        self.assertIsInstance(False, bool)
    
    def test_type_conversion(self):
        self.assertEqual(int(10.5), 10)
        self.assertEqual(float(10), 10.0)
        self.assertEqual(str(100), "100")
        self.assertEqual(list((1, 2, 3)), [1, 2, 3])
        self.assertEqual(tuple([1, 2, 3]), (1, 2, 3))
        self.assertEqual(set([1, 2, 2, 3]), {1, 2, 3})
    
    def test_type_checking(self):
        value = 42
        self.assertTrue(isinstance(value, int))
        self.assertFalse(isinstance(value, str))
        with self.assertRaises(SyntaxError):
            exec("for = 10")  # Invalid: reserved keyword
    
    def test_immutable_mutable(self):
        immutable_tuple = (1, 2, 3)
        mutable_list = [1, 2, 3]
        with self.assertRaises(TypeError):
            immutable_tuple[0] = 10  # Tuples are immutable
        mutable_list[0] = 10  # Lists are mutable
        self.assertEqual(mutable_list, [10, 2, 3])
        
if __name__ == "__main__":
    unittest.main()