from llvmlite import ir
from ast_nodes import *

class CodeGenVisitor:

    # SETUP INIZIALE MODULO
    def __init__(self):
        self.module = ir.Module(name="csar_module")
        self.builder = None
        self.func_symtab = {} # {func_name: ir.Function}

        # Symbol Table per le variabili: {name: pointer_to_memory}
        self.var_symtab = {}

        # Tipi standard LLVM mappati sui tipi Csar
        self.types = {
            'integer': ir.IntType(32),
            'boolianus': ir.IntType(1), # 1 bit
            'littera': ir.IntType(8),   # 8 bit (char)
            'nullum': ir.VoidType()
        }

    # --- VISITOR PATTERN ---
    def visit(self, node):
        if node is None: return None
        method_name = f'visit_{node.__class__.__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method defined")

    # --- PROGRAMMA ---
    def visit_ProgramNode(self, node):
        # 1. Dichiara funzioni esterne
        for ext in node.extern_decls:
            self.visit(ext)

        # 2. Dichiara prototipi funzioni interne
        for func in node.functions:
            func_type = ir.FunctionType(
                self.types[func.return_type],
                [self.types[p.type_name] for p in func.params]
            )
            self.func_symtab[func.name] = ir.Function(self.module, func_type, name=func.name)

        # 3. Genera corpo funzioni
        for func in node.functions:
            self.visit(func)

        # 4. Genera Main
        self.visit(node.main)

    def visit_ExternNode(self, node):
        ret_type = self.types[node.return_type]
        arg_types = [self.types[p.type_name] for p in node.params]
        f_type = ir.FunctionType(ret_type, arg_types)
        self.func_symtab[node.name] = ir.Function(self.module, f_type, name=node.name)

    def visit_FunctionNode(self, node):
        func = self.func_symtab[node.name]

        # Crea il blocco di ingresso
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        previous_symtab = self.var_symtab.copy()
        self.var_symtab = {}

        # Allocazione argomenti
        for i, arg in enumerate(func.args):
            param_node = node.params[i]
            arg.name = param_node.name
            ptr = self.builder.alloca(self.types[param_node.type_name], name=param_node.name)
            self.builder.store(arg, ptr)
            self.var_symtab[param_node.name] = ptr

        # Genera corpo funzione
        self.visit(node.body)


        # Se il blocco finale non è terminato, aggiungiamo return
        if not self.builder.block.is_terminated:
            if node.return_type == 'nullum':
                self.builder.ret_void()
            elif node.return_type == 'integer':
                self.builder.ret(ir.Constant(self.types['integer'], 0))
            elif node.return_type == 'boolianus':
                self.builder.ret(ir.Constant(self.types['boolianus'], 0))
            elif node.return_type == 'littera':
                self.builder.ret(ir.Constant(self.types['littera'], 0))

        self.var_symtab = previous_symtab

    def visit_MainNode(self, node):
        f_type = ir.FunctionType(ir.IntType(32), [])
        func = ir.Function(self.module, f_type, name="main")
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        self.var_symtab = {}
        self.visit(node.body)

        # Return 0 standard per il main
        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def visit_BodyNode(self, node):
        for decl in node.var_decls:
            self.visit(decl)
        for stmt in node.statements:
            self.visit(stmt)

    # --- ISTRUZIONI ---
    def visit_VarDeclNode(self, node):
        typ = self.types[node.type_name]
        ptr = self.builder.alloca(typ, name=node.name)
        self.var_symtab[node.name] = ptr

        if node.init_expr:
            val = self.visit(node.init_expr)
            self.builder.store(val, ptr)
        else:
            self.builder.store(ir.Constant(typ, 0), ptr)

    def visit_AssignNode(self, node):
        val = self.visit(node.expr)
        ptr = self.var_symtab[node.name]
        self.builder.store(val, ptr)

    def visit_IfNode(self, node):
        then_block = self.builder.append_basic_block(name="then")
        else_block = self.builder.append_basic_block(name="else")
        merge_block = self.builder.append_basic_block(name="endif")

        cond_val = self.visit(node.condition)
        self.builder.cbranch(cond_val, then_block, else_block)

        # THEN
        self.builder.position_at_start(then_block)
        self.visit(node.then_body)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        # ELSE
        self.builder.position_at_start(else_block)
        if node.else_body:
            self.visit(node.else_body)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        # MERGE
        self.builder.position_at_start(merge_block)

    def visit_WhileNode(self, node):
        cond_block = self.builder.append_basic_block(name="while_cond")
        body_block = self.builder.append_basic_block(name="while_body")
        end_block = self.builder.append_basic_block(name="while_end")

        self.builder.branch(cond_block)

        # COND
        self.builder.position_at_start(cond_block)
        cond_val = self.visit(node.condition)
        self.builder.cbranch(cond_val, body_block, end_block)

        # BODY
        self.builder.position_at_start(body_block)
        self.visit(node.body)
        self.builder.branch(cond_block)

        # END
        self.builder.position_at_start(end_block)

    def visit_ReturnNode(self, node):
        if node.expr:
            val = self.visit(node.expr)
            self.builder.ret(val)
        else:
            self.builder.ret_void()

    def visit_ProcCallNode(self, node):
        func = self.func_symtab[node.name]
        #Prepara gli argomenti
        args = [self.visit(arg) for arg in node.args]
        # call i32 @somma(i32 6, i32 %x)
        self.builder.call(func, args)

    # --- ESPRESSIONI ---
    def visit_BinaryOpNode(self, node):
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        op = node.op

        if op == '+': return self.builder.add(lhs, rhs, name="addtmp")
        if op == '-': return self.builder.sub(lhs, rhs, name="subtmp")
        if op == '*': return self.builder.mul(lhs, rhs, name="multmp")
        if op == '/': return self.builder.sdiv(lhs, rhs, name="divtmp")

        if op == '&&': return self.builder.and_(lhs, rhs, name="andtmp")
        if op == '||': return self.builder.or_(lhs, rhs, name="ortmp")

        # --- FIX: Mappa simboli per icmp_signed ---
        # llvmlite vuole i simboli '<', '>', '==', non 'slt', 'sgt', 'eq'
        cmp_map = {
            '::': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>='
        }

        if op in cmp_map:
            # Genera: %cmptmp = icmp eq i32 %lhs, %rhs
            return self.builder.icmp_signed(cmp_map[op], lhs, rhs, name="cmptmp")


    def visit_LiteralNode(self, node):
        val = node.value
        typ = self.types[node.type_name]

        if node.type_name == 'integer':
            return ir.Constant(typ, val)
        elif node.type_name == 'boolianus':
            return ir.Constant(typ, 1 if val else 0)
        elif node.type_name == 'littera':
            # val è stringa convertire in ASCII ord
            return ir.Constant(typ, ord(val) if isinstance(val, str) else val)
        elif node.type_name == 'nullum':
            return ir.Constant(typ, None)

    def visit_VarExprNode(self, node):
        #recupera il puntatore alla variabile
        ptr = self.var_symtab[node.name]
        # Genera: %val = load i32, i32* %x
        return self.builder.load(ptr, name=node.name)

    def visit_FunCallNode(self, node):
        func = self.func_symtab[node.name]
        args = [self.visit(arg) for arg in node.args]
        return self.builder.call(func, args, name="calltmp")