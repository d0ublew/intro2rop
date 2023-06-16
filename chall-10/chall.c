#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    setup();
    puts("Welcome to intro2rop chall-10");
    printf("Input: ");
    char buf[32];
    read(0, buf, 0x50);
    printf("%s\n", buf);
    printf("Can you repeat? ");
    read(0, buf, 0x50);
    printf("%s\n", buf);
    printf("One last time? ");
    read(0, buf, 0x50);
    return 0;
}
