class Program:
    def __init__(self):
        self.function_definitions = []
        self.statements = []

    def add_fun_def(self, definition):
        self.function_definitions.append(definition)

    def add_statement(self, statement):
        self.statements.append(statement)