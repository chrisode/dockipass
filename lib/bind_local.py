
from .commander import run_bork, run_in_background, kill_process
from json import dumps as json_dumps, loads as json_loads


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

    print(all_ports)

    forward_ports(all_ports)


    #pids = run_bork("ps ax | grep [s]ocat | awk '{print $1}'")
    #print(pids)


def forward_ports(ports):
    forwared_ports = get_forwared_ports()

    for key in forwared_ports:
        if key not in ports:
            pid = forwared_ports[key]
            kill_process(pid)
            del forwared_ports[key]
    
    store_forwared_ports()

    for port in ports:
        if port not in forwared_ports:
            forward(port)

def get_and_format_ports(ports):
    formated_list = []
    ports_list = ports.split(", ")
        
    for port_addr in ports_list:
        port = get_port(port_addr)
        if (port):
            formated_list.append(port)

    return formated_list


def get_port(port):
    if port.startswith(":::"):
        return False

    return port.split("->")[0].split(":")[1]
     
    

def forward(port):
    cmd = f"socat \"tcp-listen:{port},bind=localhost,reuseaddr,fork\" \"tcp:dockipass-alias.local:{port}\""
    pid = run_in_background(cmd)
    store_forwared_port(port, pid)


forwared_ports = {}
ports_file = "forwared_ports.json"


def get_forwared_ports():
    global forwared_ports

    if not forwared_ports:
        with open(ports_file, "r") as file:
            json = json_loads(file.read())
            forwared_ports = json

    return forwared_ports


def store_forwared_port(port, pid):
    forwared_ports[port] = pid
    store_forwared_ports()


def store_forwared_ports():
    with open(ports_file, "w") as file:
        file.write(json_dumps(forwared_ports))

    #docker_output.split("Å")

    #print(docker_output)


#docker ps --format "{status=\"{{.State}}\",ports=\"{{.Ports}}\"}"
#socat "tcp-listen:49154,bind=localhost,reuseaddr,fork" "tcp:dockipass-alias.local:49154"