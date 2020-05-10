import unittest
from tests.interpreter.interpret import interpret


class TestAddition(unittest.TestCase):
    def test_simple_return(self):
        s = 'ret 1;' \
            'ret 2;'
        self.assertEqual(1.0, interpret(s).value)

    def test_simple_addition(self):
        s = 'ret 1 + 2;'
        self.assertEqual(3.0, interpret(s).value)

    def test_addition(self):
        s = 'ret 1 + 2 + 3 + 4 + 5 + 6;'
        self.assertEqual(21.0, interpret(s).value)

    def test_addition_with_parentheses(self):
        s = 'ret 1 + ((2 + 3 + 4) + 5 + 6);'
        self.assertEqual(21.0, interpret(s).value)


if __name__ == '__main__':
    unittest.main()
