class FunctionDefinition:
    def __init__(self, token_id, parameter_token_list, statement):
        self.token_id = token_id
        self.parameter_list = parameter_token_list
        self.statement = statement


class FunctionCall:
    def __init__(self, token_id, argument_list):
        self.token_id = token_id
        self.argument_list = argument_list
