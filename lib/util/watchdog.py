"""
Watchdog class maintains background processes and makes sure that they all continue running.
If any of them exit unexpectedly, then watchdog will exit, too.
"""
# Package Imports
import threading
import logging
import sys

# Constants setting
THREAD_CHECK_INTERVAL_SECONDS = 5


def exit_from_main_thread_crash():
    """
    Exits from a main thread crash.
    """
    # Log and exit.
    logging.critical('Main thread crashed.')
    sys.exit(-1)


def exit_from_cron_thread_crash():
    """
    Exits from a main thread crash.
    """
    # Log and exit.
    logging.critical('Cron thread crashed.')
    sys.exit(-1)


def exit_from_tempfiles_thread_crash():
    """
    Exits from a main thread crash.
    """
    # Log and exit.
    logging.critical('Tempfiles thread crashed.')
    sys.exit(-1)


class Watchdog(threading.Thread):
    """
    Watchdog class makes sure all the threads are still running.
    """

    def __init__(self, main_thread, cron_thread, tempfiles_thread):
        """
        Watchdog initializer.
        Carries over all the threads.
        """
        # Carry over threads.
        self.main_thread = main_thread
        self.cron_thread = cron_thread
        self.tempfiles_thread = tempfiles_thread

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

            # Check tempfiles thread.
            if not self.tempfiles_thread.is_alive():
                exit_from_tempfiles_thread_crash()

            # Sleep.
            time.sleep(THREAD_CHECK_INTERVAL_SECONDS)
