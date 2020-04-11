class FunctionDefinition:
    def __init__(self):
        self.id = ''
        self.parameter_list = []
        self.body = None

    def add_parameters(self, parameter_list):
        self.parameter_list = parameter_list