# Csar
Latinum Programmin Language 
IT:
Latinus è un linguaggio di programmazione imperativo, staticamente tipizzato, progettato a scopo didattico. Il progetto consiste nella realizzazione di un compilatore completo (Frontend + Backend) che traduce il codice sorgente Latinus in LLVM IR (Intermediate Representation), permettendo la generazione di eseguibili nativi ottimizzati.

Il linguaggio combina la semplicità concettuale del tutorial Kaleidoscope con la struttura formale di un compilatore classico (simil-C/Pascal), utilizzando una sintassi interamente basata su parole chiave latine.

Il compilatore è sviluppato in Python e segue una pipeline modulare:

-Analisi Lessicale e Sintattica (Frontend): Implementata utilizzando la libreria Lark. La grammatica è definita in formato EBNF e gestisce tokenizzazione e parsing per generare l'Abstract Syntax Tree (AST).

-Analisi Semantica: Verifica della coerenza dei tipi (Type Checking) e gestione dell'unico scope (Globale + Locale di funzione).

-Generazione Codice Intermedio (Backend): Visita dell'AST e traduzione in LLVM IR utilizzando llvmlite.

-Linking & Runtime: Il codice IR generato viene compilato e linkato con una Runtime Library in C (per la gestione dell'I/O, es. printf), producendo un eseguibile finale.

EN:
Latinus is an imperative, statically typed programming language designed for educational purposes. The project involves the development of a full compiler (Frontend + Backend) that translates Latinus source code into LLVM IR (Intermediate Representation), enabling the generation of optimized native executables.

The language combines the conceptual simplicity of the Kaleidoscope tutorial with the formal structure of a classic compiler (C-like/Pascal-like), featuring a syntax entirely based on Latin keywords.

The compiler is developed in Python and follows a modular pipeline:

Lexical and Syntactic Analysis (Frontend): Implemented using the Lark library. The grammar is defined in EBNF format and handles tokenization and parsing to generate the Abstract Syntax Tree (AST).

Semantic Analysis: Performs Type Checking and manages the single scope structure (Global + Function Local).

Intermediate Code Generation (Backend): Traverses the AST and translates it into LLVM IR using llvmlite.

Linking & Runtime: The generated IR code is compiled and linked with a C Runtime Library (handling I/O, e.g., printf) to produce the final executable.
