# How environment works in fml:
#
# Environment = Outer scope + Global scope + Call stack.
#
# Outer scope is at the lowest level.
# Outer scope contains built-in functions and variables
# and can be seen everywhere in program.
# Outer scope's variables or functions cannot be changed by user,
# but can be covered by vars in higher scopes.
#
# Global scope can be seen everywhere in program.
#
# Call stack = [LocalScope, FunctionScope, FunctionScope, ...]
#
# There is no object FunctionScope
# Instead 2 normal scopes are created:
#   first one to save function call arguments
#   second is for scope inside function
#
# Scopes are linked:
# Outer scope <- Global scope <- Grandparent scope <- Parent scope <- Child scope
#
# When function call takes place the previous scope is stored on call stack.
# When program exits a call the last scope is popped from stack.
#
# LocalScope can be stored on call stack
# in case there was new function call.


from Objects.Identifier import Identifier
from Objects.Function import FunctionDefinition
from Objects.Builtins import BuiltinFunctionCreator


class Scope:
    def __init__(self, parent_scope=None):
        self.parent_scope = parent_scope
        self.symbol_table = {}

    def set_var(self, var: Identifier, evaluated_value):
        # To set variable means that
        # the variable got assigned.
        # First check if the variable exists
        # in one of the parent scopes and if it does, reassign it.
        # If it doesn't, add it to the symbol table of this scope.

        if not self.try_to_find_var_and_set_it(var, evaluated_value):
            self.symbol_table[var.get_name()] = evaluated_value

    def try_to_find_var_and_set_it(self, var: Identifier, evaluated_value):
        # Check if var is in the current scope.
        # If it's not check in the parent scope.
        # Function stops calling itself when var is found and set
        # or when it reaches global scope where it is stopped.
        # Returns True if found and set var in current scope.
        # Otherwise returns what parent returned.

        if var.get_name() in self.symbol_table:
            self.symbol_table[var.get_name()] = evaluated_value
            return True
        return self.parent_scope.try_to_find_var_and_set_it(var, evaluated_value)

    def get_var(self, var: Identifier):
        # Loop through all parent scopes (including current scope)
        # and return first matched variable or None if not found.

        scope = self
        while (value := scope.symbol_table.get(var.get_name(), None)) is None\
                and scope.parent_scope is not None:
            scope = scope.parent_scope
        return value


class GlobalScope(Scope):
    # Class for outer and global scopes
    # The only difference from normal Scope is that
    # it contains table of function definitions

    def __init__(self, parent_scope=None):
        super().__init__(parent_scope)

        self.fun_table = {}

    def add_fun_def(self, fun_def: FunctionDefinition):
        self.fun_table[fun_def.get_name()] = fun_def

    def get_fun_def(self, fun):
        if fun.get_name() in self.fun_table:
            return self.fun_table[fun.get_name()]
        if self.parent_scope is not None:
            return self.parent_scope.get_fun_def(fun)
        return None

    def try_to_find_var_and_set_it(self, var: Identifier, evaluated_value):
        # Current scope should not be the outer scope
        if self.parent_scope is None:
            raise Exception

        # We are allowed to change var in the global scope
        if var.get_name() in self.symbol_table:
            self.symbol_table[var.get_name()] = evaluated_value
            return True
        return False


class Environment:
    def __init__(self):
        self.outer_scope = GlobalScope()
        self._add_builtin_fun_defs()

        self.global_scope = GlobalScope(self.outer_scope)
        self.current_scope = self.global_scope
        self.call_stack = []
        self.fun_call_nesting = 0

    def set_var(self, var: Identifier, evaluated_value):
        self.current_scope.set_var(var, evaluated_value)

    def get_var(self, var: Identifier):
        return self.current_scope.get_var(var)

    def create_new_local_scope(self):
        # last scope is new_scope's parent scope
        new_scope = Scope(self.current_scope)

        # now new scope becomes current scope
        self.current_scope = new_scope

    def destroy_local_scope(self):
        # here we can free memory of last scope
        # but python's garbage collector does the work for us.
        self.current_scope = self.current_scope.parent_scope

    def create_new_fun_scope(self, parameters, arguments):
        # Create function scope
        # store in it function parameters
        # relations of scopes:
        # global scope <- function local scope

        parameters_scope = self._put_parameters_inside_new_scope(parameters, arguments)
        self.call_stack.append(self.current_scope)
        # self.call_stack.append(parameters_scope)
        self.current_scope = parameters_scope  # Scope(parameters_scope)
        self.fun_call_nesting += 1

    def _put_parameters_inside_new_scope(self, parameters, arguments):
        fun_scope = Scope(self.global_scope)

        for param, arg in zip(parameters, arguments):
            fun_scope.symbol_table[param.get_name()] = arg

        return fun_scope

    def destroy_fun_scope(self):
        # 'destroy' current function scope
        self.current_scope = None
        self.fun_call_nesting -= 1

        # restore scope before function call
        self.current_scope = self.call_stack.pop() \
            if self.call_stack else self.global_scope

    def add_fun_def(self, fun_def):
        self.global_scope.add_fun_def(fun_def)

    def get_fun_def(self, fun):
        return self.global_scope.get_fun_def(fun)

    def _add_builtin_fun_defs(self):
        for builtin in BuiltinFunctionCreator.get_builtin_fun_defs():
            self.outer_scope.fun_table[builtin.name] = FunctionDefinition(*builtin.get_wrapped_fun())


