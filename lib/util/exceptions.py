# InvalidDotenvFileError is raised when issues reading in .env file.
class InvalidDotenvFileError(ValueError):
    def __init__(self, reason):
        self.strerr = reason

# UndefinedVariableError is raised when variables in .env file are defined incorrectly or not at all.
class UndefinedVariableError(ValueError):
    def __init__(self, reason):
        self.strerr = reason

# DuplicateCommandError is raised when the command loader finds two commands using the same command name.
class DuplicateCommandError(ValueError):
    def __init__(self, reason):
        self.strerr = reason

# FirstMessageInChannelError is raised when attempting to pull the previous message fails because this is the first message in the channel.
class FirstMessageInChannelError(Exception):
    def __init__(self):
        pass

# CannotAccessUserlistError is raised when can't access the userlist.
class CannotAccessUserlistError(Exception):
    def __init__(self):
        pass

# NoUserSpecifiedError is raised when trying to access a user from an argument that it can't find.
class NoUserSpecifiedError(Exception):
    def __init__(self):
        pass

# UnableToFindUserError is raised when can't find a user based on that argument.
class UnableToFindUserError(Exception):
    def __init__(self, completed_users, incomplete_user):
        self.completed_users = completed_users
        self.incomplete_user = incomplete_user



