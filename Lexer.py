from Token import TokenType, Token, RESERVED_KEYWORDS
from Error import LexerError, ErrorCode
from Position import Position

MAX_ID_LENGTH = 128


class Lexer:
    def __init__(self, source):
        self.current_token = None
        self.source = source
        self.build_next_token()

    def error(self, error_code=None):
        s = "'{lexeme}' line: {position.line} column: {position.column}".format(
            lexeme=self.source.current_char,
            position=Position(self.source)
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

        collected_chars = []

        # Handle integer part of scalar
        if self.source.current_char == '0':
            collected_chars.append('0')
            self.source.move_to_next_char()
            if self.source.current_char.isdigit():
                self.error(error_code=ErrorCode.TOKEN_BUILD_FAIL)
        else:
            while self.source.current_char.isdigit():
                collected_chars.append(self.source.current_char)
                self.source.move_to_next_char()

        # Handle decimal part of scalar
        if self.source.current_char == '.':
            collected_chars.append(self.source.current_char)
            self.source.move_to_next_char()

            if not self.source.current_char.isdigit():
                self.error(error_code=ErrorCode.TOKEN_BUILD_FAIL)

            while self.source.current_char.isdigit():
                collected_chars.append(self.source.current_char)
                self.source.move_to_next_char()

            # Handle scientific notation
            if self.source.current_char == 'e' or self.source.current_char == 'E':
                collected_chars.append(self.source.current_char)
                self.source.move_to_next_char()

                if self.source.current_char == '-' or self.source.current_char == '+':
                    collected_chars.append(self.source.current_char)
                    self.source.move_to_next_char()

                if not self.source.current_char.isdigit():
                    self.error(error_code=ErrorCode.TOKEN_BUILD_FAIL)

                while self.source.current_char.isdigit():
                    collected_chars.append(self.source.current_char)
                    self.source.move_to_next_char()

        # convert to string
        result = ''.join(collected_chars)

        return Token(
            type=TokenType.SCALAR,
            value=float(result),
        )

    def try_to_build_id(self):
        if not self.source.current_char.isalpha():
            return None

        collected_chars = [self.source.current_char]
        length_of_result = 1
        self.source.move_to_next_char()

        while length_of_result <= MAX_ID_LENGTH and \
                (self.source.current_char.isalnum() or self.source.current_char == '_'):
            collected_chars.append(self.source.current_char)
            self.source.move_to_next_char()
            length_of_result += 1

        if length_of_result > MAX_ID_LENGTH:
            self.error(error_code=ErrorCode.EXCEED_MAX_ID_SIZE)

        # convert to string
        result = ''.join(collected_chars)

        if not (token_type := RESERVED_KEYWORDS.get(result)):
            token_type = TokenType.ID

        return Token(
            type=token_type,
            value=result,
        )

    def try_to_build_string(self):
        if self.source.current_char != '"':
            return None

        collected_chars = []

        self.source.move_to_next_char()

        while self.source.current_char != '"':
            # string hasn't been finished, ETX appeared
            if self.source.current_char != TokenType.ETX.value:
                self.error(error_code=ErrorCode.TOKEN_BUILD_FAIL)

            # if current char is '\'
            if self.source.current_char == '\\':
                self.source.move_to_next_char()

                collected_chars.append({
                    '"': '"',
                    '\\': '\\'
                }.get(self.source.current_char, f'\\{self.source.current_char}'))
            else:
                collected_chars.append(self.source.current_char)
            self.source.move_to_next_char()

        self.source.move_to_next_char()

        # convert to string
        result = ''.join(collected_chars)

        return Token(
            type=TokenType.STRING,
            value=result,
        )

    # Static variable
    _similar_token_types = [
        (TokenType.MUL, TokenType.POW),
        (TokenType.LESS, TokenType.LEQ),
        (TokenType.GRE, TokenType.GEQ),
        (TokenType.ASSIGN, TokenType.EQ)
    ]

    def try_to_build_similar_tokens(self):
        for type_1char, type_2chars in Lexer._similar_token_types:
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
            return None
        else:
            # No exception occurred.
            # Return created single-character token.
            self.source.move_to_next_char()
            return Token(type=token_type)

    # Static variable
    _building_methods = [
        try_to_build_scalar,
        try_to_build_id,
        try_to_build_string,
        try_to_build_similar_tokens,
        try_to_build_neq,   # not equal (!=) token
        try_to_build_single_char_token
    ]

    def build_next_token(self):
        while self.skip_comment() or self.skip_whitespace():
            pass

        position = Position(self.source)

        for try_to_build_token in Lexer._building_methods:
            if token := try_to_build_token(self):
                token.position = position
                self.current_token = token
                return

        # If no success in building a known token
        self.error(error_code=ErrorCode.TOKEN_BUILD_FAIL)


