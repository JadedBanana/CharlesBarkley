"""
Tasks module performs tasks (runs methods) at set intervals.
"""
# Package Imports
from datetime import datetime, timedelta
import threading
import logging
import time


# Store tasks.
CURRENT_TASK_THREAD = None
TASKS = {}


def add_task(task_name, interval, count, method, *args):
    """
    Adds a task to the list of tasks to be performed.

    Arguments:
        task_name (str) : The name of the task that will be performed.
                          If duplicate, this task won't be added to the list.
        interval (int) : The amount of seconds before performing the task.
        count (int) : The number of times to perform the task before removing it from the list.
                      Numbers <= 0 will be treated as infinity.
        method (method) : The method that will be called when each interval is reached.
        *args (list[]) : The arguments with which to call the method.
    """
    # If the task name is already there, then return.
    if task_name in TASKS:
        return

    # Otherwise, add it in.
    TASKS[task_name] = {'interval': interval, 'method': method, 'args': args, 'count': count,
                        'next': datetime.now() + timedelta(seconds=interval), 'last': datetime.now()}

    # Log.
    logging.debug(f'Added task {task_name} to perform at {interval} second intervals')

    # Start the thread, if we should.
    start_thread_if_not_going()


def remove_task(task_name):
    """
    Removes a task from the list of tasks.

    Arguments:
        task_name (str) : The name of the task to be removed.
    """
    # If that task name doesn't exist, then return.
    if task_name not in TASKS:
        return

    # Delete the task.
    del TASKS[task_name]

    # Log.
    logging.debug(f'Removed task {task_name} from task list')


def start_thread_if_not_going():
    """
    Starts the task-performing thread, if it's not already running.
    """
    # Global variable.
    global CURRENT_TASK_THREAD

    # A simple few lines.
    if not CURRENT_TASK_THREAD:
        CURRENT_TASK_THREAD = threading.Thread(target=perform_task_loop)
        CURRENT_TASK_THREAD.start()


def perform_task(task):
    """
    Performs the given task.

    Arguments:
        task (dict) : The task's data.
    """
    # Run the method with the arguments.
    try:
        task['method'](*task['args'])

        # Decrease the count if the count > 0.
        if task['count'] > 0:
            task['count'] -= 1

    # If an error occurred, log it.
    except Exception:
        # Get the traceback_str.
        import traceback
        traceback_str = traceback.format_exc().replace('\n\n', '\n').strip('\n')

        # Log the error.
        logging.error(f"Exception caused with task {task['method']} with arguments {task['args']}:\n"
                      f"{traceback_str}")

        # Remove this task from the task list by setting its remaining runs to 0.
        task['count'] = 0


def perform_task_loop():
    """
    Performs all the tasks in TASKS.
    Will continue forever if this isn't run in parallel.
    """
    # Log the beginning of the thread.
    logging.debug('Task thread starting...')

    # While there are tasks, run them.
    while TASKS:

        # Set the time to sleep as the minimum time til the next task.
        time_until_next_task = (min(TASKS[task]['next'] for task in TASKS) - datetime.now()).seconds
        time.sleep(max(time_until_next_task, 0) + 0.05)

        # Perform all the tasks that were supposed to happen before now.
        now = datetime.now()
        for task in [task for task in TASKS if TASKS[task]['next'] <= now]:
            perform_task(TASKS[task])

            # If the task is out of runs, then remove it.
            if not TASKS[task]['count']:
                remove_task(task)

            # Otherwise, set the next time.
            else:
                TASKS[task]['next'] = TASKS[task]['last'] + timedelta(seconds=TASKS[task]['interval'])
                TASKS[task]['last'] = now

    # Set the CURRENT_TASK_THREAD to None.
    global CURRENT_TASK_THREAD
    CURRENT_TASK_THREAD = None

    # Log the end of the thread.
    logging.debug('Task thread finished.')


def is_alive():
    """
    Returns whether the thread is alive or not.
    Note: Will return True if the thread is None.
          Will only return False if the thread exists and isn't running.

    Returns:
        bool : Whether the thread is running.
    """
    # If there are no tasks, return true.
    if not TASKS:
        return True

    # Otherwise, there are tasks. If there is no thread, then return False.
    if not CURRENT_TASK_THREAD:
        return False

    # Finally, return the CURRENT_TASK_THREAD's option for that.
    return CURRENT_TASK_THREAD.is_alive()
