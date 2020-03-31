import unittest
from Lexer import Lexer
from Token import TokenTypes


class LexerTest(unittest.TestCase):
    def test_easy_expressions(self):
        with open('expressions/easy.txt') as file:
            lexer = Lexer(file.read())

        current_token = lexer.get_next_token()
        while current_token.type != TokenTypes.EOF:
            print(current_token)
            current_token = lexer.get_next_token()


if __name__ == '__main__':
    unittest.main()
