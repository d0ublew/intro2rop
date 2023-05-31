#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int call_counter = 0;

void callme(int key) {
    if (key != 0xdeadbeef)
        return;
    call_counter++;
}

void win(int key1, int key2) {
    if (call_counter < 3)
        exit(1);

    if (key1 != 0xbeefdead || key2 != 0xf00d)
        exit(1);

    int fd = open("./flag.txt", O_RDONLY);
    if (fd < 0) {
        puts("Unable to open ./flag.txt, this file may not exist");
        exit(1);
    }
    char buf[64];
    int nbytes = read(fd, buf, sizeof(buf));
    if (nbytes < 0) {
        puts("Unable to read ./flag.txt content");
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
    puts("Welcome to intro2rop chall-02");
    printf("Input: ");
    char buf[32];
    read(0, buf, 256);
    return 0;
}
