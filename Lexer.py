from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError, ErrorCode


class Lexer:
    def __init__(self, text):
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1

    def error(self, error_code=None):
        s = "'{lexeme}' line: {line} column: {column}".format(
            lexeme=self.current_char,
            line=self.line,
            column=self.column,
        )
        raise LexerError(error_code=error_code, message=s)

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

        # Handle decimal part of scalar
        if self.current_char == '.':
            result += self.current_char
            peeked_char = self.peek()
            if peeked_char is not None and peeked_char.isdigit():
                self.next()
                while self.current_char is not None and self.current_char.isdigit():
                    result += self.current_char
                    self.next()

                # Handle scientific notation
                if self.current_char == 'e' or self.current_char == 'E':
                    result += self.current_char
                    peeked_char = self.peek()
                    if peeked_char == '-' or peeked_char == '+':
                        self.next()
                        result += self.current_char
                    peeked_char = self.peek()
                    if peeked_char is not None and peeked_char.isdigit():
                        self.next()
                        while self.current_char is not None and self.current_char.isdigit():
                            result += self.current_char
                            self.next()
                    else:
                        self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
            else:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        return float(result)

    def id(self):
        # Create a new token with current line and column number
        token = Token(type=None, value=None, line=self.line, column=self.column)

        result = ''
        if self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.next()
        while self.current_char is not None \
                and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.next()

        token_type = RESERVED_KEYWORDS.get(result)
        if token_type is None:
            # identifier
            token.type = TokenType.ID
            token.value = result
        else:
            # reserved keyword
            token.type = token_type
            token.value = result
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

            if self.current_char.isalnum():
                return self.id()

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

            if self.current_char == '=':
                self.next()
                return Token(TokenType.EQ, '=', self.line, self.column)

            self.error()

        return Token(TokenType.EOF, None)
