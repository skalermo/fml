import unittest
from tests.interpreter.utils import interpret


class TestDotProduct(unittest.TestCase):
    def test_simple_dot_product(self):
        s = 'ret [1, 2] * [2; 3];'
        self.assertEqual(8, interpret(s).to_py())

        s = 'a = [1, 2, 0, 0, 0];' \
            'b = [0; 3; 2; 0; 5];' \
            'ret a * b;'
        self.assertEqual(6, interpret(s).to_py())

    def test_hard_dot_product(self):
        s = 'a = [2, 3, 1, 56;' \
            '      1, 77, 4, 3;' \
            '      65, 22, 2, 6];' \
            'b = [0, 12, 4;' \
            '      73, 3, 2;' \
            '      87, 32, 1;' \
            '      2, 1, 66];' \
            'ret a * b;'
        expected = [[418, 121, 3711],
                    [5975, 374, 360],
                    [1792, 916, 702]]
        self.assertEqual(expected, interpret(s).to_py())


if __name__ == '__main__':
    unittest.main()
