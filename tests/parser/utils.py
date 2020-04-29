from Source.Source import StringSource
from Lexer.Lexer import Lexer
from Parser.Parser import Parser
from Error import ParserError, ErrorCode


def should_fail(tester, string_source, expected_error_code=None, expected_token_type=None):
    parser = Parser(Lexer(StringSource(string_source)))
    with tester.assertRaises(ParserError) as e:
        parser.parse_program()
    if expected_error_code is not None:
        tester.assertEqual(expected_error_code, e.exception.error_code)
    if expected_token_type is not None:
        tester.assertEqual(expected_token_type, e.exception.expected_token_type)