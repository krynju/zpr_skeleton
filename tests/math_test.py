import unittest
import python_cpp_example
import numpy as np


class MainTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(python_cpp_example.add(1, 1), 2)

    def test_subtract(self):
        self.assertEqual(python_cpp_example.subtract(1, 1), 0)

    def test_getint(self):
        self.assertEqual(python_cpp_example.getint(np.array([1, 2, 3], dtype=int)), 2)

    def test_getint_direct(self):
        self.assertEqual(python_cpp_example.getint(np.array([1, 2, 3], dtype=int)), 2)


if __name__ == '__main__':
    unittest.main()
