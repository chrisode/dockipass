
from .commander import run_in_background, kill_process, find_process
from .docker import get_ports
from .multipass import get_name
from json import dumps as json_dumps, loads as json_loads
from os import path

VERBOSE = False


def bind_local(cleanup=False, verbose=False):
    global VERBOSE
    global forwared_ports
    VERBOSE = verbose

    if cleanup == True:
        unbind_all()
        return

    ports = get_ports()
    forward_ports(ports)

    VERBOSE = False
    forwared_ports = {}


forwared_ports = {}
ports_file = "forwared_ports.json"


def forward_ports(ports):
    forwared_ports = get_forwared_ports()
    for port in list(forwared_ports.keys()):
        if port not in ports:
            stop_forward(port)

    if not ports or len(ports) == 0:
        return

    for port in ports:
        if port not in forwared_ports:
            forward(port)
        else:
            log(
                f"Port {port} is already forwarded on pid {forwared_ports[port]}")


def stop_forward(port):
    pid = forwared_ports[port]
    kill_process(pid)
    remove_forwared_port(port)
    log(f"Stopped forwarding on port: {port}, killed pid: {pid}")


def forward(port):
    pid = run_in_background(
        ["socat", f"\"tcp-listen:{port},bind=localhost,reuseaddr,fork\"", f"\"tcp:{get_name()}.local:{port}\""], shell=True)
    add_forwared_port(port, pid)
    log(f"Forwarded port: {port}, socat running with pid: {pid}")


def get_forwared_ports():
    global forwared_ports

    if not forwared_ports:
        if not path.exists(ports_file):
            return {}

        with open(ports_file, "r") as file:
            json = json_loads(file.read())
            forwared_ports = json

    return forwared_ports


def remove_forwared_port(port):
    global forwared_ports
    if port in forwared_ports:
        del forwared_ports[port]
        store_forwared_ports()


def add_forwared_port(port, pid):
    forwared_ports[port] = pid
    store_forwared_ports()


def store_forwared_ports():
    with open(ports_file, "w+") as file:
        file.write(json_dumps(forwared_ports))


# Unbinds all ports and resets forwarded_ports
def unbind_all():
    pids = find_process("socat")

    for pid in pids:
        if pid != "":
            kill_process(int(pid))

    global forwared_ports
    forwared_ports = {}
    store_forwared_ports()


def log(msg):
    if VERBOSE == True:
        print(msg)
