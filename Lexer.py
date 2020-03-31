from Token import TokenTypes, Token, RESERVED_KEYWORDS


class Lexer:
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '\n':
            self.advance()
        self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(TokenTypes.ID, result))
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char == ';':
                self.advance()
                return Token(TokenTypes.SEMI, ';')

            if self.current_char.isdigit():
                return Token(TokenTypes.SCALAR, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenTypes.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenTypes.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenTypes.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenTypes.DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenTypes.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenTypes.RPAREN, ')')

            self.error()

        return Token(TokenTypes.EOF, None)