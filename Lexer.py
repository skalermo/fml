from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError, ErrorCode


class Lexer:
    def __init__(self, source):
        self.source = source
        self.current_token = self.get_next_token()

    def error(self, error_code=None):
        s = "'{lexeme}' line: {line} column: {column}".format(
            lexeme=self.source.source.current_char,
            line=self.source.line,
            column=self.source.column,
        )
        raise LexerError(error_code=error_code, message=s)

    def skip_whitespace(self):
        while self.source.current_char is not None and self.source.current_char.isspace():
            self.source.move_to_next_char()

    def skip_comment(self):
        while self.source.current_char != '\n':
            self.source.move_to_next_char()
        self.source.move_to_next_char()

    def scalar(self):
        result = ''

        # Handle integer part of scalar
        while self.source.current_char is not None and self.source.current_char.isdigit():
            result += self.source.current_char
            self.source.move_to_next_char()

        # Handle decimal part of scalar
        if self.source.current_char == '.':
            result += self.source.current_char
            peeked_char = self.peek()
            if peeked_char is not None and peeked_char.isdigit():
                self.source.move_to_next_char()
                while self.source.current_char is not None and self.source.current_char.isdigit():
                    result += self.source.current_char
                    self.source.move_to_next_char()

                # Handle scientific notation
                if self.source.current_char == 'e' or self.source.current_char == 'E':
                    result += self.source.current_char
                    peeked_char = self.peek()
                    if peeked_char == '-' or peeked_char == '+':
                        self.source.move_to_next_char()
                        result += self.source.current_char
                    peeked_char = self.peek()
                    if peeked_char is not None and peeked_char.isdigit():
                        self.source.move_to_next_char()
                        while self.source.current_char is not None and self.source.current_char.isdigit():
                            result += self.source.current_char
                            self.source.move_to_next_char()
                    else:
                        self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
            else:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        return float(result)

    def id(self):
        # Create a new token with current line and column number
        token = Token(type=None, value=None, line=self.source.line, column=self.source.column)

        result = ''
        if self.source.current_char is not None and self.source.current_char.isalnum():
            result += self.source.current_char
            self.source.move_to_next_char()
        while self.source.current_char is not None \
                and (self.source.current_char.isalnum() or self.source.current_char == '_'):
            result += self.source.current_char
            self.source.move_to_next_char()

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

    def string(self):
        result = ''

        while self.source.current_char != '"':
            # if current char is '\'
            if self.source.current_char == '\\' and self.peek() == '"':
                result += '"'
                self.source.move_to_next_char()
                self.source.move_to_next_char()
            else:
                result += self.source.current_char
                self.source.move_to_next_char()

        self.source.move_to_next_char()
        return result

    def get_next_token(self):
        while self.source.current_char is not None:

            if self.source.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.source.current_char == '#':
                self.skip_comment()
                continue

            if self.source.current_char == ';':
                self.source.move_to_next_char()
                return Token(TokenType.SEMI, ';', self.source.line, self.source.column)

            if self.source.current_char.isdigit():
                return Token(TokenType.SCALAR, self.scalar(), self.source.line, self.source.column)

            if self.source.current_char.isalnum():
                return self.id()

            if self.source.current_char == '+':
                self.source.move_to_next_char()
                return Token(TokenType.PLUS, '+', self.source.line, self.source.column)

            if self.source.current_char == '-':
                self.source.move_to_next_char()
                return Token(TokenType.MINUS, '-', self.source.line, self.source.column)

            if self.source.current_char == '*':
                self.source.move_to_next_char()
                return Token(TokenType.MUL, '*', self.source.line, self.source.column)

            if self.source.current_char == '/':
                self.source.move_to_next_char()
                return Token(TokenType.FLOAT_DIV, '/', self.source.line, self.source.column)

            if self.source.current_char == '(':
                self.source.move_to_next_char()
                return Token(TokenType.LPAREN, '(', self.source.line, self.source.column)

            if self.source.current_char == ')':
                self.source.move_to_next_char()
                return Token(TokenType.RPAREN, ')', self.source.line, self.source.column)

            if self.source.current_char == '=':
                self.source.move_to_next_char()
                return Token(TokenType.EQ, '=', self.source.line, self.source.column)

            if self.source.current_char == '"':
                self.source.move_to_next_char()
                return Token(TokenType.STRING, self.string(), self.source.line, self.source.column)

            self.error()

        return Token(TokenType.EOF, None)
