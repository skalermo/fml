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
    EXPECTED_EXPRESSION = 'Expected expression'
    EXPECTED_ID = 'Expected identifier'
    EXPECTED_SEMI = 'Expected semicolon'
    EXPECTED_ITERABLE = 'Expected iterable'
    EXPECTED_CONDITION = 'Condition is empty'
    EXPECTED_MTRX_ROW = 'Expected matrix row'
    EXPECTED_MTRX_ITEM = 'Expected matrix item'
    EXPECTED_RVALUE = 'Expected rvalue'

    MTRX_ROW_LEN_MISMATCH = 'Matrix should have rows of the same length'

    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'


class Error(Exception):
    def __init__(self, error_code=None, position=None, context='', source_type='', expected_token_type=None):
        # hide traceback of pycharm
        sys.tracebacklimit = 0

        # Error message structure:
        #   1. source type, line, column
        #   2. context
        #   3. pointer
        #   4. Error type, error message
        expected = ''
        if error_code == ErrorCode.UNEXPECTED_TOKEN and expected_token_type is not None:
            expected = f', expected {expected_token_type}'
        error_source = f'File "{source_type}", line {position.line}, column {position.column}\n'
        pointer_line = ''.join([' '*(len(context)-1), '^\n'])
        context += '\n'
        message = f'{type(self).__name__}: {error_code}{expected}\n'

        self.expected_token_type = expected_token_type
        self.error_code = error_code
        self.message = ''.join([error_source, context, pointer_line, message])
        super().__init__(self.message)


class LexerError(Error):
    pass


class ParserError(Error):
    pass
