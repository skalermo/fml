import unittest
from Source.Source import StringSource
from Parser.Parser import Parser
from Objects.String import String


class TestString(unittest.TestCase):
    def test_simple(self):
        s = '"Hello world";'
        self.assertEqual(String, type(Parser(StringSource(s)).try_to_parse_string()))

    def test_parse_program_with_string(self):
        s = 'a = 1 + 2;' \
            's = "some string";'
        Parser(StringSource(s)).parse_program()


if __name__ == '__main__':
    unittest.main()
