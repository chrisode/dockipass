
from .commander import run_bork, run_in_background, kill_process
from json import dumps as json_dumps, loads as json_loads
from os import path


def bind_local(cleanup = False):

    if cleanup == True:
        unbind_all()
        return
    

    ports = get_docker_ports()
    forward_ports(ports)


def get_docker_ports():
    docker_output = run_bork('docker ps --format "{{.State}}Å{{.Ports}}"')

    if not docker_output:
        forward_ports([])
        return False

    rows = docker_output.split("\n")

    all_ports = []
    for row in rows:
        if not row:
            continue
        state, ports = row.split("Å")

        if state != "running":
            continue

        ports_list = get_and_format_ports(ports)
        all_ports.extend(ports_list)

    return all_ports


def get_and_format_ports(ports):
    formated_list = []
    ports_list = ports.split(", ")

    for port_addr in ports_list:
        port = get_port(port_addr)
        if (port):
            formated_list.append(int(port))

    return formated_list


def get_port(port):
    if port.startswith(":::"):
        return False

    return port.split("->")[0].split(":")[1]


forwared_ports = {}
ports_file = "forwared_ports.json"


def forward_ports(ports):
    forwared_ports = get_forwared_ports()

    for port in list(forwared_ports.keys()):
        if port not in ports:
            stop_forward(port)

    for port in ports:
        if port not in forwared_ports:
            forward(port)


def stop_forward(port):
    pid = forwared_ports[port]
    kill_process(pid)
    remove_forwared_port(port)
    print(f"Stopped forwarding on port: {8080}, killed pid: {pid}")


def forward(port):
    cmd = f"socat \"tcp-listen:{port},bind=localhost,reuseaddr,fork\" \"tcp:dockipass-alias.local:{port}\""
    pid = run_in_background(cmd)
    add_forwared_port(port, pid)
    print(f"Forwared port: {port}, socat running with pid: {pid}")


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
    pids = run_bork("ps ax | grep [s]ocat | awk '{print $1}'")
    for pid in pids.split("\n"):
        if pid != "":
            kill_process(int(pid))

    global forwared_ports 
    forwared_ports = {}
    store_forwared_ports()