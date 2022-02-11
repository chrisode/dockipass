import re
from time import sleep
from .bind_local import bind_local
from .commander import run as run_cmd

available_background_tasks = {"listen": bind_local}


def check_for_background_task(argv):
    if len(argv) < 3:
        return False

    if argv[1] != "background":
        return False

    if not argv[2] in available_background_tasks:
        return False

    return True


def run_task_forever(task, sleep_time=30):
    while True:
        result = run_task(task)
        if result == False:
            break

        sleep(sleep_time)


def run_task(task):
    if not task in available_background_tasks:
        return False
    
    if check_if_task_is_running(task) == False:
        available_background_tasks[task]()


def check_if_task_is_running(task):
    output = run_cmd(["ps", "ax"], live=False)
    items = re.findall(f"^.*background {task}.*$", output, re.MULTILINE)

    if len(items) > 0:
        return True

    return False