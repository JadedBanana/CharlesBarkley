"""
Environment file. Helps with managing dozens of environment variables.
"""
# Imports
from lib.util import environment
import logging


# Storage of logging levels based on numbers.
LOGGING_LEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]

def basic_setup():
    """
    Performs basic setup for the logging module.
    Sets the logging format and level.
    """
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=LOGGING_LEVELS[environment.get('LOGGING_LEVEL')])


def debug_setup():
    """
    Performs debug setup for the logging module.
    Sets the logging format and level.
    """
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG)