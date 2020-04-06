from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError, ErrorCode


class Lexer:
    def __init__(self, source):
        self.source = source
        self.current_token = self.get_next_token()

    def error(self, error_code=None):
        s = "'{lexeme}' line: {line} column: {column}".format(
            lexeme=self.source.current_char,
            line=self.source.line,
            column=self.source.column,
        )
        raise LexerError(error_code=error_code, message=s)

    def skip_whitespace(self):
        skipped = 0
        while self.source.current_char.isspace():
            self.source.move_to_next_char()
            skipped += 1
        return skipped

    def skip_comment(self):
        if self.source.current_char == '#':
            while self.source.current_char != '\n':
                self.source.move_to_next_char()
            self.source.move_to_next_char()
            return True
        return False

    def try_to_build_scalar(self):
        result = ''

        # Handle integer part of scalar
        while self.source.current_char.isdigit():
            result += self.source.current_char
            self.source.move_to_next_char()

        # Handle decimal part of scalar
        if self.source.current_char == '.':
            result += self.source.current_char
            self.source.move_to_next_char()
            if self.source.current_char.isdigit():
                self.source.move_to_next_char()
                while self.source.current_char.isdigit():
                    result += self.source.current_char
                    self.source.move_to_next_char()

                # Handle scientific notation
                if self.source.current_char == 'e' or self.source.current_char == 'E':
                    result += self.source.current_char
                    if self.source.current_char == '-' or self.source.current_char == '+':
                        self.source.move_to_next_char()
                        result += self.source.current_char
                    if self.source.current_char.isdigit():
                        self.source.move_to_next_char()
                        while self.source.current_char.isdigit():
                            result += self.source.current_char
                            self.source.move_to_next_char()
                    else:
                        self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
            else:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        return float(result)

    def try_to_build_id(self):
        if not self.source.current_char.isalnum():
            return None

        # Create a new token with current line and column number
        token = Token(type=None, value=None, line=self.source.line, column=self.source.column)

        result = self.source.current_char
        self.source.move_to_next_char()

        while self.source.current_char.isalnum() or self.source.current_char == '_':
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
        while self.skip_comment() or self.skip_whitespace():
            pass

        token = None

        if token := self.try_to_build_scalar():
            return token

        if token := self.try_to_build_id():
            return token

        if self.source.current_char == '"':
            self.source.move_to_next_char()
            return Token(TokenType.STRING, self.string(), self.source.line, self.source.column)

        # Handle single-character tokens
        try:
            token_type = TokenType(self.source.current_char)
        except ValueError:
            # No enum member with value equal to self.source.current_char.
            self.error()
        else:
            # No exception occurred.
            # Create single-character token.
            token = Token(
                type=token_type,
                value=token_type.value,
                line=self.source.line,
                column=self.source.column
            )
            self.source.move_to_next_char()
            return token


