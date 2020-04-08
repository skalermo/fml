from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError, ErrorCode
from Position import PositionBuilder

MAX_ID_LENGTH = 128


class Lexer:
    def __init__(self, source):
        self.current_token = None
        self.source = source
        self._position_builder = PositionBuilder(source)
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
                    result += self.source.current_char
                    self.source.move_to_next_char()

                if not self.source.current_char.isdigit():
                    self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

                while self.source.current_char.isdigit():
                    result += self.source.current_char
                    self.source.move_to_next_char()

        return Token(
            type=TokenType.SCALAR,
            value=float(result),
        )

    def try_to_build_id(self):
        if not self.source.current_char.isalpha():
            return None

        result = self.source.current_char
        length_of_result = 1
        self.source.move_to_next_char()

        while length_of_result <= MAX_ID_LENGTH and \
                (self.source.current_char.isalnum() or self.source.current_char == '_'):
            result += self.source.current_char
            length_of_result += 1
            self.source.move_to_next_char()

        if length_of_result > MAX_ID_LENGTH:
            self.error(error_code=ErrorCode.EXCEED_MAX_ID_SIZE)

        if not (token_type := RESERVED_KEYWORDS.get(result)):
            token_type = TokenType.ID

        return Token(
            type=token_type,
            value=result,
        )

    def try_to_build_string(self):
        if self.source.current_char != '"':
            return None

        result = ''

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

        return Token(
            type=TokenType.STRING,
            value=result,
        )

    def try_to_build_similar_tokens(self):
        similar_token_types = [
            (TokenType.MUL, TokenType.POW),
            (TokenType.LESS, TokenType.LEQ),
            (TokenType.GRE, TokenType.GEQ),
            (TokenType.ASSIGN, TokenType.EQ)
        ]
        for type_1char, type_2chars in similar_token_types:
            if token := self._generic_builder(type_1char, type_2chars):
                return token
        return None

    def _generic_builder(self, type_1char, type_2chars):
        if self.source.current_char != type_1char.value:
            return None

        self.source.move_to_next_char()

        if self.source.current_char == type_2chars.value[-1]:
            self.source.move_to_next_char()
            return Token(type=type_2chars)
        return Token(type=type_1char)

    def try_to_build_neq(self):
        if self.source.current_char != '!':
            return None

        self.source.move_to_next_char()

        if self.source.current_char != '=':
            self.error(error_code=ErrorCode.TOKEN_BUILD_FAIL)
        self.source.move_to_next_char()
        return Token(type=TokenType.NEQ)

    def try_to_build_single_char_token(self):
        # Handle single-character tokens
        try:
            token_type = TokenType(self.source.current_char)
        except ValueError:
            # No enum member with value equal to self.source.current_char.
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)
        else:
            # No exception occurred.
            # Return created single-character token.
            self.source.move_to_next_char()
            return Token(type=token_type)

    def move_to_next_token(self):
        while self.skip_comment() or self.skip_whitespace():
            pass

        position = self._position_builder.current_position()

        # Last method raises exception if doesn't manage to build a token
        building_methods = [
            self.try_to_build_scalar,
            self.try_to_build_id,
            self.try_to_build_string,
            self.try_to_build_similar_tokens,
            self.try_to_build_neq,
            self.try_to_build_single_char_token
        ]

        for try_to_build_token in building_methods:
            if token := try_to_build_token():
                token.position = position
                self.current_token = token
                return




