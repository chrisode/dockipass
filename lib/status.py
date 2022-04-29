from .config import get_name, get_forwarded_ports
from .multipass import get_info, check_aliases
from .background_task import check_if_task_is_running

def status():
    name = get_name()
    info = get_info()

    if info == False:
        return "Failed to get info about VM"

    vm_info = info.get("info").get(name)

    state = vm_info.get("state")

    status = "Dockipass status\n"
    status += f"VM Name:\t {name}\n"
    status += f"State:\t\t {state}\n"
    status += f"Mounts setup:\t {get_mounts_status(vm_info)}\n"
    status += f"Aliases setup:\t {check_aliases()}\n"
    status += f"Listening:\t {get_listening(state)}\n"
    status += f"Forwarded:\t {get_and_format_forwarded_ports(state)}"

    return status


def get_mounts_status(vm_info):
    mounts = list(vm_info.get("mounts").keys())[0]
    return mounts == "/Users"


def get_listening(state):
    if state != "Running":
        return False

    return check_if_task_is_running("listen")


def get_and_format_forwarded_ports(state):
    if state != "Running":
        return False

    forwarded_ports = list(get_forwarded_ports().keys())

    if not forwarded_ports:
        return False

    return ", ".join(forwarded_ports)