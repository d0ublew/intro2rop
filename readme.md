# intro2rop

## Requirements

- GNU/Linux system
- Docker
- GDB (preferably with `GEF` plugin)
- Decompiler (optional): Ghidra or Binary Ninja Cloud
- pwntools
- pwninit
- one_gadget

## Tools

### Docker

For Kali Linux

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

4. Install docker-compose

   ```sh
   sudo mkdir -p /usr/local/lib/docker/cli-plugins
   sudo curl -SL https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
   sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
   docker compose version
   sudo ln -sf /usr/local/lib/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose
   ```

References: [Installing Docker on Kali Linux | Kali Linux Documentation](https://www.kali.org/docs/containers/installing-docker-on-kali/)

For **other** GNU/Linux distributions

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

### Decompiler

Choose **either** one.

#### Binary Ninja Cloud

Sign up here if you have not: <https://cloud.binary.ninja/>

#### Ghidra

For Kali Linux

```sh
sudo apt install ghidra
```

For **other** GNU/Linux distribution, consult the [official guide](https://htmlpreview.github.io/?https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_10.3.1_build/GhidraDocs/InstallationGuide.html)

### pwntools

```sh
python3 -m pip install -U pwntools
```

### pwninit

```sh
wget https://github.com/io12/pwninit/releases/download/3.3.0/pwninit -O pwninit
chmod +x ./pwninit
sudo mv ./pwninit /opt/pwninit
```

### one_gadget

```sh
# Install `ruby` with your favorite package manager
sudo apt install ruby

# Install `one_gadget`
sudo gem install one_gadget
```

## Getting Started

```sh
# clone the repo
git clone https://github.com/d0UBleW/intro2rop.git
cd intro2rop

# starting the challenges
make

# solving the challenges
cd chall-00
../init.sh

# stopping the challenges
make clean
```

## Resources

- [slides](https://docs.google.com/presentation/d/1qCcrEg02nyrph3AhtreSfj_Djhz1GFHzYTJTXVNTDTY/edit?usp=sharing)
