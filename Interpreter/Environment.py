# How environment works in fml:
#
# Environment - Global scope + Call stack.
# Global scope can be seen everywhere in program.
#
# Call stack - [FunctionScope, FunctionScope, ...]
# FunctionScope - [LocalScope[LocalScope[...]]]
# A local scope inside global scope is also stored on call stack.


from typing import List, Dict
from Parser.Objects.Identifier import Identifier


class Symbol:
    pass


class SymbolTable:
    def __init__(self):
        self.symbol_table: Dict[str: Symbol] = {}

    def __setitem__(self, key, value):
        self.symbol_table[key] = value

    def __getitem__(self, item):
        return self.symbol_table.get(item, None)


class Scope:
    pass


class LocalScope(Scope):
    pass


class FunctionScope(Scope):
    pass


class Environment:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.call_stack = []

    # def destroy_local_scope(self):
    #     # make sure not to delete global scope
    #     if len(self.scopes) >= 1:
    #         del self.scopes[-1]
    #         self.local_scope = self.scopes[-1]
    #
    # def add_var(self, var: Identifier, evaluated_value):
    #     self.local_scope[var.get_name()] = evaluated_value
    #
    # def get_var(self, var_name: str):
    #     # check local scope
    #     if self.local_scope[var_name] is not None:
    #         return self.local_scope[var_name]
    #
    #     # now check second to the last scope
    #     # make sure we are not inside a function
    #     if not self.local_scope.inside_function \
    #             and len(self.scopes) >= 1 \
    #             and self.scopes[-2][var_name] is not None:
    #         return self.scopes[-2][var_name]
    #
    #     # finally return either from global scope or None
    #     return self.global_scope[var_name]
    #
