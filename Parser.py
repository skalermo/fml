from Source import TokenType
from Error import ParserError, ErrorCode


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        program = self.parse_program()

    def error(self, error_code=None):
        raise ParserError(error_code=error_code)

    def parse_program(self):
        program = Program()
        while self.lexer.current_token.type != TokenType.ETX:
            if definition := self.try_to_parse_fun_definition():
                program.add_fun_def(definition)
            if statement := self.try_to_parse_statement():
                program.add_statement(statement)

        return program

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.move_to_next_token()

        fun_def = FunctionDefinition()

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        fun_def.set_fun_id(self.lexer.current_token)
        self.lexer.move_to_next_token()

        if self.lexer.current_token.type != TokenType.LPAREN:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        self.parse_fun_parameters()

        # parameters
        # fun body

    def try_to_parse_statement(self):
        pass

    def parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        if self.lexer.current_token.type != TokenType.ID:
            self.error()

        parameter_list = [self.lexer.current_token]
        self.lexer.move_to_next_token()

        while self.lexer.current_token.type != TokenType.RPAREN:
            if self.lexer.current_token.type != TokenType.COMMA:
                self.error()

            self.lexer.move_to_next_token()

            if self.lexer.current_token.type != TokenType.ID:
                self.error()

            parameter_list.append(self.lexer.current_token)
            self.lexer.move_to_next_token()

        return parameter_list


class Program:
    def __init__(self):
        pass

    def add_fun_def(self, definition):
        pass

    def add_statement(self, statement):
        pass


class FunctionDefinition:
    def __init__(self):
        self.id = ''
        self.parameter_list = []
        self.body = []

    def set_fun_id(self, id):
        self.id = id

    def parse_parameters(self):
        pass


class Statement:
    pass

class CompoundStatement(Statement):
    pass

