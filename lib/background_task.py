from time import sleep
from .bind_local import bind_local

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

    available_background_tasks[task]()
