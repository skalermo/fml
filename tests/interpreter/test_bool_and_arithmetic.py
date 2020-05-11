import unittest
from Objects.Scalar import Scalar


class TestBoolAndArithmetic(unittest.TestCase):
    def test_scalar_to_bool(self):
        false_scalar = Scalar(0)
        self.assertFalse(false_scalar)


if __name__ == '__main__':
    unittest.main()
