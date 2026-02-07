Csar Compiler
Csar è un linguaggio di programmazione procedurale imperativo, fortemente tipizzato, ispirato alla sintassi latina e basato sulla struttura del C. Questo progetto implementa un compilatore completo (Frontend, Middle-end, Backend) scritto in Python, che traduce il codice sorgente Csar in LLVM IR.





PER ESEGUIRE I TEST python3 run_tests.py

PER ESEGUIRE LA CALCOLATRICE

COMPILARE
python3 src/main.py tests/calcolatrice.csar

LINK
clang tests/calcolatrice.ll tests/runtime.c -o calcolatrice

ESEGUIRE
./calcolatrice



📋 Requisiti di Sistema
Per eseguire il compilatore e generare gli eseguibili finali, sono necessari i seguenti strumenti:

1. Python

Versione richiesta: Python 3.8+

2. Librerie Python (Dipendenze)

Il compilatore richiede le seguenti librerie, installabili via pip:

lark: Per il Lexer e il Parser.

llvmlite: Per la generazione e l'ottimizzazione del codice intermedio LLVM.

3. Clang (Backend & Linker)

Poiché il compilatore genera codice intermedio (.ll), è necessario Clang per compilare l'IR in codice macchina e linkarlo con le librerie di sistema (necessario per funzioni come printf).

Windows: Installare LLVM (che include Clang).

Linux: sudo apt install clang

macOS: xcode-select --install

🚀 Installazione
Clonare o scaricare la cartella del progetto.

Installare le dipendenze Python eseguendo:

Bash
pip install lark llvmlite
(Opzionale ma consigliato) Utilizzare un Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
pip install lark llvmlite
🛠️ Guida alla Compilazione
Il processo di compilazione avviene in due fasi:

Traduzione: Da Csar (.csar) a LLVM IR (.ll) usando il nostro compilatore main.py.

Linking: Da LLVM IR (.ll) a Eseguibile (.exe) usando clang.

Passo 1: Generare il Codice Intermedio

Eseguire lo script main.py passando il file sorgente come argomento:

Bash
python main.py nome_file.csar
Se la compilazione ha successo, verrà creato un file nome_file.ll nella stessa directory. Il compilatore applicherà automaticamente le ottimizzazioni (O3) se il modulo llvm_optimizer.py è presente.

Passo 2: Creare l'Eseguibile

Utilizzare Clang per compilare il file .ll generato:

Su Linux / macOS:

Bash
clang nome_file.ll -o programma_eseguibile
./programma_eseguibile
Su Windows:

PowerShell
clang nome_file.ll -o programma.exe
.\programma.exe
📂 Struttura del Progetto
main.py: Entry point. Orchestra le fasi di compilazione.

grammar.lark: Specifica della grammatica (Lexer & Parser).

ast_nodes.py: Definizione delle classi dell'Albero Sintattico Astratto (AST).

transformer.py: Converte il Parse Tree di Lark in AST.

semantic_visitor.py: Analisi Semantica (Type checking e Scoping).

codegen.py: Generazione del codice LLVM IR (Naive).

llvm_optimizer.py: Ottimizzazione del codice IR (Mem2Reg, Constant Folding).

