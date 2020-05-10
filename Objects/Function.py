from Interpreter.Ast import AST


class FunctionDefinition(AST):
    def __init__(self, id, parameter_token_list, statement):
        self.id = id
        self.parameter_list = parameter_token_list
        self.statement = statement

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.value}'

    def get_name(self):
        return self.id.value


class FunctionCall(AST):
    def __init__(self, id, argument_list):
        self.id = id
        self.argument_list = argument_list

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id.value}'
