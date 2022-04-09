import os

forwarded_file = "forwared_ports.json"
file_contents = ""
_config_path = "config/config.json"
_config_content = ""


def backup_forwared():
    global file_contents
    if not os.path.exists(forwarded_file):
        return False

    with open(forwarded_file, "r") as file:
        file_contents = file.read()


def restore_forwarded():
    if not file_contents:
        return False

    with open(_config_path, "w+") as file:
        file.write(file_contents)


def backup_config():
    global _config_content
    if not os.path.exists(_config_path):
        return False

    with open(_config_path, "r") as file:
        _config_content = file.read()


def restore_config():
    if not _config_content:
        return False

    with open(_config_path, "w+") as file:
        file.write(_config_content)