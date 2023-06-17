# intro2rop

## chall-00

return to `win()`

pw: `6a774b8ae3317c41bc47f0cadc6a75f4`

## chall-01

call `callme()` three times then `win()`

pw: `c9b366f820e5614f7bc00ac0f1277e12`

## chall-02

call `callme(0xdeadbeef)` three times then `win(0xbeefdead, 0xf00d)`

pw: `7eef71bd82f1964e103fc5e1ffacb448`

## chall-03

return to

```c
int fd = open("./flag.txt", O_RDONLY);
```

but we need to set rbp with writable memory address, otherwise it would raise `SIGBUS` error for accessing unmapped memory region

```asm
mov DWORD PTR [rbp-0x4], eax
```

pw: `6cf86a56067b33624585e338ca88953c`

## chall-04

try to call with literal `flag.txt` instead of the memory address

use existing `flag.txt` string address to call `win("flag.txt")`

pw: `edc81fecfb00f0a15b1eb01341ea1774`

## chall-05

using write gadget to write `flag.txt` string on `bss` and use the address to call `win("flag.txt")`

pw: `1acbb901506069c33899076b9eba8cb3`

## chall-06

stack pivot

pw: ``

## chall-07

use imported `system@plt` to call `system("/bin/bash")`

pw: `8ad7fe96b6ef6fb4715b1354f18f095b`

## chall-08

`ret2plt`

pw: `be3f64315f4fd50842c191a4ff5c1114`

## chall-09

`ret2csu`

- try to call `system` but fail since our new pivot address size is limited
- this is because `system` has `sub rsp, 0x388` instruction and then `mov QWORD PTR [rsp+0x8], 0x1` in which `[rsp+0x8]` points to memory region with no write permission

pw: `c62079f6406e071edcccce4fd1a50538`

## RELRO

### No RELRO

```sh
gcc -z norelro ...
gcc -Wl,-z,norelro ...
```

### Partial RELRO

```sh
gcc -z relro -z lazy ...
gcc -Wl,-z,relro,-z,lazy ...
```

### Full RELRO

```sh
gcc -z relro ...
gcc -Wl,-z,relro ...
```

## PLT and GOT

- `-no-pie` -> `.got.plt`
- `-pie` -> `.plt.got`

- `-fno-plt` will always resolved all external symbols at load time

## PIC vs PIE

- PIE means load the executable in random memory address offset

- PIC means the generated assembly code uses PC-relative addressing instead of absolute (PC: program counter / instruction pointer)

```sh
# PIC
jmp label+offset
jmp [rip+0x1337]

# no PIC
jmp 0xdeadbeef
```

## ret2dlresolve
