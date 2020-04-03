import sys


class ErrorCode:
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'


class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        # Hide exception traceback
        sys.tracebacklimit = 0

        super().__init__(message)


class LexerError(Error):
    pass


class ParserError(Error):
    pass
