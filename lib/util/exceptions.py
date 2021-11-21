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

# Used in __get_closest_user to disclose why an empty list would be returned
class NoUserSpecifiedError(Exception):
    def __init__(self, args=None): Exception.__init__(self, args)
class UnableToFindUserError(Exception):
    def __init__(self, completed_users, incomplete_user, args=None): self.completed_users = completed_users; self.incomplete_user = incomplete_user; Exception.__init__(self, args)
class ArgumentTooShortError(Exception):
    def __init__(self, short_user, args=None): self.short_user = short_user; Exception.__init__(self, args)


