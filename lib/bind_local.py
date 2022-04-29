
from .config import get_forwarded_ports, set_forwarded_ports
from .commander import run_in_background, kill_process, find_process
from .docker import get_ports
from .multipass import get_name

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


def forward_ports(ports):
    forwared_ports = get_forwarded_ports()

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
    ports = get_forwarded_ports()
    pid = ports[port]
    kill_process(pid)
    remove_forwared_port(port)
    log(f"Stopped forwarding on port: {port}, killed pid: {pid}")


def forward(port):
    pid = run_in_background(
        ["socat", f"\"tcp-listen:{port},bind=localhost,reuseaddr,fork\"", f"\"tcp:{get_name()}.local:{port}\""], shell=True)
    add_forwared_port(port, pid)
    log(f"Forwarded port: {port}, socat running with pid: {pid}")


def remove_forwared_port(port):
    ports = get_forwarded_ports()
    if port in ports:
        del ports[port]
        set_forwarded_ports(ports)


def add_forwared_port(port, pid):
    ports = get_forwarded_ports()
    ports[port] = pid
    set_forwarded_ports(ports)


# Unbinds all ports and resets forwarded_ports
def unbind_all():
    pids = find_process("socat")

    for pid in pids:
        if pid != "":
            kill_process(int(pid))

    set_forwarded_ports({})


def log(msg):
    if VERBOSE == True:
        print(msg)
