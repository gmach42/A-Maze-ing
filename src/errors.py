class MazeGenerationErrors(Exception):
    def __init__(self, details: str = None):
        message: str = f"A generation error has been raised :\n{details}"
        super().__init__(message)
