from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError


class Lexer:
    def __init__(self, text):
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1

    def error(self):
        s = "Lexer error on '{lexeme}' line: {line} column: {column}".format(
            lexeme=self.current_char,
            line=self.line,
            column=self.column,
        )
        raise LexerError(message=s)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def next(self):
        # Move to the next character
        # Set current_char
        if self.current_char == '\n':
            self.line += 1
            self.column = 0

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Reached end of the input
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    def skip_comment(self):
        while self.current_char != '\n':
            self.next()
        self.next()

    def scalar(self):
        result = ''

        # Handle integer part of scalar
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.next()

        return int(result)

    def id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.next()

        token = RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result, self.line, self.column))
        return token

    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char == ';':
                self.next()
                return Token(TokenType.SEMI, ';', self.line, self.column)

            if self.current_char.isdigit():
                return Token(TokenType.SCALAR, self.scalar(), self.line, self.column)

            if self.current_char == '+':
                self.next()
                return Token(TokenType.PLUS, '+', self.line, self.column)

            if self.current_char == '-':
                self.next()
                return Token(TokenType.MINUS, '-', self.line, self.column)

            if self.current_char == '*':
                self.next()
                return Token(TokenType.MUL, '*', self.line, self.column)

            if self.current_char == '/':
                self.next()
                return Token(TokenType.DIV, '/', self.line, self.column)

            if self.current_char == '(':
                self.next()
                return Token(TokenType.LPAREN, '(', self.line, self.column)

            if self.current_char == ')':
                self.next()
                return Token(TokenType.RPAREN, ')', self.line, self.column)

            self.error()

        return Token(TokenType.EOF, None)
