import unittest
from tests.interpreter.utils import interpret


class TestDoWhileLoop(unittest.TestCase):
    def test_simple(self):
        s = 'a = 10;' \
            'do {' \
            '   #print(a);\n' \
            '   a = a - 1;' \
            '} while (a > 0);' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

    def test_false_condition(self):
        s = 'a = 10;' \
            'do {' \
            '   a = a - 1;' \
            '} while (a < 0);' \
            'ret a;'
        self.assertEqual(9, interpret(s).to_py())


if __name__ == '__main__':
    unittest.main()
