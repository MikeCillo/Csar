# File: ast_nodes.py

from dataclasses import dataclass
from typing import List, Optional, Union

# --- CLASSE BASE ---
class Node:
    pass

# --- STRUTTURA DEL PROGRAMMA ---

@dataclass
class ProgramNode(Node):
    extern_decls: List['ExternNode']
    functions: List['FunctionNode']
    main: 'MainNode'

@dataclass
class ExternNode(Node):
    name: str
    params: List['ParamNode']
    return_type: str

@dataclass
class FunctionNode(Node):
    name: str
    params: List['ParamNode']
    return_type: str
    body: 'BodyNode'

@dataclass
class MainNode(Node):
    body: 'BodyNode'

@dataclass
class ParamNode(Node):
    type_name: str
    name: str

# --- BLOCCO E BODY ---

@dataclass
class BodyNode(Node):
    # Secondo la regola C89, separiamo dichiarazioni e statement
    var_decls: List['VarDeclNode']
    statements: List[Node]

# --- ISTRUZIONI (Statements) ---

@dataclass
class VarDeclNode(Node):
    type_name: str
    name: str
    init_expr: Optional[Node]  # Può essere None se non inizializzata

@dataclass
class AssignNode(Node):
    name: str
    expr: Node

@dataclass
class IfNode(Node):
    condition: Node
    then_body: 'BodyNode'
    else_body: Optional['BodyNode']

@dataclass
class WhileNode(Node):
    condition: Node
    body: 'BodyNode'

@dataclass
class ReturnNode(Node):
    expr: Optional[Node]

@dataclass
class ProcCallNode(Node):
    name: str
    args: List[Node]

# --- ESPRESSIONI (Expressions) ---

@dataclass
class BinaryOpNode(Node):
    left: Node
    op: str  # +, -, *, /, ::, <, && ...
    right: Node

@dataclass
class FunCallNode(Node):
    name: str
    args: List[Node]

@dataclass
class LiteralNode(Node):
    # value può essere int, str (per i char), o bool
    value: Union[int, str, bool]
    type_name: str # 'integer', 'littera', 'boolianus', 'nullum'

@dataclass
class VarExprNode(Node):
    name: str