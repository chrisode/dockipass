import subprocess
import os, signal

def run(cmd):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())

    rc = process.poll()

def run_bork(cmd):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)
    return process.stdout.read().decode("utf-8")

def run_in_background(cmd):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)
    return process.pid

def kill_process(pid):
    # Hantera om processen inte existerar, ta bara bort? Alternativt hitta ett annat sätt att spara pid som är mer tillförlitligt
    print ("Killing process with id", pid)
    os.kill(pid, signal.SIGTERM)
    