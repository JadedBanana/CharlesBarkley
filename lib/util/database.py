# Package Imports
import sqlalchemy as db


# Database variables
ENGINE = None
CONNECTION = None
METADATA = None

# Database tables
REMINDER_TABLE = None


def initialize():
    """
    Initializes the database and pulls all the required tables.
    """