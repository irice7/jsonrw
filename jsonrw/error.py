class PossibleError:
    ERROR: bool = False
    MESSAGE: str = ''

    @classmethod
    def __init__(cls, error: bool, message: str):
        cls.ERROR, cls.MESSAGE = error, message
