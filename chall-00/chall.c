#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

void win(void) {
    int fd = open("./flag.txt", O_RDONLY);
    if (fd < 0) {
        puts("Unable to open ./flag.txt, this file may not exist");
        return;
    }
    char buf[64];
    int nbytes = read(fd, buf, sizeof(buf));
    if (nbytes < 0) {
        puts("Unable to read ./flag.txt content");
        return;
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
    puts("Welcome to intro2rop chall-00");
    printf("Input: ");
    char buf[32];
    read(0, buf, 64);
    return 0;
}
