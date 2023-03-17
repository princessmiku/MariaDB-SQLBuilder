"""
Arithmetic Operators, math in sql

More information under
https://mariadb.com/kb/en/arithmetic-operators/
"""
from typing import Union


_invalid_arithmetic = ["+", "-", "*", "/", "%"]


class ArithmeticColumn:

    def __init__(self, table: str, column: str):
        self._column = table + "." + column

    def __str__(self):
        return self._column


def _check_type(variable: Union[ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder']):
    from mariadb_sqlbuilder.builder.select_builder import SelectBuilder
    if not isinstance(variable, (ArithmeticColumn, Arithmetic, int, float, SelectBuilder)):
        raise TypeError(
            "Variable is not a valid type, accept ArithmeticColumn, Arithmetic, int, float or"
            " a sub Select query (SelectBuilder)"
        )


class Arithmetic:

    def __init__(self, variable: Union[
        ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder'
    ]):
        if not isinstance(variable, (ArithmeticColumn, int, float)):
            raise
        self.arithmetic_str = str(variable)

    def add(self, variable: Union[
        ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder'
    ]):
        _check_type(variable)
        if str(variable).endswith(";"):
            variable = str(variable)[:-1]
        self.arithmetic_str += f" + {variable}"
        return self

    def sub(self, variable: Union[
        ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder'
    ]):
        _check_type(variable)
        if str(variable).endswith(";"):
            variable = str(variable)[:-1]
        self.arithmetic_str += f" - {variable}"
        return self

    def mul(self, variable: Union[
        ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder'
    ]):
        _check_type(variable)
        if str(variable).endswith(";"):
            variable = str(variable)[:-1]
        self.arithmetic_str += f" * {variable}"
        return self

    def div(self, variable: Union[
        ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder'
    ]):
        _check_type(variable)
        if str(variable).endswith(";"):
            variable = str(variable)[:-1]
        self.arithmetic_str += f" / {variable}"
        return self

    def mod(self, variable: Union[
        ArithmeticColumn, 'Arithmetic', int, float, 'SelectBuilder'
    ]):
        _check_type(variable)
        if str(variable).endswith(";"):
            variable = str(variable)[:-1]
        self.arithmetic_str += f" % {variable}"
        return self

    def __str__(self):
        return f"({self.arithmetic_str})"
