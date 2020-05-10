import unittest
from tests.interpreter.interpret import interpret


class TestAddMatrices(unittest.TestCase):
    def test_simple(self):
        s = 'a = [1, 2];' \
            'b = [2, 4];' \
            'ret a + b;'
        m = interpret(s)
        self.assertEqual((1, 2), m.shape)
        self.assertEqual(3.0, m[0][0].value)
        self.assertEqual(6.0, m[0][1].value)


if __name__ == '__main__':
    unittest.main()
