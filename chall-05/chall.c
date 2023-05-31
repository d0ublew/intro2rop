#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void disass_me(void) {
    __asm__("mov %r12, (%r13)");
}

void win(char *file_name) {
    int fd = open(file_name, O_RDONLY);
    if (fd < 0) {
        printf("Unable to open %s, this file may not exist\n", file_name);
        exit(1);
    }
    close(fd);
    fd = open("./win.txt", O_RDONLY);
    char buf[64];
    int nbytes = read(fd, buf, sizeof(buf));
    if (nbytes < 0) {
        printf("Unable to read ./win.txt content");
        exit(1);
    }
    write(1, buf, nbytes);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    setup();
    puts("Welcome to intro2rop chall-05");
    printf("Input: ");
    char buf[32];
    read(0, buf, 64);
    return 0;
}
