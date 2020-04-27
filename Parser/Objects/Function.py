class FunctionDefinition:
    def __init__(self, id, parameter_list, statement):
        self.id = id
        self.parameter_list = parameter_list
        self.statement = statement


class FunctionCall:
    def __init__(self, id, argument_list):
        self.id = id
        self.argument_list = argument_list
