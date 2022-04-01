from pathlib import Path
from .commander import run as run_cmd
from .config import DEFAULT_NAME

aliases = ["docker", "docker-compose"]


def start(name=DEFAULT_NAME):
    _run_multipass(["start", name])


def restart(name=DEFAULT_NAME):
    _run_multipass(["restart", name])


def stop(name=DEFAULT_NAME):
    _run_multipass(["stop", name])


def delete(name=DEFAULT_NAME):
    remove_alias()
    _run_multipass(["delete", name])
    _run_multipass(["purge"])


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2):
    lauched = _run_multipass(["launch", "-c", str(cpu), "-m", memory, "-d", disk, "-n",
                              name, "20.04", "--cloud-init", f"\"cloud-init-config/alias.yaml\""], shell=True)

    if lauched == False:
        return False

    mount_users_folder(name)
    create_alias(name)


def remove_alias():
    for alias in aliases:
        _run_multipass(["unalias", alias])


def create_alias(name=DEFAULT_NAME):
    for alias in aliases:
        _run_multipass(["alias", f"{name}:{alias}", alias])

    modify_compose_alias()


def modify_compose_alias():
    home = str(Path.home())
    filepath = f"{home}/Library/Application Support/multipass/bin/docker-compose"

    new_file = []
    with open(filepath, "r") as file:
        output = file.read()

        if output.find("$arguments") > -1:
            return

        for line in output.split("\n"):
            find_hashbang = line.find("#!")
            if find_hashbang > -1:
                new_file.append(line)
                new_file.append(bash_for_compose_file())
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


def bash_for_compose_file():
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


def mount_users_folder(name=DEFAULT_NAME):
    _run_multipass(["mount", "/Users/", name])


def _run_multipass(cmd: list, shell=False):
    cmd.insert(0, "multipass")
    return run_cmd(cmd, shell=shell)
