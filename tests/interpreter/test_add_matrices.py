import unittest
from tests.interpreter.utils import interpret


class TestAddMatrices(unittest.TestCase):
    def test_simple(self):
        s = 'a = [1, 2];' \
            'b = [2, 4];' \
            'ret a + b;'
        m = interpret(s)
        self.assertEqual((1, 2), m.shape)
        m = m.to_py()
        self.assertEqual([[3, 6]], m)

    def test_add_nested_matrices(self):
        s = 'a = [1, [1, 2], 2];' \
            'b = [10, [1, 2], 3];' \
            'ret a + b;'
        m = interpret(s)
        self.assertEqual((1, 3), m.shape)
        m = m.to_py()
        self.assertEqual([[11, [[2, 4]], 5]], m)

    def test_multirow_addition(self):
        s = 'a = [1; 2; 3; 4];' \
            'b = [4; 3; 2; 1];' \
            'ret a + b;'
        m = interpret(s)
        self.assertEqual((4, 1), m.shape)
        m = m.to_py()
        self.assertEqual([[5], [5], [5], [5]], m)


if __name__ == '__main__':
    unittest.main()
