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
    write(1, "Welcome to intro2rop chall-08\nInput: ", 37);
    char buf[32];
    read(0, buf, 256);
    return 0;
}
