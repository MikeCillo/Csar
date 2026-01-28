from lark import Transformer, v_args
from ast_nodes import *

class CsarTransformer(Transformer):

    # --- PROGRAMMA ---
    def program(self, items):
        # items[0]: lista extern, items[1]: lista funzioni, items[2]: main
        return ProgramNode(extern_decls=items[0], functions=items[1], main=items[2])

    def external_decl_list(self, items):
        return items

    def function_decl_list(self, items):
        return items


    # --- DICHIARAZIONI

    def external_decl(self, items):
        # Struttura: [ID, (Params?), Arrow, ReturnType]
        name = str(items[0])

        # Caso A: Ci sono i parametri (Lunghezza 4)
        if len(items) == 4:
            params = items[1]
            ret_type = items[3]

        # Caso B: NON ci sono parametri (Lunghezza 3)
        else:
            params = []
            ret_type = items[2]

        return ExternNode(name=name, params=params, return_type=str(ret_type))

    def function_decl(self, items):
        # Struttura: [ID, (Params?), Arrow, ReturnType, Body]

        name = str(items[0])

        # Caso A Lunghezza 5
        if len(items) == 5:
            params = items[1]
            ret_type = items[3]
            body = items[4]

        # Caso B Lunghezza 4
        else:
            params = []
            ret_type = items[2]
            body = items[3]

        return FunctionNode(name=name, params=params, return_type=str(ret_type), body=body)

    def main_block(self, items):
        # items[0] è il blocco del main
        return MainNode(body=items[0])

    # --- PARAMETRI E TIPI ---
    def param_list(self, items):
        return items

    def param(self, items):
        return ParamNode(type_name=str(items[0]), name=str(items[1]))

    def arrow(self, items):
        return None # non serve nell'AST

    def return_type(self, items):
        return str(items[0])

    def type(self, items):
        return str(items[0])

    # --- BLOCCO ---
    def block(self, items):
        # items[0]: lista dichiarazioni variabili
        # items[1]: lista istruzioni
        return BodyNode(var_decls=items[0], statements=items[1])

    def var_decl_list(self, items): return items
    def stmt_list(self, items): return items

    # --- ISTRUZIONI ---
    def stmt(self, items): return items[0]

    def var_decl_stmt(self, items):
        # items: [Type, ID, OptionalInit, "."]
        type_name = str(items[0])
        name = str(items[1])
        # items[2] inizializzazione opzionale Value/None
        init_expr = items[2] if items[2] is not None else None
        return VarDeclNode(type_name=type_name, name=name, init_expr=init_expr)

    def optional_init(self, items):
        # Se c'è l'inizializzazione, restituisce il valore. Altrimenti None.
        return items[0] if items else None

    def assign_stmt(self, items):
        return AssignNode(name=str(items[0]), expr=items[1])

    def if_stmt(self, items):
        condition = items[0]
        then_body = items[1]
        # Se la lista è lunga più di 2, c'è anche l'ELSE
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

    # --- ESPRESSIONI (Literals e Variabili) ---
    def var_expr(self, items):
        return VarExprNode(name=str(items[0]))

    def number_expr(self, items):
        # Conversione fondamentale: stringa -> intero
        return LiteralNode(value=int(items[0]), type_name='integer')

    def char_expr(self, items):
        raw_val = str(items[0]) # Es: "'A'"
        val = raw_val[1:-1]     # Rimuove gli apici: "A"
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

    # --- LOGICA OPERATORI (Ciclo per associatività a sinistra) ---
    def _binary_op(self, items):
        node = items[0]
        # Salta a passi di 2: prende Operatore e Operando Destro
        for i in range(1, len(items), 2):
            op = str(items[i])
            right = items[i+1]
            node = BinaryOpNode(left=node, op=op, right=right)
        return node

    # Mappiamo tutte le espressioni binarie sullo stesso metodo
    logic_or = _binary_op
    logic_and = _binary_op
    comp_expr = _binary_op
    sum_expr = _binary_op
    term_expr = _binary_op

    def comp_op(self, items): return str(items[0])
    def add_op(self, items): return str(items[0])
    def mul_op(self, items): return str(items[0])