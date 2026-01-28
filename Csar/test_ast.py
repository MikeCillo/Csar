from lark import Lark
from transformer import CsarTransformer
from ast_nodes import *
import sys

# 1. Carichiamo la grammatica
try:
    with open("grammar.lark", "r") as f:
        grammar = f.read()
except FileNotFoundError:
    print("ERRORE: Non trovo il file 'grammar.lark'. Assicurati di essere nella cartella giusta!")
    sys.exit(1)

# Crea il parser Lark
parser = Lark(grammar, start="program", parser="lalr")

# 2. Codice di prova Csar (con le nuove regole: littera, dichiarazioni in testa, ecc.)
code = """
// Dichiarazione esterna
externus functio scribe_char(littera c) -> nullum .

// Funzione di prova
functio calcola(integer n) -> integer {
    // Dichiarazioni prima delle istruzioni (regola C89)
    integer ris : n .
    
    // Istruzioni
    si (n > 0) {
        ris : n + 1 .
    } aliter {
        ris : 0 .
    }
    redde ris .
}

principalis {
    // Dichiarazioni
    integer x : 10 .
    integer y .

    // Istruzioni
    y : calcola(x) .
    scribe_char('A') .
}
"""

print("-" * 50)
print("1. TEST PARSING (Lark)")
print("-" * 50)

try:
    tree = parser.parse(code)
    print("SUCCESS: Il codice è stato parsato correttamente!")
    print(tree.pretty()) # Stampa l'albero grezzo (utile per debug)
except Exception as e:
    print(f"ERROR: Errore di parsing:\n{e}")
    sys.exit(1)

print("\n" + "-" * 50)
print("2. TEST TRANSFORMER (Generazione AST)")
print("-" * 50)

try:
    transformer = CsarTransformer()
    ast_root = transformer.transform(tree)

    print(f"SUCCESS: AST Generato -> {ast_root}")
    print(f"Tipo Radice: {type(ast_root)}")

    # Verifica veloce dei contenuti
    if isinstance(ast_root, ProgramNode):
        print(f"\nVerifica Contenuti:")
        print(f" - Funzioni trovate: {len(ast_root.functions)}")
        if len(ast_root.functions) > 0:
            print(f" - Prima funzione: '{ast_root.functions[0].name}' (Ritorna: {ast_root.functions[0].return_type})")
        print(f" - Main presente: {'Sì' if ast_root.main else 'No'}")

except Exception as e:
    print(f"ERROR: Errore durante la trasformazione in AST:\n{e}")
    sys.exit(1)