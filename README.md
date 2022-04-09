# Dockipass

Dockipass is a simple python script to start an Ubuntu VM using [multipass](https://multipass.run/) and running docker inside it.

It will let you launch a new VM and install docker inside and mount `/Users` in it. It will also create aliases to docker and docker-compose which will allow you to work with these without installing them locally on your machine.

## Setup
You need multipass and python3 installed.<br>
`brew install multipass python3`

*Optional: Install socat to bind serices to localhost* <br>
`brew install socat`

Install dependecies with [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) <br>
`poetry install`

You can then run `./dockipass.py launch` and it will setup, create and launch the virtual machine for you.

## Access dockercontainers from localhost
Multipass does not natively bind forwared ports in the VM to localhost. You can however use the listen command to do this, it will check which ports are forwarded for all running containers and then use `socat` to bind the port and forward traffic to it. It will also kill any running instances of socat when the container is stopped. 

```sh
Usage:
dockipass.py listen [OPTIONS]

Options:
  -c, --cleanup
  -b, --background
  -v, --verbose
  -h, --help [SUBCOMMANDS...] - Display this help and exit
```

## Usage
```sh
Usage:
dockipass.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...] - Display this help and exit

Commands:
  start         - start multipass
  stop          - stop multipass
  restart       - restart multipass
  delete        - remove a multipass instance
  launch [NAME] - launch multipass
  listen        - Bind forwarded docker ports to localhost

Run "dockipass.py COMMAND --help" for more information on a command.
```
