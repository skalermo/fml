from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError, ErrorCode


class Lexer:
    def __init__(self, source):
        self.current_token = None
        self.source = source
        self.move_to_next_token()

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
            while self.source.current_char != '\n' \
                    and self.source.current_char != TokenType.ETX.value:

                self.source.move_to_next_char()
            self.source.move_to_next_char()
            return True
        return False

    def try_to_build_scalar(self):
        if not self.source.current_char.isdigit():
            return None

        result = ''
        token = Token(
            type=TokenType.SCALAR,
            value=None,
            line=self.source.line,
            column=self.source.column
        )

        # Handle integer part of scalar
        if self.source.current_char == '0':
            result += '0'
            self.source.move_to_next_char()
            if self.source.current_char.isdigit():
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
        else:
            while self.source.current_char.isdigit():
                result += self.source.current_char
                self.source.move_to_next_char()

        # Handle decimal part of scalar
        if self.source.current_char == '.':
            result += self.source.current_char
            self.source.move_to_next_char()

            if not self.source.current_char.isdigit():
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            while self.source.current_char.isdigit():
                result += self.source.current_char
                self.source.move_to_next_char()

            # Handle scientific notation
            if self.source.current_char == 'e' or self.source.current_char == 'E':
                result += self.source.current_char
                self.source.move_to_next_char()

                if self.source.current_char == '-' or self.source.current_char == '+':
                    self.source.move_to_next_char()
                    result += self.source.current_char

                if not self.source.current_char.isdigit():
                    self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

                while self.source.current_char.isdigit():
                    result += self.source.current_char
                    self.source.move_to_next_char()

        token.value = float(result)
        return token

    def try_to_build_id(self):
        if not self.source.current_char.isalpha():
            return None

        token = Token(
            type=None,
            value=None,
            line=self.source.line,
            column=self.source.column
        )

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

    def try_to_build_string(self):
        if self.source.current_char != '"':
            return None
        result = ''

        token = Token(
            type=TokenType.STRING,
            value=None,
            line=self.source.line,
            column=self.source.column
        )

        self.source.move_to_next_char()

        while self.source.current_char != '"':
            # if current char is '\'
            if self.source.current_char == '\\':
                self.source.move_to_next_char()

                result += {
                    '"': '"',
                    '\\': '\\'
                }.get(self.source.current_char, f'\\{self.source.current_char}')
            else:
                result += self.source.current_char
            self.source.move_to_next_char()

        self.source.move_to_next_char()
        token.value = result
        return token

    def try_to_build_pow(self):
        if self.source.current_char != '*':
            return None

        self.source.move_to_next_char()
        if self.source.current_char == '*':
            self.source.move_to_next_char()
            return Token(
                type=TokenType.POW,
                value=TokenType.POW.value,
                line=self.source.line,
                column=self.source.column
            )
        return Token(
            type=TokenType.MUL,
            value=TokenType.MUL.value,
            line=self.source.line,
            column=self.source.column
        )

    def move_to_next_token(self):
        while self.skip_comment() or self.skip_whitespace():
            pass

        if token := self.try_to_build_scalar():
            self.current_token = token
            return

        if token := self.try_to_build_id():
            self.current_token = token
            return

        if token := self.try_to_build_string():
            self.current_token = token
            return

        if token := self.try_to_build_pow():
            self.current_token = token
            return

        # Handle single-character tokens
        try:
            token_type = TokenType(self.source.current_char)
        except ValueError:
            # No enum member with value equal to self.source.current_char.
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
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
            self.current_token = token
            return


