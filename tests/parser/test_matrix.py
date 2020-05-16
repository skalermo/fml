import unittest
from Lexer.Lexer import TokenType
from Error import ErrorCode, ErrorDescription
from tests.parser.utils import should_fail


class TestMatrixFails(unittest.TestCase):
    def test_rbrack_missing(self):
        m = '['
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

    def test_comma_missing(self):
        m = '[a b];'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

    def test_one_row(self):
        m = '[a, ]'
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.NO_ITEM)

        m = '[a, b, '
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.NO_ITEM)

        m = '[, b, '
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

        m = '[a, b, c]'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)

    def test_multiple_rows(self):
        m = '[a;];'
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_MTRX_ROW)

        m = '[[]'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

        m = '[' \
            'a, b;' \
            'b, c;' \
            'c, d, e' \
            ']'
        should_fail(self, m, ErrorCode.MTRX_ROW_LEN_MISMATCH)

        m = '[[' \
            'a, b;' \
            'b, c;' \
            'c, d, e]]'
        should_fail(self, m, ErrorCode.MTRX_ROW_LEN_MISMATCH)

        m = '[a;b;;d]'
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_MTRX_ROW)

        m = '[' \
            '1+2+3;' \
            ';' \
            '5*3**2-1' \
            '];'
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_MTRX_ROW)

    def test_nested_matrices_without_semi(self):
        m = '[[[[]]]]'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)

        m = '[[[]]]]'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)
        m = '[' \
            '[], [], []' \
            ']'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.SEMI)

    def test_nested_matrices(self):
        m = '[[[[]]]'
        should_fail(self, m, ErrorCode.UNEXPECTED_TOKEN, TokenType.RBRACK)

        m = '[' \
            '[], [], [];' \
            '];'
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.EMPTY_MTRX_ROW)

        m = '[' \
            '[], [], [];' \
            '[], [],' \
            '];'
        should_fail(self, m,
                    ErrorCode.EXPECTED_NOT_NONE,
                    None,
                    ErrorDescription.NO_ITEM)

        m = '[' \
            '[], [], [];' \
            '[], []' \
            '];'
        should_fail(self, m, ErrorCode.MTRX_ROW_LEN_MISMATCH)

        # maybe error is not so obvious
        # test for row length is executed
        # within matrix object creation
        m = '[' \
            '[a], [a], [a];' \
            '[a], []a, [a];' \
            '[a], [a], [a]' \
            '];'
        should_fail(self, m, ErrorCode.MTRX_ROW_LEN_MISMATCH)


if __name__ == '__main__':
    unittest.main()
