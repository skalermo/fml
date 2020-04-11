from Source import TokenType
from Error import ParserError, ErrorCode
from grammatical_objects.Program import Program
from grammatical_objects.Function import FunctionDefinition
from grammatical_objects.Statement import CompoundStatement


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        program = self.parse_program()

    def error(self, error_code=None, token=None):
        raise ParserError(error_code=error_code, message='')

    def parse_program(self):
        program = Program()
        while self.lexer.current_token.type != TokenType.ETX:
            if definition := self.try_to_parse_fun_definition():
                program.add_fun_def(definition)
            if statement := self.parse_statement():
                program.add_statement(statement)

        return program

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.build_next_token()

        fun_def = FunctionDefinition()

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        fun_def.id = self.lexer.current_token
        self.lexer.build_next_token()

        if self.lexer.current_token.type != TokenType.LPAREN:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        self.lexer.build_next_token()
        fun_def.add_parameters(self.parse_fun_parameters())

        fun_def.body = self.parse_statement()
        if fun_def.body is None:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        return fun_def

    def try_to_parse_expression(self):
        pass

    def try_to_parse_do_while_loop(self):
        pass

    def try_to_parse_while_loop(self):
        pass

    def try_to_parse_for_loop(self):
        pass

    def try_to_parse_if_statement(self):
        pass

    def try_to_parse_compound_statement(self):
        if self.lexer.current_token != TokenType.LCURB:
            return None

        self.lexer.build_next_token()
        statement_list = []
        while self.lexer.current_token != TokenType.RCURB:
            if self.lexer.current_token == TokenType.ETX:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            if statement := self.parse_statement():
                statement_list.append(statement)

        self.lexer.build_next_token()
        return CompoundStatement(statement_list)

    # static variable
    _parse_methods = [
        try_to_parse_expression,
        try_to_parse_do_while_loop,
        try_to_parse_while_loop,
        try_to_parse_for_loop,
        try_to_parse_if_statement,
        try_to_parse_compound_statement
    ]

    def parse_statement(self):
        for try_to_parse_statement in Parser._parse_methods:
            if statement := try_to_parse_statement(self):
                return statement

        return None

    def parse_fun_parameters(self):
        if self.lexer.current_token.type == TokenType.RPAREN:
            return []

        self.lexer.build_next_token()

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        parameter_list = [self.lexer.current_token]
        self.lexer.build_next_token()

        while self.lexer.current_token.type != TokenType.RPAREN:
            if self.lexer.current_token.type != TokenType.COMMA:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            self.lexer.build_next_token()

            if self.lexer.current_token.type != TokenType.ID:
                self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

            parameter_list.append(self.lexer.current_token)
            self.lexer.build_next_token()

        return parameter_list

















