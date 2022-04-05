from platform import machine as platform_machine

def _get_architecture():
    machine = platform_machine()

    if not machine:
        return "amd64"

    return machine

DEFAULT_NAME = "dockipass"
ARCHITECTURE = _get_architecture()