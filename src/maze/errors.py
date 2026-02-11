class MazeGenerationErrors(Exception):
    def __init__(self, details: str = None):
        message: str = f"A generation error has been raised :\n{details}"
        super().__init__(message)


class ConfigError(MazeGenerationErrors):
    def __init__(self, mp: str = None):
        details: str = f"A config file error :\n {mp}"
        super().__init__(details)


class FormatError(ConfigError):
    pass


class MissingKey(ConfigError):
    pass


class TooManyVar(ConfigError):
    pass
