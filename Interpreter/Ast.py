from abc import ABC, abstractmethod


class AST(ABC):
    def __repr__(self) -> str:
        raise NotImplementedError


class NodeVisitor:
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
