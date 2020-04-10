import unittest
from Lexer import Lexer
from Token import TokenType, Token, RESERVED_KEYWORDS
from Source import FileSource, StringSource
from Error import LexerError, ErrorCode


class LexerTest(unittest.TestCase):
    def test_all_tokens(self):

        tokens = [
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
            Token(TokenType.SCALAR, float('0.0001e-2')),
            Token(TokenType.ETX)
        ]

        file_source = FileSource('tokens/all_tokens.txt')
        lexer = Lexer(file_source)
        for expected_token in tokens:
            token = lexer.current_token
            self.assertEqual(expected_token.type, token.type)
            self.assertEqual(expected_token.value, token.value)
            lexer.build_next_token()

    def test_unknown_single_char_token(self):
        string = '^'
        string_source = StringSource(string)
        with self.assertRaises(LexerError) as e:
            Lexer(string_source)
        self.assertNotEqual(ErrorCode.UNEXPECTED_TOKEN, e.exception.error_code)
        self.assertEqual(ErrorCode.TOKEN_BUILD_FAIL, e.exception.error_code)

    def test_etx_on_comment_line(self):
        string = 'not_comment = 1; # a comment'
        lexer = Lexer(StringSource(string))

        tokens = [
            Token(TokenType.ID, 'not_comment'),
            Token(TokenType.ASSIGN),
            Token(TokenType.SCALAR, 1),
            Token(TokenType.SEMI),
            Token(TokenType.ETX)
        ]

        for expected_token in tokens:
            token = lexer.current_token
            self.assertEqual(expected_token.type, token.type)
            self.assertEqual(expected_token.value, token.value)
            lexer.build_next_token()

    def test_etx_in_unfinished_string(self):
        string = '"some random string'
        with self.assertRaises(LexerError):
            lexer = Lexer(StringSource(string))
            while lexer.current_token.type != TokenType.ETX:
                lexer.build_next_token()

    def test_too_long_id(self):
        id = ''.join(['a']*128)

        # should pass
        try:
            Lexer(StringSource(id))
        except LexerError:
            self.fail()

        # should fail
        id += 'a'
        with self.assertRaises(LexerError) as e:
            Lexer(StringSource(id))
        self.assertEqual(ErrorCode.EXCEED_MAX_ID_SIZE, e.exception.error_code)

    def test_scalar_starts_with_zeros(self):
        string = '0'

        # should pass
        try:
            Lexer(StringSource(string))
        except LexerError:
            self.fail()

        string += '0'
        # should fail
        with self.assertRaises(LexerError):
            Lexer(StringSource(string))


if __name__ == '__main__':
    unittest.main()
