import unittest
from tests.interpreter.utils import interpret


class TestAssignment(unittest.TestCase):
    def test_simple_assignment(self):
        s = 'a = 1;' \
            'b = 2;' \
            'c = a + b;' \
            'ret c;'
        self.assertEqual(3.0, interpret(s).value)


if __name__ == '__main__':
    unittest.main()
