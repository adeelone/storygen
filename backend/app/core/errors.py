class StoryGenError(Exception):
    """Base domain exception."""


class SafetyRefusal(StoryGenError):
    def __init__(self, message: str, rewrite: str) -> None:
        self.message = message
        self.rewrite = rewrite
        super().__init__(message)


class BudgetExceeded(StoryGenError):
    """Generation exceeded its configured soft budget."""
