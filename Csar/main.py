import sys
import os
from lark import Lark
from transformer import CsarTransformer
from codegen import CodeGenVisitor
# --- IMPORT SEMANTICA ---
from semantic_visitor import SemanticVisitor, SemanticError

# Proviamo a importare l'ottimizzatore
try:
    from llvm_optimizer import optimize_ir
    OPTIMIZER_AVAILABLE = True
except ImportError:
    OPTIMIZER_AVAILABLE = False
    print("⚠️  Nota: 'llvm_optimizer.py' non trovato. Ottimizzazioni disabilitate.")

def compile_file(filename):
    # 1. Caricamento Grammatica
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        grammar_path = os.path.join(base_path, "grammar.lark")
        with open(grammar_path, "r") as f: grammar = f.read()
        with open(filename, "r") as f: code = f.read()
    except FileNotFoundError as e:
        print(f"ERRORE: Non trovo il file '{e.filename}'")
        return

    print(f"Compilando {filename}...")

    # 2. Parsing (Crea Parse Tree)
    try:
        parser = Lark(grammar, start="program", parser="lalr")
        tree = parser.parse(code)
    except Exception as e:
        print(f"Errore Sintattico:\n{e}")
        return

    # 3. Trasformazione (Crea AST)
    transformer = CsarTransformer()
    ast = transformer.transform(tree)

    # --- 3b. ANALISI SEMANTICA (Type Checking & Scope) ---
    semantic = SemanticVisitor()
    try:
        semantic.visit(ast)
    except SemanticError as e:
        print(f"⛔ Errore Semantico: {e}")
        return  # Si ferma qui se i tipi sono sbagliati!
    print("Analisi Semantica: OK ✅")

    # 4. CodeGen (Backend)
    codegen = CodeGenVisitor()
    try:
        codegen.visit(ast)
    except Exception as e:
        print(f"Errore CodeGen: {e}")
        return

    raw_llvm_code = str(codegen.module)
    final_code = raw_llvm_code

    # 5. Ottimizzazione (Middle-end)
    if OPTIMIZER_AVAILABLE:
        print("--- OTTIMIZZAZIONE LLVM (Pass Manager) ---")
        try:
            optimized_code = optimize_ir(raw_llvm_code)
            len_raw = len(raw_llvm_code)
            len_opt = len(optimized_code)
            print(f"Riduzione: {len_raw} -> {len_opt} bytes ({len_raw - len_opt} risparmiati)")
            final_code = optimized_code
        except Exception as e:
            print(f"Errore Ottimizzatore: {e}")

    # 6. Salvataggio
    out_filename = filename.replace(".csar", ".ll")
    with open(out_filename, "w") as f:
        f.write(final_code)
    print(f"\nSalvataggio: {out_filename} ✅")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <file.csar>")
    else:
        compile_file(sys.argv[1])