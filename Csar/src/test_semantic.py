from lark import Lark
from transformer import CsarTransformer
from semantic_visitor import SemanticVisitor, SemanticError
import sys

# 1. SETUP
with open("grammar.lark", "r") as f: grammar = f.read()
parser = Lark(grammar, start="program", parser="lalr")
transformer = CsarTransformer()

def check_code(code_str, test_name):
    print(f"\n--- TEST: {test_name} ---")
    try:
        tree = parser.parse(code_str)
        ast = transformer.transform(tree)
        visitor = SemanticVisitor()
        visitor.visit(ast)
        print("✅ SUCCESS: Codice semanticamente corretto.")
    except SemanticError as e:
        print(f"❌ ERRORE SEMANTICO RILEVATO: {e}")
    except Exception as e:
        print(f"⚠️ ERRORE GENERICO: {e}")

# --- TEST 1: CODICE CORRETTO ---
code_ok = """
externus functio print(integer x) -> nullum .
functio somma(integer a, integer b) -> integer {
    redde a + b .
}
principalis {
    integer x : 10 .
    integer y : somma(x, 5) .
    si (y > 10) { 
        print(y) . 
    }
}
"""
check_code(code_ok, "Codice Valido")

# --- TEST 2: ERRORE DI TIPO (Integer + Littera) ---
code_type_err = """
principalis {
    integer x : 10 + 'A' .  // Errore!
}
"""
check_code(code_type_err, "Errore di Tipo (Int + Char)")

# --- TEST 3: VARIABILE NON DICHIARATA ---
code_scope_err = """
principalis {
    x : 5 . // x non dichiarato
}
"""
check_code(code_scope_err, "Variabile Non Dichiarata")

# --- TEST 4: SHADOWING (Vietato) ---
code_shadow = """
functio test() -> nullum { 
    integer global_var . // Errore se global_var esiste fuori
    redde . 
}
principalis { integer global_var . }
"""
# Nota: il test shadowing qui è locale, per testarlo bene servirebbe una var globale reale.
# Simuliamo shadowing reale:
code_shadow_real = """
functio pippo() -> nullum { redde . }
principalis {
    integer pippo . // Errore: nasconde la funzione
}
"""
check_code(code_shadow_real, "Shadowing Vietato")