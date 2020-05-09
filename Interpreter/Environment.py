# How environment works in fml:
#
# Environment = Outer scope + Global scope + Call stack.
#
# Outer scope is at lowest level.
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


from Parser.Objects.Identifier import Identifier


class Scope:
    def __init__(self, parent_scope=None):
        self.parent_scope = parent_scope
        self.symbol_table = {}

    def add_var(self, var: Identifier, evaluated_value):
        # To add variable to a scope means that
        # the variable got assigned.
        # First check if the variable exists in this scope, if it does, reassign it.
        # If it doesn't, add it to the symbol table of this scope.

        self.symbol_table[var.get_name()] = evaluated_value

    def get_var(self, var: Identifier):
        # Loop through all parent scopes (including current scope)
        # and return first matched variable or None if not found.

        scope = self
        while (value := scope.symbol_table.get(var.get_name(), None)) is None\
                and scope.parent_scope is not None:
            scope = scope.parent_scope
        return value


class Environment:
    def __init__(self):
        self.outer_scope = Scope()
        self.global_scope = Scope(self.outer_scope)
        self.current_scope = self.global_scope
        self.call_stack = []
        self.fun_table = {}
        self.fun_call_nesting = 0

    def add_var(self, var: Identifier, evaluated_value):
        self.current_scope.add_var(var, evaluated_value)

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

    def create_new_fun_scope(self, parameters):
        # Create 2 scopes
        # first one only contains function parameters
        # and is created for convenience
        # second scope represents scope inside function
        # relations of scopes:
        # global scope <- parameters scope <- function local scope

        parameters_scope = self._put_parameters_inside_new_scope(parameters)
        self.call_stack.append(self.current_scope)
        self.call_stack.append(parameters_scope)
        self.current_scope = Scope(parameters_scope)
        self.fun_call_nesting += 1

    def _put_parameters_inside_new_scope(self, parameters):
        fun_scope = Scope(self.global_scope)
        for param in parameters:
            # todo
            fun_scope.add_var(param, None)
        return fun_scope

    def destroy_fun_scope(self):
        # there are 2 scopes that are related to function scope:
        # current scope and last scope on call stack
        # "destroy" them
        self.current_scope = None
        self.call_stack.pop()
        self.fun_call_nesting -= 1

        # restore scope before function call
        self.current_scope = self.call_stack.pop() \
            if self.call_stack else self.global_scope
