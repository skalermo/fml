from abc import abstractmethod


from Objects.Scalar import Scalar
from Lexer.Token import Token, TokenType


class BuiltinFunction():
    @abstractmethod
    def __call__(self, *args):
        pass


class Abs(BuiltinFunction):
    def __init__(self):
        self.name = 'abs'

    def __call__(self, scalar):
        return Scalar(Token(TokenType(abs(scalar.token.value))))


class Len(BuiltinFunction):
    def __init__(self):
        self.name = 'len'

    def __call__(self, object):
        return len(object)


class Max(BuiltinFunction):
    def __init__(self):
        self.name = 'max'

    def __call__(self, *args):
        pass


class Min(BuiltinFunction):
    def __init__(self):
        self.name = 'max'

    def __call__(self, *args):
        pass


class Print(BuiltinFunction):
    def __init__(self):
        self.name = 'print'

    def __call__(self, *args):
        print(*args)


