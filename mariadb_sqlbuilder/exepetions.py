"""
All custom exceptions for the sql builder
"""


class BetweenValueIsBigger(Exception):
    """
    Raises if value 1 is bigger than value 2,
    usually value 1 need to be smaller or the same then value 2
    """
    pass
