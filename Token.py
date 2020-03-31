class TokenTypes:
    SEMI = 'SEMI'
    SCALAR = 'SCALAR'
    STRING = 'STRING'
    MATRIX = 'MATRIX'
    POW = 'POW'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    LPAREN = '('
    RPAREN = ')'
    ID = 'ID'
    EOF = 'EOF'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'and': Token('and', 'and'),
    'div': Token('div', 'div'),
    'do': Token('do', 'do'),
    'else': Token('else', 'else'),
    'for': Token('for', 'for'),
    'fun': Token('fun', 'fun'),
    'if': Token('if', 'if'),
    'in': Token('in', 'in'),
    'mod': Token('mod', 'mod'),
    'not': Token('not', 'not'),
    'or': Token('or', 'or'),
    'ret': Token('ret', 'ret'),
    'while': Token('while', 'while'),
}