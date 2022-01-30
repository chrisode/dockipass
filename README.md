# Dockipass

Dockipass is a simple python script to start an Ubuntu VM using [multipass](https://multipass.run/) and running docker inside it.

It will let you launch a new VM and install docker inside it, it will then mount `/Users` and setup a `docker context` to use with your docker cli. 

## Setup
You need multipass and python3 installed. 
`brew install multipass python3`

Python also requires some pip packages installed
`pip3 install -r requirements.txt`

You also need to have a default public ssh key setup in `~/.ssh/id_rsa.pub`.

You can then run `./dockipass.py launch` and it will launch the 

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
  launch [NAME]  - launch multipass

Run "dockipass.py COMMAND --help" for more information on a command.
```