import unittest

from prime import is_prime

class Tests(unittest.TestCase):

    def test_1(self):
        self.assertFalse(is_prime(1))

    def test_11(self):
        self.assertTrue(is_prime(11))

    def test_25(self):
        self.assertFalse(is_prime(25))


if __name__ == '__main__':
    unittest.main()