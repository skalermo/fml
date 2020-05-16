from Interpreter.Interpreter import Interpreter
from Parser.Parser import Parser
from Source.Source import StringSource
from Error import InterpreterError


def interpret(string_source):
    parser = Parser(StringSource(string_source))
    return Interpreter().interpret(parser.parse_program())


def should_fail(
        tester,
        string_source,
        expected_error_code=None,
        expected_id=None,
):
    parser = Parser(StringSource(string_source))
    with tester.assertRaises(InterpreterError) as e:
        Interpreter().interpret(parser.parse_program())
    if expected_error_code is not None:
        tester.assertEqual(expected_error_code, e.exception.error_code)
    if expected_id is not None:
        tester.assertEqual(expected_id, e.exception.id)
