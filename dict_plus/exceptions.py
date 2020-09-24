class InvalidIteratorException(Exception):
    """
    Raised when an invalid Iterator is passed in
    """
    pass


class InvalidElementTypeException(TypeError):
    """
    Raised when the Element type doesn't match the expected element type
    """
    pass


class InvalidElementValueException(ValueError):
    """
    Raised when the Element value doesn't match the expected element value constraints
    """
    pass


class InvalidSubDictType(ValueError):
    """
    Raised when the subdict type of a listdict isn't the correct type
    """
    pass
