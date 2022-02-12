import os


forwarded_file = "forwared_ports.json"
file_contents = ""


def backup_forwared():
    global file_contents
    if not os.path.exists(forwarded_file):
        return False

    with open(forwarded_file, "r") as file:
        file_contents = file.read()


def restore_forwarded():
    if not file_contents:
        return False

    with open(forwarded_file, "w+") as file:
        file.write(file_contents)
