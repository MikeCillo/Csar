#include <stdio.h>

void scribe_int(int x) { printf("%d\n", x); }
void scribe_char(char c) { printf("%c\n", c); }

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