import unittest
from Source.Source import FileSource
from Interpreter.Interpreter import Interpreter
from tests.interpreter.utils import interpret, should_fail
from Interpreter.AstDumper import dumpAST


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # dumpAST(FileSource('../../examples/perceptron.txt'))
        Interpreter(FileSource('../../examples/print_override_test.txt')).interpret().to_py()


if __name__ == '__main__':
    unittest.main()
