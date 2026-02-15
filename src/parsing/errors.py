class MazeGenerationErrors(Exception):
    """
    A base class for exceptions related to maze generation and
    configuration errors.
    """
    def __init__(self, details: str | None = None):
        message: str = f"A generation error has been raised :\n{details}"
        super().__init__(message)


class ConfigError(MazeGenerationErrors):
    def __init__(self, mp: str | None = None):
        details: str = f"A config file error :\n {mp}"
        super().__init__(details)


class FormatError(ConfigError):
    pass


class MissingKey(ConfigError):
    pass


class TooManyVar(ConfigError):
    pass


class NoSolutionError(Exception):
    pass


class ExecutionError(Exception):
    def __init__(self, details: str):
        message: str = f' An execution error has been raised: {details}'
        super().__init__(message)
