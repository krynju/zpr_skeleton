import unittest
import distribution
import numpy as np


class MainTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(distribution.add(1, 1), 2)

    def test_subtract(self):
        self.assertEqual(distribution.subtract(1, 1), 0)

    def test_getint_direct(self):
        self.assertEqual(distribution.getint(np.array([1, 2, 3], dtype=int)), 2)

    def test_increment_array(self):
        self.assertTrue(np.array_equal(distribution.increment_array(np.array([1, 2, 3], dtype=int)), np.array([2,3,4])))

    def test_create_tuple(self):
        self.assertEqual(distribution.create_tuple(2, 66), (2, 66))

    def test_quantiles(self):
        a = np.array([1, 2, 3, 4, 5], dtype=int)
        b = np.array([2.0, 2.6, 3.2, 3.8, 4.4], dtype=np.double)
        self.assertTrue(np.array_equal(distribution.quantiles(a, 5), b))

        a = np.array([1,2], dtype=int)
        b = np.array([2.0], dtype=np.double)
        self.assertTrue(np.array_equal(distribution.quantiles(a, 1), b))

        a = np.array([1, 2, 3], dtype=int)
        b = np.array([2.0], dtype=np.double)
        self.assertTrue(np.array_equal(distribution.quantiles(a, 1), b))

        a = np.array([1, 1, 1], dtype=int)
        b = np.array([1], dtype=np.double)
        self.assertTrue(np.array_equal(distribution.quantiles(a, 1), b))


    def test_histogram(self):
        a = np.array(["bcd", "cde", "abc", "abc", "xyee"])
        d = distribution.histogram(a)
        self.assertTrue(distribution.histogram(a) == d)



if __name__ == '__main__':
    unittest.main()
