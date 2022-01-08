"""
Tasks module performs tasks (runs methods) at set intervals.
"""
# Package Imports
from discord.ext import tasks as discord_tasks
import logging


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
                          Method must be asynchronous.
        *args (list[]) : The arguments with which to call the method.
    """
    # If the task name is already there, then return.
    if task_name in TASKS:
        return

    # Log.
    logging.debug(f'Added task {task_name} to perform at {interval} second intervals.')

    # Add the task.
    task = discord_tasks.loop(seconds=interval, count=count if count > 0 else None)(method)
    task.start(*args)

    # Slot the task into the dict.
    TASKS[task_name] = task


def remove_task(task_name):
    """
    Removes a task from the list of tasks.

    Arguments:
        task_name (str) : The name of the task to be removed.
    """
    # If that task name doesn't exist, then return.
    if task_name not in TASKS:
        return

    # Stop the task and delete it.
    TASKS[task_name].stop()
    del TASKS[task_name]

    # Log.
    logging.debug(f'Removed task {task_name} from task list.')
