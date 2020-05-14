from Interpreter.Ast import AST


class Scalar(AST):
    def __init__(self, value):
        self.value = value

    def to_py(self):
        return self.value

    def __bool__(self):
        if self.value == 0:
            return False
        return True

    def __str__(self):
        return f'{self.__class__.__name__}: {self.value}'

    def __eq__(self, other):
        if not isinstance(other, Scalar):
            return False
        return self.value == other.value

    def get_value(self):
        return self.value
