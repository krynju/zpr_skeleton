import unittest
import distribution
import numpy as np


class MainTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(distribution.add(1, 1), 2)

    def test_subtract(self):
        self.assertEqual(distribution.subtract(1, 1), 0)

    def test_getint(self):
        a = np.array([1, 2, 3], dtype=int)
        self.assertEqual(distribution.getint(a), 2)
        self.assertEqual(a[0], 7)

    def test_getint_direct(self):
        self.assertEqual(distribution.getint(np.array([1, 2, 3], dtype=int)), 2)

    def test_increment_array(self):
        self.assertTrue(np.array_equal(distribution.increment_array(np.array([1, 2, 3], dtype=int)), np.array([2,3,4])))

    def test_create_tuple(self):
        self.assertEqual(distribution.create_tuple(2, 69), (2,69))

    def test_generateQQ(self):
        a = np.array([4,3,5], dtype=np.double)
        b = np.array([2,3,1], dtype=np.double)
        (x, y) = distribution.generateQQ(a, b, 3)
        self.assertTrue(np.array_equal(x, np.array([3, 4, 5])))
        self.assertTrue(np.array_equal(y, np.array([1, 2, 3])))

    def test_quantiles(self):
        a = np.array([1, 2, 3, 4, 5], dtype=np.double)
        b = np.array([2.0, 2.6, 3.2, 3.8, 4.4], dtype=np.double)
        self.assertTrue(np.array_equal(distribution.quantiles(a, 5), b))

    def test_histogram(self):
        a = np.array(["bcd", "cde", "abc", "abc", "xyee"])
        d = distribution.histogram(a)
        self.assertTrue(distribution.histogram(a) == d)



if __name__ == '__main__':
    unittest.main()
