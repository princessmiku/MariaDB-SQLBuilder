"""
All custom exceptions for the sql builder
"""


class BetweenValueIsBigger(Exception):
    """
    Raises if value 1 is bigger than value 2,
    usually value 1 need to be smaller or the same then value 2
    """


class JsonNotSupported(Exception):
    """
    If Json not supported, in example if you use Arithmetic, there's
    no name for that key
    """


class InvalidColumnType(Exception):
    """
    If a type of Column not supported in the validator system
    """


class ValidatorType(Exception):
    """
    The python type of the given value are not a supported type
    of the column
    """


class ValidatorLength(Exception):
    """
    The length of the value is not in the allowed length of the column
    """


class ValidatorRange(Exception):
    """
    If a Number not in the allowed range
    """


class ValidatorUnknown(Exception):
    """
    If is an error unexpectedly, because it shouldn't be possible
    """


class ValidatorTableNotFound(Exception):
    """
    If a table not registered in the validator system
    """


class ValidatorColumnNotFound(Exception):
    """
    If a Column of a table not registered in the validator system
    """
