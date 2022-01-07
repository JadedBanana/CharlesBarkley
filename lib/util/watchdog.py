"""
Watchdog class maintains background processes and makes sure that they all continue running.
If any of them exit unexpectedly, then watchdog will exit, too.
"""
# Package Imports
import threading
import logging

# Constants setting
THREAD_CHECK_INTERVAL_SECONDS = 5


def exit_from_main_thread_crash():
    """
    Exits from a main thread crash.
    """
    # Log and exit.
    logging.critical('WATCHDOG: Main thread crashed.')
    stop_all_threads()


def exit_from_cron_thread_crash():
    """
    Exits from a cron thread crash.
    """
    # Log and exit.
    logging.critical('WATCHDOG: Cron thread crashed.')
    stop_all_threads()


def exit_from_temp_files_thread_crash():
    """
    Exits from a temp files thread crash.
    """
    # Log and exit.
    logging.critical('WATCHDOG: Temp files thread crashed.')
    stop_all_threads()


def stop_all_threads():
    """
    Stop all threads.
    This is done by terminating the program via the command line.
    Execution varies based on what operating system we're running on.
    As of right now, only works on Windows and UNIX-based systems.
    """
    # Imports.
    import subprocess
    import platform
    import os

    # First, get the PID.
    pid = os.getpid()

    # If running on Windows, use taskkill command.
    if platform.system() == 'Windows':
        subprocess.run(['taskkill', '-F', '/PID', str(pid)])

    # Otherwise, run the linux-based one.
    subprocess.run(['kill', '-9', str(pid)])


class Watchdog(threading.Thread):
    """
    Watchdog class makes sure all the threads are still running.
    """

    def __init__(self, main_thread, cron_thread, temp_files_thread):
        """
        Watchdog initializer.
        Carries over all the threads.
        """
        # Carry over threads.
        self.main_thread = main_thread
        self.cron_thread = cron_thread
        self.temp_files_thread = temp_files_thread

        # Initialize self.
        threading.Thread.__init__(self)


    def run(self):
        """
        Runs the checking loop.
        """
        # Import time
        import time

        # Infinite loop.
        while True:

            # Check main thread.
            if not self.main_thread.is_alive():
                exit_from_main_thread_crash()

            # Check cron thread.
            if not self.cron_thread.is_alive():
                exit_from_cron_thread_crash()

            # Check temp_files thread.
            if not self.temp_files_thread.is_alive():
                exit_from_temp_files_thread_crash()

            # Sleep.
            time.sleep(THREAD_CHECK_INTERVAL_SECONDS)
