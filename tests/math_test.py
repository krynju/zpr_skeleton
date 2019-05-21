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

    def test_increment_array(self):
        self.assertTrue(np.array_equal(python_cpp_example.increment_array(np.array([1, 2, 3], dtype=int)), np.array([2,3,4])))

    def test_create_tuple(self):
        self.assertEqual(python_cpp_example.create_tuple(2, 69), (2,69))

    def test_generateQQ(self):
        a = np.array([4,3,5], dtype=np.double)
        b = np.array([2,3,1], dtype=np.double)
        (x, y) = python_cpp_example.generateQQ(a, b, 3)
        self.assertTrue(np.array_equal(x, np.array([3, 4, 5])))
        self.assertTrue(np.array_equal(y, np.array([1, 2, 3])))


if __name__ == '__main__':
    unittest.main()
