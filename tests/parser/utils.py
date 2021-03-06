from Source.Source import StringSource
from Parser.Parser import Parser
from Error import ParserError


def should_fail(
        tester,
        string_source,
        expected_error_code=None,
        expected_token_type=None,
        expected_description=None
):
    parser = Parser(StringSource(string_source))
    with tester.assertRaises(ParserError) as e:
        parser.parse_program()
    if expected_error_code is not None:
        tester.assertEqual(expected_error_code, e.exception.error_code)
    if expected_token_type is not None:
        tester.assertEqual(expected_token_type, e.exception.expected_token_type)
    if expected_description:
        tester.assertEqual(expected_description, e.exception.description)
