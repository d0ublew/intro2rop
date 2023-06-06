#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void disass_me() {
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
    char banner[] = "Welcome to intro2rop chall-08";
    puts(banner);
    printf("[LEAK] banner address: %p\n", banner);
    printf("Input 1: ");
    char buf_1[64];
    read(0, buf_1, 0x80);
    printf("Input 2: ");
    char buf_2[64];
    read(0, buf_2, 96);
    return 0;
}
