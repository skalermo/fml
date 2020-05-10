import unittest
from Parser.Parser import Parser
from Source.Source import StringSource


class TestMatrixObject(unittest.TestCase):
    @staticmethod
    def parse_matrix(string):
        parser = Parser(StringSource(string))
        return parser.try_to_parse_matrix()

    def test_empty_matrix(self):
        m = '[]'
        matrix = self.parse_matrix(m)
        self.assertEqual(0, len(matrix))

    def test_length_of_matrix(self):
        m = '[a]'
        matrix = self.parse_matrix(m)
        self.assertEqual(1, len(matrix))

        m = '[a, b, c, d]'
        matrix = self.parse_matrix(m)
        self.assertEqual(4, len(matrix))

    def test_length_of_nested_matrix(self):
        m = '[[]]'
        matrix = self.parse_matrix(m)
        self.assertEqual(1, len(matrix))

        m = '[[[]], [], [[]]]'
        matrix = self.parse_matrix(m)
        self.assertEqual(3, len(matrix))

    def test_length_of_multirow_matrix(self):
        m = '[1; 2]'
        matrix = self.parse_matrix(m)
        self.assertEqual(2, len(matrix))

        m = '[1, 2; 3, 4]'
        matrix = self.parse_matrix(m)
        self.assertEqual(4, len(matrix))


if __name__ == '__main__':
    unittest.main()
