from lark import Transformer, v_args
from ast_nodes import *

class CsarTransformer(Transformer):

    # --- PROGRAMMA ---
    def program(self, items):
        return ProgramNode(extern_decls=items[0], functions=items[1], main=items[2])

    def external_decl_list(self, items):
        return items

    def function_decl_list(self, items):
        return items

    # --- HELPER PER INDICI ---
    def _extract_params_and_ret(self, items, has_body=False):
        # La struttura di items è:
        # [ID, (Params?), Arrow, ReturnType, (Body?)]

        # L'ID è sempre il primo
        name = str(items[0])

        # Il ReturnType è sempre l'ultimo (o penultimo se c'è il Body)
        ret_index = -2 if has_body else -1
        ret_type = items[ret_index]

        # Body (se c'è) è l'ultimo
        body = items[-1] if has_body else None

        # I parametri dipendono dalla lunghezza.
        # Con Params: lunghezza 4 (extern) o 5 (functio)
        # Senza Params: lunghezza 3 (extern) o 4 (functio)

        expected_len_with_params = 5 if has_body else 4

        if len(items) == expected_len_with_params:
            params = items[1]
        else:
            params = []

        return name, params, ret_type, body

    # --- DICHIARAZIONI ---
    def external_decl(self, items):
        name, params, ret_type, _ = self._extract_params_and_ret(items, has_body=False)
        return ExternNode(name=name, params=params, return_type=str(ret_type))

    def function_decl(self, items):
        name, params, ret_type, body = self._extract_params_and_ret(items, has_body=True)
        return FunctionNode(name=name, params=params, return_type=str(ret_type), body=body)

    def main_block(self, items):
        return MainNode(body=items[0])

    def param_list(self, items):
        return items

    def param(self, items):
        return ParamNode(type_name=str(items[0]), name=str(items[1]))

    def arrow(self, items):
        return None # Ignoriamo la freccia nell'AST

    def return_type(self, items):
        return str(items[0])

    def type(self, items):
        return str(items[0])

    # --- BLOCCO ---
    def block(self, items):
        return BodyNode(var_decls=items[0], statements=items[1])

    def var_decl_list(self, items): return items
    def stmt_list(self, items): return items

    # --- ISTRUZIONI ---
    def stmt(self, items): return items[0]

    def var_decl_stmt(self, items):
        type_name = str(items[0])
        name = str(items[1])
        init_expr = items[2] if items[2] is not None else None
        return VarDeclNode(type_name=type_name, name=name, init_expr=init_expr)

    def optional_init(self, items):
        return items[0] if items else None

    def assign_stmt(self, items):
        return AssignNode(name=str(items[0]), expr=items[1])

    def if_stmt(self, items):
        condition = items[0]
        then_body = items[1]
        else_body = items[2] if len(items) > 2 else None
        return IfNode(condition=condition, then_body=then_body, else_body=else_body)

    def else_block(self, items): return items[0]

    def while_stmt(self, items):
        return WhileNode(condition=items[0], body=items[1])

    def return_stmt(self, items):
        expr = items[0] if items else None
        return ReturnNode(expr=expr)

    def proc_call_stmt(self, items):
        name = str(items[0])
        args = items[1] if len(items) > 1 else []
        return ProcCallNode(name=name, args=args)

    # --- ESPRESSIONI ---
    def var_expr(self, items):
        return VarExprNode(name=str(items[0]))

    def number_expr(self, items):
        return LiteralNode(value=int(items[0]), type_name='integer')

    def char_expr(self, items):
        raw_val = str(items[0])
        val = raw_val[1:-1]
        return LiteralNode(value=val, type_name='littera')

    def bool_true(self, items):
        return LiteralNode(value=True, type_name='boolianus')

    def bool_false(self, items):
        return LiteralNode(value=False, type_name='boolianus')

    def null_expr(self, items):
        return LiteralNode(value=None, type_name='nullum')

    def fun_call_expr(self, items):
        return items[0]

    def fun_call(self, items):
        name = str(items[0])
        args = items[1] if len(items) > 1 else []
        return FunCallNode(name=name, args=args)

    def args_list(self, items): return items

    def _binary_op(self, items):
        node = items[0]
        for i in range(1, len(items), 2):
            op = str(items[i])
            right = items[i+1]
            node = BinaryOpNode(left=node, op=op, right=right)
        return node

    logic_or = _binary_op
    logic_and = _binary_op
    comp_expr = _binary_op
    sum_expr = _binary_op
    term_expr = _binary_op

    def comp_op(self, items): return str(items[0])
    def add_op(self, items): return str(items[0])
    def mul_op(self, items): return str(items[0])