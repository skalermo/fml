import unittest
from Source.Source import FileSource
from Lexer.Lexer import Lexer
from Lexer.Token import TokenType, Token


class PositionTest(unittest.TestCase):
    def test_trivial(self):
        file_source = FileSource('tokens/positions1.txt')
        lexer = Lexer(file_source)

        # positions within line
        positions = [1, 2, 3, 5, 9, 11, 14, 16]

        for expected_position in positions:
            token = lexer.current_token
            self.assertEqual(expected_position, token.position.column)
            lexer.build_next_token()

    def test_positions_on_multiple_lines(self):
        file_source = FileSource('tokens/positions2.txt')
        lexer = Lexer(file_source)

        positions = [
            (2, 1), (2, 3), (2, 5), (2, 8),
            (3, 1), (3, 3), (3, 5), (3, 7), (3, 8), (3, 9),
            (4, 1),
            (5, 5), (5, 6),
            (6, 10), (6, 12),
            (7, 7), (7, 9),
            (8, 1), (8, 4), (8, 6), (8, 10), (8, 18), (8, 19), (8, 21)
        ]

        for expected_position in positions:
            token = lexer.current_token
            self.assertEqual(expected_position[0], token.position.line)
            self.assertEqual(expected_position[1], token.position.column)
            lexer.build_next_token()

    def test_real_life_problems(self):
        file_source = FileSource('tokens/positions3.txt')
        lexer = Lexer(file_source)

        positions = [
            (2, 1), (2, 5), (2, 20), (2, 21), (2, 22),
            (3, 5), (3, 13), (3, 15), (3, 31), (3, 33), (3, 49), (3, 51), (3, 52),
            (4, 1)
        ]

        for expected_position in positions:
            token = lexer.current_token
            self.assertEqual(expected_position[0], token.position.line)
            self.assertEqual(expected_position[1], token.position.column)
            lexer.build_next_token()


if __name__ == '__main__':
    unittest.main()
