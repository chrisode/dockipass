import subprocess
import os
import signal


def run(cmd, live=True):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)

    if live == False:
        return process.stdout.read().decode("utf-8")

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())

    rc = process.poll()


def run_in_background(cmd):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)
    return process.pid


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except OSError:
        return False
