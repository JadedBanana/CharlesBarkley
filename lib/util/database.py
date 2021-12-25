# Local Imports
from lib.util import environment

# Package Imports
from sqlalchemy.exc import ArgumentError, OperationalError, NoSuchModuleError, UnboundExecutionError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import logging
import sys

# List of tables we should expect to see in the database.
# Functions similar to lib.util.environment's EXPECTED_DOTENV_VARS.
EXPECTED_DATABASE_TABLES = [
    'reminder'
]

# Database variables
BASE = None
ENGINE = None

# Database tables
REMINDER_TABLE = None


def initialize():
    """
    Initializes the database and pulls all the required tables.
    """
    # Set the outside values as global, so we can modify them.
    global BASE, ENGINE

    # Set the base.
    BASE = automap_base()

    # Set the engine.
    ENGINE = create_engine(environment.get('SQLALCHEMY_DATABASE_URL'))

    # Prepare the base with the engine.
    BASE.prepare(ENGINE, reflect=True)

    # If we've made it this far, then yay! Log our success.
    logging.info('Database connection established successfully.')
