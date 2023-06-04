#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char buf_g[32];

void _main() {
    __asm__("xchg %rsp, %rax");
    __asm__("ret");
    __asm__("pop %rax");
    __asm__("ret");
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    setup();
    write(1, "Welcome to intro2rop chall-08\nInput: ", 37);
    read(0, buf_g, 256);
    write(1, "\nInput 2: ", 10);
    char buf[32];
    return 0;
}
