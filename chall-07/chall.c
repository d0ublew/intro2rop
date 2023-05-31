#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char shell[] = "/bin/bash";

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void info() {
    printf("Running as: ");
    system("whoami");
}

int main(void) {
    setup();
    puts("Welcome to intro2rop chall-07");
    printf("\nInput: ");
    char buf[32];
    read(0, buf, 72);
    return 0;
}
