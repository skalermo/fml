import unittest
from Lexer.Lexer import TokenType
from Error import ErrorCode
from tests.parser.utils import should_fail


class TestMatrixSubscriptingFails(unittest.TestCase):
    def test_no_semi(self):
        s = 'm[a]'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)

    def test_multiple_indices(self):
        s = 'm[a, b, c]'
        # expected two indices, got 3
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

    def test_empty_index(self):
        s = 'm[];'
        should_fail(self, s, ErrorCode.EXPECTED_EXPRESSION)

    def test_colon_index(self):
        s = 'm[:,];'
        should_fail(self, s, ErrorCode.EXPECTED_EXPRESSION)

        s = 'm[::];'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

        s = 'm[:,a+:];'
        should_fail(self, s, ErrorCode.EXPECTED_RVALUE)

        s = 'm[:,:+a];'
        should_fail(self, s, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)


if __name__ == '__main__':
    unittest.main()
