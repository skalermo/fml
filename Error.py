import sys


# Custom exception handler
def handler(exception_type, exception, traceback):
    print(Error.message)


# sys.excepthook = handler


class ErrorCode:
    TOKEN_BUILD_FAIL = 'Failed to build a token'
    EXCEED_MAX_ID_SIZE = 'Exceeded max length of an identifier'

    UNEXPECTED_TOKEN = 'Unexpected token'
    EXPECTED_NOT_NONE = 'No object parsed.'
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


class ErrorDescription:
    EMPTY_FUN_BODY = 'Function body should not be empty.'
    EMPTY_DO_WHILE_BODY = 'Body of do while loop should not be emtpy.'
    EMPTY_DO_WHILE_CONDITION = 'Condition of do while loop should not be empty.'
    EMPTY_WHILE_BODY = 'Body of while loop should not be empty.'
    EMPTY_WHILE_CONDITION = 'Condition of while loop should not be empty.'
    NO_ITERABLE = 'No iterable found.'
    EMPTY_FOR_BODY = 'Body of for loop should not be empty.'
    EMPTY_IF_CONDITION = 'Condition of if statement should not be empty.'
    EMPTY_IF_BODY = 'Body of if statement should not be empty.'
    EMPTY_ELSE_BODY = 'Body of else statement should not be empty.'
    EMPTY_RET_BODY = 'Expression to return should not be empty.'
    NO_RVALUE = 'Expected rvalue, but got nothing.'
    EMPTY_MTRX_ROW = 'Expected matrix row, but got nothing.'
    NO_ARGUMENT = 'No argument found.'
    NO_INDEX = 'No index found.'
    NO_ITEM = 'No matrix item found.'
    EMPTY_COMPOUND_STATEMENT = 'Compound statement should not be empty.'


class Error(Exception):
    def __init__(self,
                 error_code=None,
                 position=None,
                 context='',
                 source_type='',
                 description='',
                 expected_token_type=None):
        # hide traceback of pycharm
        sys.tracebacklimit = 0

        # Error message structure:
        #   1. source type, line, column
        #   2. context
        #   3. pointer
        #   4. Error type, error message
        #   5. Description
        expected = ''
        if error_code == ErrorCode.UNEXPECTED_TOKEN and expected_token_type is not None:
            expected = f', expected {expected_token_type}'
        error_source = f'File "{source_type}", line {position.line}, column {position.column}\n'
        pointer_line = ''.join([' '*(len(context)-1), '^\n'])
        context += '\n'
        message = f'{type(self).__name__}: {error_code}{expected}\n'
        if description:
            description += '\n'

        self.expected_token_type = expected_token_type
        self.error_code = error_code
        self.message = ''.join([error_source, context, pointer_line, message, description])
        super().__init__(self.message)


class LexerError(Error):
    pass


class ParserError(Error):
    pass
