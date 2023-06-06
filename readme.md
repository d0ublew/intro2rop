# intro2rop

## Installation

### Docker

#### Kali Linux

1. Install docker

   ```sh
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl enable docker --now
   sudo usermod -aG docker $USER
   ```

2. Logout and login again or reboot

3. Verify docker is installed

   ```sh
   docker run --rm -it hello-world
   ```

References: [Installing Docker on Kali Linux | Kali Linux Documentation](https://www.kali.org/docs/containers/installing-docker-on-kali/)

#### Other Linux Distribution

1. Install [docker engine](https://docs.docker.com/engine/install/)
2. Install [docker compose](https://docs.docker.com/compose/install/linux/)

### GDB

1. Check if GDB is already installed on your machine, otherwise install it via package manager (the package should be named `gdb`)

   ```sh
   gdb -v
   ```

2. Install GDB plugin, `GEF`

   ```sh
   wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/py && \
       echo source ~/.gdbinit-gef.py >> ~/.gdbinit
   ```

### pwntools

```sh
python3 -m pip install pwntools
```

## Getting Started

```sh
# clone the repo
git clone https://github.com/d0UBleW/intro2rop.git
cd intro2rop

# starting the challenges
docker-compose up -d

# stopping the challenges
docker-compose down

# solving the challenges
cd chall-00
../init.sh
```

## Resources

- [slides](https://docs.google.com/presentation/d/1qCcrEg02nyrph3AhtreSfj_Djhz1GFHzYTJTXVNTDTY/edit?usp=sharing)
