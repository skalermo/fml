from abc import abstractmethod, ABC


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
    parameter_list = None
    name = None

    @abstractmethod
    def get_parameters(self):
        pass

    def set_parameter_list(self, parameters):
        self.parameter_list = parameters

    def get_wrapped_fun(self):
        return (Identifier(self.name),
                self.parameter_list,
                self)


class Abs(BuiltinFunction):
    name = 'abs'
    parameter_list = [Identifier('a')]

    def get_parameters(self):
        return self.parameter_list[0]


class Len(BuiltinFunction):
    name = 'len'
    parameter_list = [Identifier('a')]

    def get_parameters(self):
        return self.parameter_list[0]


class Max(BuiltinFunction):
    name = 'max'
    parameter_list = [Identifier('a'),
                      Identifier('b')]

    def get_parameters(self):
        return self.parameter_list[0], self.parameter_list[1]


class Min(BuiltinFunction):
    name = 'min'
    parameter_list = [Identifier('a'),
                      Identifier('b')]

    def get_parameters(self):
        return self.parameter_list[0], self.parameter_list[1]


class Print(BuiltinFunction):
    name = 'print'
    parameter_list = None

    def get_parameters(self):
        return self.parameter_list


class Round(BuiltinFunction):
    name = 'round'
    parameter_list = [Identifier('a')]

    def get_parameters(self):
        return self.parameter_list[0]


class Shape(BuiltinFunction):
    name = 'shape'
    parameter_list = [Identifier('a')]

    def get_parameters(self):
        return self.parameter_list[0]


class Transpose(BuiltinFunction):
    name = 'transpose'
    parameter_list = [Identifier('a')]

    def get_parameters(self):
        return self.parameter_list[0]
