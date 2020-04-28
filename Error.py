import sys


# Custom exception handler
def handler(exception_type, exception, traceback):
    print(Error.message)


# sys.excepthook = handler


class ErrorCode:
    TOKEN_BUILD_FAIL = 'Failed to build a token'
    EXCEED_MAX_ID_SIZE = 'Exceeded max length of an identifier'

    UNEXPECTED_TOKEN = 'Unexpected token'
    EXPECTED_STATEMENT = 'Expected statement'
    EXPECTED_SEMI = 'Expected semicolon'
    MTRX_ROW_LEN_MISMATCH = 'Matrix should have rows of the same length'
    RVAL_FAIL = 'Expected rvalue, got nothing'

    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'


class Error(Exception):
    def __init__(self, error_code=None, position=None, context='', source_type='', token=''):
        # hide traceback of pycharm
        sys.tracebacklimit = 0

        # Error message structure:
        #   1. source type, line, column
        #   2. context
        #   3. pointer
        #   4. Error type, error message

        error_source = f'File "{source_type}", line {position.line}, column {position.column}\n'
        pointer_line = ''.join([' '*(len(context)-1), '^\n'])
        context += '\n'
        message = f'{type(self).__name__}: {error_code}\n'

        self.error_code = error_code
        self.message = ''.join([error_source, context, pointer_line, message])
        super().__init__(self.message)


class LexerError(Error):
    pass


class ParserError(Error):
    pass
