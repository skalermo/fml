from Interpreter.Ast import AST
from Objects.Identifier import Identifier
from Objects.Builtins import BuiltinFunction


MAX_GENERIC_PARAMETERS = 10


class FunctionDefinition(AST):
    def __init__(self, id, parameter_token_list, statement):
        self.id = id
        self.parameter_list = parameter_token_list
        self.statement = statement

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.value}'

    def get_name(self):
        return self.id.value

    def make_generic_parameters(self, arguments):
        self.parameter_list = []
        if len(arguments) > MAX_GENERIC_PARAMETERS:
            self.parameter_list = None
            return

        if isinstance(self.statement, BuiltinFunction):
            self.statement.set_parameter_list(self.parameter_list)

        # chr(97) == 'a'
        for i in range(len(arguments)):
            self.parameter_list.append(Identifier(chr(97+i)))


class FunctionCall(AST):
    def __init__(self, id, argument_list):
        self.id = id
        self.argument_list = argument_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.value}'
