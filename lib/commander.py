import re
import os
import signal
from time import sleep

from sarge import run as sarge_run, Capture


def run(cmd, live=True, shell=False):
    if shell == True:
        cmd = " ".join(cmd)

    process = sarge_run(cmd, stdout=Capture(), stderr=Capture(), shell=shell)

    if live == False:
        return runner(process, live)
    else:
        return run_live(process)


def runner(process, live):
    if (check_process(process) == False):
        if live == True:
            print(read(process.stderr))
        return read(process.stderr), False

    return read(process.stdout), True


def run_live(process):
    while True:
        if (check_process(process) == False):
            print(readline(process.stderr))
            return False

        output = readline(process.stdout)
        if output == "":
            break

        print(output)

    process.wait()


def check_process(process):
    exit_code = process.poll_last()
    if exit_code == None:
        return None

    if exit_code == 0:
        return True

    return False


def read(pipe):
    return pipe.read().decode("utf-8").strip()


def readline(pipe):
    return pipe.readline().decode("utf-8").strip()


def run_in_background(cmd: list, shell=False):
    if shell == True:
        cmd = " ".join(cmd)

    process = sarge_run(cmd, stdout=Capture(),
                        stderr=Capture(), shell=shell, async_=True)
    # _async returns faster than the process can return, so we need to wait a few milliseconds
    sleep(0.5)
    return process.commands[0].process.pid


def find_process(process):
    processes = search_for_process(process)
    return _get_pids_from_process_list(processes)


def search_for_process(process):
    processes, status = run(["ps", "ax"], live=False)
    return re.findall(f"^.*{process}.*$", processes, re.MULTILINE)


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except OSError:
        return False


def _get_pids_from_process_list(process_list: list):
    pids = list()
    for process in process_list:
        pids.append(process.strip().split(" ")[0])

    return pids
