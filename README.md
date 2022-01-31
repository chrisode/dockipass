# Dockipass

Dockipass is a simple python script to start an Ubuntu VM using [multipass](https://multipass.run/) and running docker inside it.

It will let you launch a new VM and install docker inside and mount `/Users` in it. It will also create aliases to docker and docker-compose which will allow you to work with these without installing them locally on your machine. In case you want to have docker locally and use `docker context` to manage your connections, it can  setup a `docker context` for you instead of installing the aliases. 

## Setup
You need multipass and python3 installed. 
`brew install multipass python3`

Python also requires some pip packages installed
`pip3 install -r requirements.txt`

If you decide to use `docker context` will you also need to have a default public ssh key setup in `~/.ssh/id_rsa.pub`.

You can then run `./dockipass.py launch` and it will setup, create and launch the virtual machine for you.

## Usage
```sh
Usage:
dockipass.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...] - Display this help and exit

Commands:
  start [NAME]   - start multipass
  stop [NAME]    - stop multipass
  restart [NAME] - restart multipass
  delete [NAME]  - remove a multipass instance
  launch [NAME]  - launch multipass

Run "dockipass.py COMMAND --help" for more information on a command.
```