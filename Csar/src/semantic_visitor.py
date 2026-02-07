from ast_nodes import *

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.global_scope = {}  # {name: (type, 'global')}
        self.local_scope = None # {name: (type, 'local')} o None se siamo fuori funzione
        self.current_function_return_type = None

    def enter_function(self, function_name, return_type):
        self.local_scope = {}
        self.current_function_return_type = return_type

    def exit_function(self):
        self.local_scope = None
        self.current_function_return_type = None

    def define(self, name, type_name, kind):
        """Definisce un simbolo controllando lo Shadowing."""
        if kind == 'local':
            # 1. Controllo Shadowing (vietato nascondere globali)
            if name in self.global_scope:
                raise SemanticError(f"Errore Shadowing: La variabile locale '{name}' ha il nome di una globale.")
            # 2. Controllo duplicati locali
            if name in self.local_scope:
                raise SemanticError(f"Errore: Variabile locale '{name}' gia' dichiarata.")
            self.local_scope[name] = (type_name, 'local')

        elif kind == 'global':
            if name in self.global_scope:
                raise SemanticError(f"Errore: Simbolo globale '{name}' gia' dichiarato.")
            self.global_scope[name] = (type_name, 'global')

    def lookup(self, name):
        """Cerca prima nel locale, poi nel globale."""
        if self.local_scope is not None and name in self.local_scope:
            return self.local_scope[name][0]
        if name in self.global_scope:
            return self.global_scope[name][0]
        return None

class SemanticVisitor:

    # --- CREAZIONE SYMBOL TABLE ---
    def __init__(self):
        self.symbol_table = SymbolTable()
        # Set per tracciare le variabili inizializzate nella funzione corrente
        self.initialized_vars = set()

    # --- VISITOR PATTERN CON RIFLESSIONE ---
    def visit(self, node):
        if node is None: return None
        method_name = f'visit_{node.__class__.__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"Nessun metodo visit_{node.__class__.__name__} definito.")

    # --- PROGRAMMA E FUNZIONI ---
    def visit_ProgramNode(self, node):
        # 1. Registra Globali (Extern)
        for ext in node.extern_decls:
            self.symbol_table.define(ext.name, ext.return_type, 'global')

        # 2. Registra Funzioni (per ricorsione)
        for func in node.functions:
            self.symbol_table.define(func.name, func.return_type, 'global')

        # 3. Visita Funzioni RICORSIONE
        for func in node.functions:
            self.visit(func)

        # 4. Visita Main
        self.visit(node.main)

    def visit_FunctionNode(self, node):
        self.symbol_table.enter_function(node.name, node.return_type)

        # Reset tracking variabili inizializzate
        self.initialized_vars = set()

        for param in node.params:
            self.symbol_table.define(param.name, param.type_name, 'local')
            # I parametri sono SEMPRE inizializzati perché arrivano da fuori
            self.initialized_vars.add(param.name)

        self.visit(node.body)
        self.symbol_table.exit_function()
        self.initialized_vars = set() # Pulizia finale

    def visit_MainNode(self, node):
        self.symbol_table.enter_function('principalis', 'nullum')

        # Reset tracking variabili inizializzate
        self.initialized_vars = set()

        self.visit(node.body)
        self.symbol_table.exit_function()
        self.initialized_vars = set() # Pulizia finale

    def visit_BodyNode(self, node):
        for decl in node.var_decls:
            self.visit(decl)
        for stmt in node.statements:
            self.visit(stmt)

    # --- ISTRUZIONI ---

    def visit_VarDeclNode(self, node):
        if node.init_expr:
            expr_type = self.visit(node.init_expr)
            if expr_type != node.type_name:
                raise SemanticError(f"Errore Tipo: '{node.name}' e' {node.type_name}, init con {expr_type}")

            # Se c'è un'espressione di init, la variabile è inizializzata!
            self.initialized_vars.add(node.name)

        scope = 'local' if self.symbol_table.local_scope is not None else 'global'
        self.symbol_table.define(node.name, node.type_name, scope)

    def visit_AssignNode(self, node):
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variabile '{node.name}' non dichiarata.")

        expr_type = self.visit(node.expr)
        if var_type != expr_type:
            raise SemanticError(f"Errore Assegnamento: '{node.name}' ({var_type}) = {expr_type}")

        # Assegnazione avvenuta -> Variabile inizializzata!
        self.initialized_vars.add(node.name)

    def visit_IfNode(self, node):
        if self.visit(node.condition) != 'boolianus':
            raise SemanticError("Errore 'si': Condizione non booleana.")
        self.visit(node.then_body)
        if node.else_body: self.visit(node.else_body)

    def visit_WhileNode(self, node):
        if self.visit(node.condition) != 'boolianus':
            raise SemanticError("Errore 'dom': Condizione non booleana.")
        self.visit(node.body)

    def visit_ReturnNode(self, node):
        expected = self.symbol_table.current_function_return_type
        found = self.visit(node.expr) if node.expr else 'nullum'
        if found != expected:
            raise SemanticError(f"Errore Return: Atteso {expected}, trovato {found}")

    def visit_ProcCallNode(self, node):
        if not self.symbol_table.lookup(node.name):
            raise SemanticError(f"Procedura '{node.name}' non definita.")
        for arg in node.args: self.visit(arg)

    # --- ESPRESSIONI ---
    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op

        if op in ['+', '-', '*', '/']: # Aritmetica (solo integer)

            if op == '/' and hasattr(node.right, 'value') and node.right.value == 0:
                 raise SemanticError("Errore Matematico: Divisione per zero!")

            if left == 'integer' and right == 'integer': return 'integer'
            raise SemanticError(f"Errore '{op}': Richiede integer, trovati {left}, {right}")

        if op in ['&&', '||']: # Logica (solo boolianus)
            if left == 'boolianus' and right == 'boolianus': return 'boolianus'
            raise SemanticError(f"Errore '{op}': Richiede boolianus.")

        if op in ['::', '!=', '<', '>', '<=', '>=']: # Confronto
            if left == right: return 'boolianus'
            raise SemanticError(f"Errore '{op}': Tipi diversi {left}, {right}")

    # -- NODI FOGLIA --

    # -- VALORE LETTERALE (Numeri, Stringhe, Bool)
    def visit_LiteralNode(self, node):
        return node.type_name

    # -- USO VARIABILE (Lettura)
    def visit_VarExprNode(self, node):
        t = self.symbol_table.lookup(node.name)
        if not t: raise SemanticError(f"Variabile '{node.name}' non dichiarata prima dell'uso.")

        # --- CONTROLLO USO VARIABILE NON INIZIALIZZATA ---
        # Se siamo in una funzione (local scope) e la variabile è locale
        if self.symbol_table.local_scope and node.name in self.symbol_table.local_scope:
            if node.name not in self.initialized_vars:
                raise SemanticError(f"PERICOLO: Variabile locale '{node.name}' usata prima di essere inizializzata!")
        # -------------------------------------------------

        return t

    # -- CHIAMATA FUNZIONE
    def visit_FunCallNode(self, node):
        t = self.symbol_table.lookup(node.name)
        if not t: raise SemanticError(f"Funzione '{node.name}' sconosciuta.")
        for arg in node.args: self.visit(arg)
        return t