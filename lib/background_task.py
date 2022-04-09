from time import sleep
from .bind_local import bind_local
from .commander import find_process, run_in_background, kill_process

available_background_tasks = {"listen": bind_local}


def check_for_background_task(argv):
    if len(argv) < 3:
        return False

    if argv[1] != "background":
        return False

    if not argv[2] in available_background_tasks:
        return False

    return True


def run_task_in_background(task_name):
    if check_if_task_is_running(task_name) == True:
        return False

    run_in_background(["python3", "./dockipass.py", "background", task_name])
    return True


def stop_task_in_background(task):
    pids = find_process(f"background {task}")
    for pid in pids:
        kill_process(int(pid))


def run_task_forever(task_name, sleep_time=30):
    while True:
        available_background_tasks[task_name]()
        sleep(sleep_time)


def check_if_task_is_running(task):
    pids = find_process(f"background {task}")

    if len(pids) > 0:
        return True

    return False
