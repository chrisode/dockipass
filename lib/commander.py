import subprocess

def run(cmd):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())

    rc = process.poll()