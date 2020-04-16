from Source import TokenType
from Error import ParserError, ErrorCode
from grammatical_objects.Program import Program
from grammatical_objects.Function import FunctionDefinition
from grammatical_objects.Statement import CompoundStatement


class Parser:
    # Static variables
    _parse_methods = []

    @classmethod
    def set_static_vars(cls):
        cls._parse_methods.extend([
            cls.try_to_parse_expression,
            cls.try_to_parse_do_while_loop,
            cls.try_to_parse_while_loop,
            cls.try_to_parse_for_loop,
            cls.try_to_parse_if_statement,
            cls.try_to_parse_compound_statement
        ])

    def __init__(self, lexer):
        self.lexer = lexer
        self.program = self.parse_program()

    def parse_program(self):
        fun_defs = {}
        statements = []

        while (definition := self.try_to_parse_fun_definition()) or\
                (statement := self.parse_statement()):
            if definition is not None:
                fun_defs[definition.id] = definition
            elif statement is not None:
                statements.append(statement)

        return Program(fun_defs, statements)

    def try_to_parse_fun_definition(self):
        if self.lexer.current_token.type != TokenType.FUN:
            return None
        self.lexer.build_next_token()

        if self.lexer.current_token.type != TokenType.ID:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        fun_id = self.lexer.current_token.value
        self.lexer.build_next_token()

        if self.lexer.current_token.type != TokenType.LPAREN:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        self.lexer.build_next_token()
        parameter_list = self.try_to_parse_fun_parameters()

        statement = self.parse_statement()
        # if fun_def.body is None:
        #     self.error(error_code=ErrorCode.UNEXPECTED_TOKEN)

        return FunctionDefinition(fun_id, parameter_list, statement)

    def parse_statement(self):
        for try_to_parse_statement in Parser._parse_methods:
            if statement := try_to_parse_statement(self):
                return statement

        return None

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

    def try_to_parse_fun_parameters(self):
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

    def error(self, error_code=None, token=None):
        raise ParserError(error_code=error_code, message='')
