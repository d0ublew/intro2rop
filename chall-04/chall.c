#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(char *file_name) {
    int fd = open(file_name, O_RDONLY);
    if (fd < 0) {
        printf("Unable to open %s, this file may not exist\n", file_name);
        exit(1);
    }
    char buf[64];
    int nbytes = read(fd, buf, sizeof(buf));
    if (nbytes < 0) {
        printf("Unable to read %s content", file_name);
        exit(1);
    }
    puts("Congrats! Here is your beloved flag.txt");
    write(1, buf, nbytes);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    setup();
    puts("Welcome to intro2rop chall-04");
    printf("Input: ");
    char buf[32];
    read(0, buf, 96);
    return 0;
}
