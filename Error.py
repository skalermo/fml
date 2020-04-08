import sys


class ErrorCode:
    TOKEN_BUILD_FAIL = 'Failed to build a token'
    EXCEED_MAX_ID_SIZE = 'Exceeded max length of an identifier'

    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'


class Error(Exception):
    def __init__(self, message: str, error_code=None, token=None):
        # Hide exception traceback
        sys.tracebacklimit = 0
        m = error_code
        if token is not None:
            m += f" '{token}'"
        else:
            m += f' {message}'
        super().__init__(m)


class LexerError(Error):
    pass


class ParserError(Error):
    pass
