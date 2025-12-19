# Csar
Latinum Programmin Language
Latinus è un linguaggio di programmazione imperativo, staticamente tipizzato, progettato a scopo didattico. Il progetto consiste nella realizzazione di un compilatore completo (Frontend + Backend) che traduce il codice sorgente Latinus in LLVM IR (Intermediate Representation), permettendo la generazione di eseguibili nativi ottimizzati.

Il linguaggio combina la semplicità concettuale del tutorial Kaleidoscope con la struttura formale di un compilatore classico (simil-C/Pascal), utilizzando una sintassi interamente basata su parole chiave latine.

Il compilatore è sviluppato in Python e segue una pipeline modulare:

-Analisi Lessicale e Sintattica (Frontend): Implementata utilizzando la libreria Lark. La grammatica è definita in formato EBNF e gestisce tokenizzazione e parsing per generare l'Abstract Syntax Tree (AST).

-Analisi Semantica: Verifica della coerenza dei tipi (Type Checking) e gestione dell'unico scope (Globale + Locale di funzione).

-Generazione Codice Intermedio (Backend): Visita dell'AST e traduzione in LLVM IR utilizzando llvmlite.

-Linking & Runtime: Il codice IR generato viene compilato e linkato con una Runtime Library in C (per la gestione dell'I/O, es. printf), producendo un eseguibile finale.

