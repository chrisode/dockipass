from .config import DOCKER_BINARY, HOME
from .commander import run


def get_ports():
    docker_output, status = run([DOCKER_BINARY, "ps", "--format", "\"{{.Ports}}\""], live=False)

    if not docker_output:
        return []

    rows = docker_output.strip("\"").split("\n")

    all_ports = []
    for row in rows:
        if not row:
            continue

        ports_list = _format_ports(row)
        all_ports.extend(ports_list)

    return all_ports


def _format_ports(ports):
    formated_list = []
    ports_list = ports.split(", ")

    for port_addr in ports_list:
        port = _format_port(port_addr)
        if (port):
            formated_list.append(port)

    return formated_list


def _format_port(port):
    if port.startswith(":::"):
        return False

    return port.split("->")[0].split(":")[1]

def patch_compose():
    filepath = f"{HOME}/Library/Application Support/multipass/bin/docker-compose"

    new_file = []
    with open(filepath, "r") as file:
        output = file.read()

        if output.find("$arguments") > -1:
            return

        for line in output.split("\n"):
            find_hashbang = line.find("#!")
            if find_hashbang > -1:
                new_file.append(line)
                new_file.append(_bash_for_compose_file())
                continue

            find_compose = line.find("docker-compose -- ")
            if find_compose > -1:
                insert_at = find_compose + len("docker-compose -- ")
                line = line[:insert_at] + "$arguments"

                new_file.append(line)
                continue

            new_file.append(line)

    with open(filepath, "w") as file:
        file.write("\n".join(new_file))


def _bash_for_compose_file():
    return """
arguments=""
f_arg=""

for (( i=1; i <= "$#"; i++ )); do
    arg=${!i}
    arguments+=" $arg"
    if [[ $arg = "-f" ]]; then
        i=$((i+1))
        f_arg=${!i}
        if [[ "$f_arg" == *"/Users"* ]]; then
            arguments+=" $f_arg"
        else
            arguments+=" $(pwd)/$f_arg"
        fi
    fi    
done

if [[ -z $f_arg ]]; then
    f_arg="$(pwd)/docker-compose.yml"
    if [[ -f $f_arg ]]; then
        arguments="-f "$f_arg$arguments
    else
        arguments="-f $(pwd)/docker-compose.yaml"$arguments
    fi
fi
    """