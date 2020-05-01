from Interpreter.Ast import NodeVisitor
from Interpreter.TextTreeStructure import TextTreeStructure


class AstDumper(NodeVisitor, TextTreeStructure):
    def visit_Program(self, program):
        for object in program.objects:
            self.add_child(lambda object=object: self.visit(object), object)

    def visit_FunctionDefinition(self, fun_def):
        for parameter in fun_def.parameter_list:
            self.add_child(lambda parameter=parameter: self.visit(parameter), parameter)
        self.add_child(lambda: self.visit(fun_def.statement), fun_def.statement)

    def visit_ReturnStatement(self, ret_statement):
        self.add_child(lambda: self.visit(ret_statement.expression), ret_statement.expression)

    def visit_ForLoop(self, for_loop):
        self.add_child(lambda: self.visit(for_loop.iterator), for_loop.iterator)
        self.add_child(lambda: self.visit(for_loop.iterable), for_loop.iterable)
        self.add_child(lambda: self.visit(for_loop.statement), for_loop.statement)

    def visit_WhileLoop(self, while_loop):
        self.add_child(lambda: self.visit(while_loop.condition_expression),
                       while_loop.condition_expression)
        self.add_child(lambda: self.visit(while_loop.statement),
                       while_loop.statement)

    def visit_DoWhileLoop(self, do_while_loop):
        self.add_child(lambda: self.visit(do_while_loop.statement),
                       do_while_loop.statement)
        self.add_child(lambda: self.visit(do_while_loop.condition_expression),
                       do_while_loop.condition_expression)

    def visit_CompoundStatement(self, comp_statement):
        for statement in comp_statement.statement_list:
            self.add_child(lambda statement=statement: self.visit(statement), statement)

    def visit_IfStatement(self, if_statement):
        self.add_child(lambda: self.visit(if_statement.condition_expression),
                       if_statement.condition_expression)
        self.add_child(lambda: self.visit(if_statement.statement), if_statement.statement)
        if if_statement.else_statement is not None:
            self.add_child(lambda: self.visit(if_statement.else_statement),
                           if_statement.else_statement)

    def visit_BinaryOperator(self, bin_op):
        self.add_child(lambda: self.visit(bin_op.lvalue), bin_op.lvalue)
        self.add_child(lambda: self.visit(bin_op.rvalue), bin_op.rvalue)

    def visit_UnaryOperator(self, unary_op):
        self.add_child(lambda: self.visit(unary_op.rvalue), unary_op.rvalue)

    def visit_FunctionCall(self, fun_call):
        for argument in fun_call.argument_list:
            self.add_child(lambda argument=argument: self.visit(argument), argument)

    def visit_MatrixSubscripting(self, mtrx_subs):
        row_idx_label = 'Row '
        if mtrx_subs.row_index is not None and mtrx_subs.column_index is None:
            row_idx_label = ''
        if mtrx_subs.row_index is not None:
            self.add_child(lambda: self.visit(mtrx_subs.row_index),
                           f'{row_idx_label}{mtrx_subs.row_index}')
        if mtrx_subs.column_index is not None:
            self.add_child(lambda: self.visit(mtrx_subs.column_index),
                           f'Column {mtrx_subs.column_index}')

    def visit_MatrixIndex(self, idx):
        if not idx.is_colon:
            self.add_child(lambda: self.visit(idx.expression), idx.expression)
        else:
            self.add_child(lambda: None, 'Colon')

    def visit_Matrix(self, matrix):
        pass

    def visit_Identifier(self, id):
        pass

    def visit_Scalar(self, scalar):
        pass

    def visit_EmptyStatement(self, empty_statement):
        pass

    def visit_String(self, string):
        pass






