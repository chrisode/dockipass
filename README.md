# Dockipass

Dockipass is a simple python script to start an Ubuntu VM using [multipass](https://multipass.run/) and running docker inside it.

It will let you launch a new VM and install docker inside and mount `/Users` in it. It will also create aliases to docker and docker-compose which will allow you to work with these without installing them locally on your machine.

## Setup
You need multipass and python3 installed.<br>
`brew install multipass python3 socat`

Install dependecies with [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) <br>
`poetry install`

Go into your poetry shell
`poetry shell`

You can then run `./dockipass.py launch` and it will setup, create and launch the virtual machine for you.

## Access dockercontainers from localhost
Multipass does not natively bind ports that docker forwared from its containers in the VM to localhost. Dockipass will by default listening for these changes and forward these ports to your localhost when running `dockipass.py launch` and  `dockipass.py start`. You can prevent this behaviour by adding the flag `-nobind` when using those commands.
When stopping or deleting the VM it will remove any forwarded ports, you can also stop the task that listens for changes by running `dockipass.py listen stop`. 

```sh
Usage:
dockipass.py listen [OPTIONS] COMMAND

Arguments:
   COMMAND - Choices: start, stop, cleanup

Options:
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
