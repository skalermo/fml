from abc import abstractmethod, ABC


from Objects.Scalar import Scalar
from Objects.Function import FunctionDefinition
from Lexer.Token import Token, TokenType
from Objects.Identifier import Identifier


class BuiltinFunctionCreator:
    @staticmethod
    def get_builtin_fun_defs():
        for builtin in [Abs(),
                        Len(),
                        Max(),
                        Min(),
                        Print(),
                        Round(),
                        Shape(),
                        Transpose()]:
            yield builtin


class BuiltinFunction(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def parameter_list(self):
        raise NotImplementedError

    @abstractmethod
    def get_parameters(self):
        pass

    def get_wrapped_fun(self):
        return FunctionDefinition(
            id = Identifier(Token(TokenType.ID, self.name)),
            parameter_token_list=self.parameter_list,
            statement=self
        )


class Abs(BuiltinFunction):
    name = 'abs'
    parameter_list = [Identifier(Token(TokenType.ID, '_'))]

    def get_parameters(self):
        return self.parameter_list[0]


class Len(BuiltinFunction):
    name = 'len'
    parameter_list = [Identifier(Token(TokenType.ID, 'a'))]

    def get_parameters(self):
        return self.parameter_list[0]


class Max(BuiltinFunction):
    name = 'max'
    parameter_list = [Identifier(Token(TokenType.ID, 'a')),
                      Identifier(Token(TokenType.ID, 'b'))]

    def get_parameters(self):
        return self.parameter_list[0], self.parameter_list[1]


class Min(BuiltinFunction):
    name = 'min'
    parameter_list = [Identifier(Token(TokenType.ID, 'a')),
                      Identifier(Token(TokenType.ID, 'b'))]

    def get_parameters(self):
        return self.parameter_list[0], self.parameter_list[1]


class Print(BuiltinFunction):
    name = 'print'
    parameter_list = [Identifier(Token(TokenType.ID, 'a'))]

    def get_parameters(self):
        return self.parameter_list[0]


class Round(BuiltinFunction):
    name = 'round'
    parameter_list = [Identifier(Token(TokenType.ID, 'a'))]

    def get_parameters(self):
        return self.parameter_list[0]


class Shape(BuiltinFunction):
    name = 'shape'
    parameter_list = [Identifier(Token(TokenType.ID, 'a'))]

    def get_parameters(self):
        return self.parameter_list[0]


class Transpose(BuiltinFunction):
    name = 'transp'
    parameter_list = [Identifier(Token(TokenType.ID, 'a'))]

    def get_parameters(self):
        return self.parameter_list[0]
