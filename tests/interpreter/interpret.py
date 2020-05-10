from Interpreter.Interpreter import Interpreter
from Parser.Parser import Parser
from Source.Source import StringSource


def interpret(string_source):
    parser = Parser(StringSource(string_source))
    return Interpreter().interpret(parser.parse_program())