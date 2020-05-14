import unittest
from tests.interpreter.interpret import interpret


class TestMtrxSubs(unittest.TestCase):
    def test_single_idx(self):
        s = 'a = [1, 2, 3];' \
            'ret a[2];'
        self.assertEqual(3, interpret(s).to_py())

        s = 'a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];' \
            'ret a[7];'
        self.assertEqual(8, interpret(s).to_py())

    def test_single_idx_multiple_rows(self):
        s = 'a = [2, 4, 5;' \
            '     4, 7, 2;' \
            '     1, 72, 2];' \
            'ret a[7];'
        self.assertEqual(72, interpret(s).to_py())

        s = 'a = [2, 4, 5, 2, 5, 7, 23;' \
            '     4, 7, 2, 2, 11, 34, 3;' \
            '     1, 72, 2, 7, 1, 0, 1];' \
            'ret a[12];'
        self.assertEqual(34, interpret(s).to_py())

    def test_double_idx(self):
        s = 'a = [1, 2, 3;' \
            '     3, 4, 5];' \
            'ret a[0, 2];'
        self.assertEqual(3, interpret(s).to_py())

        s = 'a = [1, 2, 3;' \
            '     3, 4, 5];' \
            'ret a[1, 1];'
        self.assertEqual(4, interpret(s).to_py())

    def test_row_colon_index(self):
        s = 'a = [1, 2, 3;' \
            '     4, 5, 6;' \
            '     7, 8, 9];' \
            'ret a[:, 0];'
        self.assertEqual([[1, 4, 7]], interpret(s).to_py())

        s = 'a = [1, 2, 3;' \
            '     4, 5, 6;' \
            '     7, 8, 9];' \
            'ret a[:, 2];'
        self.assertEqual([[3, 6, 9]], interpret(s).to_py())

    def test_column_colon_index(self):
        s = 'a = [1, 2, 3;' \
            '     4, 5, 6;' \
            '     7, 8, 9];' \
            'ret a[1, :];'
        self.assertEqual([[4, 5, 6]], interpret(s).to_py())

        s = 'a = [1, 2, 3;' \
            '     4, 5, 6;' \
            '     7, 8, 9];' \
            'ret a[2, :];'
        self.assertEqual([[7, 8, 9]], interpret(s).to_py())

    def test_double_colon_index(self):
        s = 'a = [1, 2, 3;' \
            '     4, 5, 6;' \
            '     7, 8, 9];' \
            'ret a[:, :];'
        self.assertEqual([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]], interpret(s).to_py())


if __name__ == '__main__':
    unittest.main()
