import unittest
from tests.interpreter.utils import interpret, should_fail
from Error import ErrorCode, ErrorDescription


class TestWhileLoop(unittest.TestCase):
    def test_simple(self):
        s = 'a = 10;' \
            'while (a > 0) {' \
            '   #print(a);\n' \
            '   a = a - 1;' \
            '}' \
            'ret a;'
        self.assertEqual(0, interpret(s).to_py())

    def test_false_condition(self):
        s = 'a = 1;' \
            'while (a > 1)' \
            '   a = a - 1;' \
            'ret a;'
        self.assertEqual(1, interpret(s).to_py())


if __name__ == '__main__':
    unittest.main()
