import sys


# Custom exception handler
def handler(exception_type, exception, traceback):
    print(Error.message)

sys.excepthook = handler


class ErrorCode:
    TOKEN_BUILD_FAIL = 'Failed to build a token'
    EXCEED_MAX_ID_SIZE = 'Exceeded max length of an identifier'

    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'


class Error(Exception):
    def __init__(self, message: str, error_code=None, token=None):
        # hide traceback of pycharm
        sys.tracebacklimit = 0

        self.error_code = error_code
        self.token = token
        self.message = message

        Error.message = f'{self.__class__.__name__}: {error_code}. {message}'
        # super().__init__(m)

    message = ''


class LexerError(Error):
    pass


class ParserError(Error):
    pass
