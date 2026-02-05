import os
import subprocess
import sys

# --- CONFIGURAZIONE ---

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Determina le cartelle in base a dove si trova questo script
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPILER_PATH = os.path.join(ROOT_DIR, "src", "main.py")  # <--- Punta a src/main.py
TESTS_DIR = os.path.join(ROOT_DIR, "tests")

def run_single_test(file_path, expect_fail=False):
    """
    Esegue il compilatore su un singolo file e verifica il risultato.
    """
    filename = os.path.basename(file_path)
    print(f"Testing {filename}...", end=" ")

    # Costruisce il comando: python src/main.py percorso/del/test.csar
    cmd = [sys.executable, COMPILER_PATH, file_path]

    try:
        # Esegue il processo catturando l'output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # Un test fallisce se il return code != 0 OPPURE se c'è "Errore" nell'output
        output = result.stdout + result.stderr
        has_error = result.returncode != 0 or "Errore" in output or "Exception" in output or "Traceback" in output

        # Logica di verifica
        if expect_fail:
            # Caso INVALID: Deve fallire per passare il test
            if has_error:
                print(f"{GREEN}PASS (Errore rilevato correttamente){RESET}")
                return True
            else:
                print(f"{RED}FAIL (Doveva fallire ma ha compilato con successo){RESET}")
                return False
        else:
            # Caso VALID: Non deve avere errori
            if not has_error:
                print(f"{GREEN}PASS{RESET}")
                return True
            else:
                print(f"{RED}FAIL (Errore imprevisto){RESET}")
                # Stampa le ultime righe dell'errore per debugging
                print(f"   >>> {output.strip().splitlines()[-1]}")
                return False

    except Exception as e:
        print(f"{RED}CRASH (Impossibile eseguire il compilatore){RESET}")
        print(e)
        return False

def run_suite():
    # Verifica che il compilatore esista
    if not os.path.exists(COMPILER_PATH):
        print(f"{RED}ERRORE CRITICO: Non trovo il compilatore in: {COMPILER_PATH}{RESET}")
        print("Assicurati che main.py sia dentro la cartella 'src'.")
        return

    print(f"{BLUE}=== AVVIO SUITE DI TEST CSAR ==={RESET}")
    print(f"Compilatore: {COMPILER_PATH}\n")

    passed = 0
    total = 0

    # 1. CERCA I TEST VALIDI (che devono funzionare)
    # Cerca nella cartella tests/valid
    valid_path = os.path.join(TESTS_DIR, "valid")
    if os.path.exists(valid_path):
        print(f"--- {BLUE}Test Validi (Devono compilare){RESET} ---")
        for f in sorted(os.listdir(valid_path)):
            if f.endswith(".csar"):
                full_path = os.path.join(valid_path, f)
                if run_single_test(full_path, expect_fail=False):
                    passed += 1
                total += 1
    else:
        print(f"{RED}Attenzione: Cartella '{valid_path}' non trovata.{RESET}")

    # 2. CERCA I TEST INVALIDI (che devono dare errore)
    # Cerca ricorsivamente in tests/invalid (gestisce semantic, syntax, ecc.)
    invalid_path = os.path.join(TESTS_DIR, "vulnerabilities")
    if os.path.exists(invalid_path):
        print(f"\n--- {BLUE}Test Invalidi (Devono dare errore){RESET} ---")
        for root, dirs, files in os.walk(invalid_path):
            for f in sorted(files):
                if f.endswith(".csar"):
                    full_path = os.path.join(root, f)
                    # Qui ci aspettiamo che fallisca (expect_fail=True)
                    if run_single_test(full_path, expect_fail=True):
                        passed += 1
                    total += 1
    else:
        print(f"{RED}Attenzione: Cartella '{invalid_path}' non trovata.{RESET}")

    # RIEPILOGO
    print("\n========================================")
    if total > 0:
        color = GREEN if passed == total else RED
        print(f"RISULTATO FINALE: {color}{passed}/{total} test superati.{RESET}")
    else:
        print("Nessun test trovato (.csar) nelle cartelle.")

if __name__ == "__main__":
    run_suite()


