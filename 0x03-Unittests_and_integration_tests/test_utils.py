import unittest
from parameterized import parameterized

# Assuming the existence of a utils module with access_nested_map.
# For demonstration, a simple implementation of access_nested_map is provided here.
# In a real scenario, you would import this function from your utils module.
def access_nested_map(nested_map, path):
    """
    Accesses a value in a nested dictionary using a list/tuple of keys as a path.
    """
    current_value = nested_map
    for key in path:
        if not isinstance(current_value, dict) or key not in current_value:
            raise KeyError(f"Key '{key}' not found in nested map or path is invalid.")
        current_value = current_value[key]
    return current_value

class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Tests that access_nested_map returns the expected result for various inputs.
        The test method body should not be longer than 2 lines as per the task.
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

# This allows running the tests directly from the script
if __name__ == '__main__':
    unittest.main()


