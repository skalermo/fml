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


class Scope(SymbolTable):
    def __init__(self, inside_function=False):
        super().__init__()
        self.inside_function = inside_function


class Environment:
    def __init__(self):
        # first scope on the list is the global scope
        # last scope is a local scope
        self.scopes: List[Scope] = [Scope()]
        self.global_scope = self.scopes[0]
        self.local_scope = self.scopes[-1]

        self.fun_table = {}
        self.fun_nesting_level = 0

    def new_local_scope(self, is_for_fun_call=False):
        self.scopes.append(Scope(is_for_fun_call))
        self.local_scope = self.scopes[-1]

        if is_for_fun_call:
            self.fun_nesting_level += 1

    def destroy_local_scope(self):
        # make sure not to delete global scope
        if len(self.scopes) >= 1:
            del self.scopes[-1]
            self.local_scope = self.scopes[-1]

    def add_var(self, var: Identifier, evaluated_value):
        self.local_scope[var.get_name()] = evaluated_value

    def get_var(self, var_name: str):
        # check local scope
        if self.local_scope[var_name] is not None:
            return self.local_scope[var_name]

        # now check second to the last scope
        # make sure we are not inside a function
        if not self.local_scope.inside_function \
                and len(self.scopes) >= 1 \
                and self.scopes[-2][var_name] is not None:
            return self.scopes[-2][var_name]

        # finally return either from global scope or None
        return self.global_scope[var_name]

