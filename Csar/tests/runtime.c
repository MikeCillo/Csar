#include <stdio.h>

void scribe_int(int x) { printf("%d\n", x); }
void scribe_char(char c) { printf("%c\n", c); }
void scribe_bool(int x) {
    if (x) printf("verum\n");
    else printf("falsum\n");
}

int legge_int() {
    int x;
    scanf("%d", &x);
    return x;
}

char legge_char() {
    char c;
    scanf(" %c", &c);
    return c;
}


// MENU PER LA CALCOLATRICE
void scribe_menu() {
    printf("\n=== CALCOLATRICE CSAR ===\n");
    printf("1. Addizione (+)\n");
    printf("2. Sottrazione (-)\n");
    printf("3. Moltiplicazione (*)\n");
    printf("4. Divisione (/)\n");
    printf("0. Esci\n");
    printf("=========================\n");
}

// errore divisone per 0 (calcolatrice)
void scribe_error() {
    printf("⚠ ERRORE: Non puoi dividere per zero!\n");
}

void chiede_int() {
    printf("Inserisci un numero intero: ");
}

void annuncia_res() {
    printf("Il risultato è: ");
}