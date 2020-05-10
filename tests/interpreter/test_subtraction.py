import unittest
from tests.interpreter.interpret import interpret


class TestSubtraction(unittest.TestCase):
    def test_simple_sub(self):
        s = 'ret 1 - 1;'
        self.assertEqual(0.0, interpret(s).value)

    def test_sub(self):
        s = 'ret 1 - 2 - 34 - 42;'
        self.assertEqual(-77.0, interpret(s).value)

    def test_sub_with_parentheses(self):
        s = 'ret 1 - (2-3) - ((4 - 5) - 2);'
        self.assertEqual(5.0, interpret(s).value)


if __name__ == '__main__':
    unittest.main()
