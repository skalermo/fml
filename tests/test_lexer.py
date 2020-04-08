import unittest
from Lexer import Lexer
from Token import TokenType, Token, RESERVED_KEYWORDS
from Source import FileSource


class LexerTest(unittest.TestCase):
    def test_all_tokens(self):

        expected_tokens = [
            Token(t) for t in RESERVED_KEYWORDS.values()
        ] + [
            Token(TokenType.ID, 'a'),
            Token(TokenType.ID, 'aaa'),
            Token(TokenType.ID, 'a123'),
            Token(TokenType.ID, 'a_'),
            Token(TokenType.ID, 'a_123'),
            Token(TokenType.ID, 'abc_def_123gh'),
            Token(TokenType.SEMI),
            Token(TokenType.COMMA),
            Token(TokenType.COLON),
            Token(TokenType.PLUS),
            Token(TokenType.MINUS),
            Token(TokenType.MUL),
            Token(TokenType.FLOAT_DIV),
            Token(TokenType.ASSIGN),
            Token(TokenType.LPAREN),
            Token(TokenType.RPAREN),
            Token(TokenType.LBRACK),
            Token(TokenType.RBRACK),
            Token(TokenType.LCURB),
            Token(TokenType.RCURB),
            Token(TokenType.LESS),
            Token(TokenType.GRE),
            Token(TokenType.LEQ),
            Token(TokenType.GEQ),
            Token(TokenType.EQ),
            Token(TokenType.NEQ),
            Token(TokenType.POW),
            Token(TokenType.SCALAR, 0),
            Token(TokenType.SCALAR, 12),
            Token(TokenType.SCALAR, 12.345),
            Token(TokenType.SCALAR, 12.345),
            Token(TokenType.SCALAR, float('12.345e6')),
            Token(TokenType.SCALAR, float('12.345e-6')),
            Token(TokenType.SCALAR, 0),
            Token(TokenType.SCALAR, 0.01),
            Token(TokenType.SCALAR, float('0.001e2')),
            Token(TokenType.SCALAR, float('0.0001e-2'))
        ]

        file_source = FileSource('tokens/all_tokens.txt')
        lexer = Lexer(file_source)
        for expected_token in expected_tokens:
            token = lexer.current_token
            self.assertEqual(expected_token.type, token.type)
            self.assertEqual(expected_token.value, token.value)
            lexer.move_to_next_token()

        self.assertEqual(Token(TokenType.ETX).type, lexer.current_token.type)


if __name__ == '__main__':
    unittest.main()
