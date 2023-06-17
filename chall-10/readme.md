# Note

In some competitions, the author would provide a `Dockerfile` for the participants to try out locally. In this scenario, the participants are expected to obtain the corresponding `libc` file from the docker container.

For this `Dockerfile` which is using `pwn.red/jail` to create an isolated environment, the jail copies the whole `ubuntu` filesystems under `/srv` and uses `chroot` to run the binary file. Thus, to know which `libc` is linked with the binary, we would need to interact with the container and do `chroot` as well. Then, the binary could be found under `/app/run`.

```console
user@hostname:~$ docker exec -it intro2rop-chall-10-1 sh
/ # chroot /srv
root@container:/# ldd /app/run
        linux-vdso.so.1 (0x00007ffe99386000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f543d284000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f543d4b1000)
root@container:/# readlink -f /lib/x86_64-linux-gnu/libc.so.6
/usr/lib/x86_64-linux-gnu/libc.so.6
root@container:/# exit
/ # exit
user@hostname:~$ docker cp intro2rop-chall-10-1:/srv/usr/lib/x86_64-linux-gnu/libc.so.6 .
```
