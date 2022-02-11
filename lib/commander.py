import re
import subprocess
import os
import signal


def run(cmd: list, live=True, shell=False):
    if shell == True:
        cmd = " ".join(cmd)

    process = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)

    if live == False:
        output = process.stdout.read().decode("utf-8")
        process.communicate()
        return output

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())

    rc = process.poll()


def run_in_background(cmd: list, shell=False):
    if shell == True:
        cmd = " ".join(cmd)

    process = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)
    return process.pid


def find_process(process):
    processes = run(["ps", "ax"], live=False)

    found_processes = re.findall(f"^.*{process}.*$", processes, re.MULTILINE)

    return _get_pids_from_process_list(found_processes)


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except OSError:
        return False


def _get_pids_from_process_list(process_list: list):
    pids = list()
    for process in process_list:
        pids.append(process.split(" ")[0])

    return pids
