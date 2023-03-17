"""
This modul is there for the basic functions of all query's
"""
from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from typing import Union, Tuple

from mariadb_sqlbuilder.helpful.validator import Validator
from mariadb_sqlbuilder.exepetions import BetweenValueIsBigger
from mariadb_sqlbuilder.helpful.arithmetic import Arithmetic
from mariadb_sqlbuilder.helpful import subquery_operator as suop


# get the name of a table column
def _get_tcn(tb, column: str) -> str:
    if tb.validator:
        tb.validator.check_column_exists(tb.table, column)
    return tb.table + "." + column


def _get_tcn_without_validator(table: str, column: str) -> str:
    return table + "." + column


def _get_tcn_validator(table: str, column: str, validator: Validator) -> str:
    if validator:
        validator.check_column_exists(table, column)
    return table + "." + column


def _transform_value_valid(value: Union[str, int, bool]) -> str:
    if value is None:
        return "NULL"
    elif isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    elif isinstance(value, (int, Arithmetic)):
        return str(value)
    elif isinstance(value, timedelta):
        if "," in str(value):
            return f"'{str(value).split(', ')[1]}'"
        return f"'{value}'"
    elif isinstance(value, datetime):
        return "'" + value.strftime("%m-%d-%Y %H:%i:%s") + "'"
    return f"'{value}'"


class BaseBuilder(ABC):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        self._tb = tb

    @abstractmethod
    def get_sql(self) -> str:
        """
        Get the sql script that was generated
        :return:
        """

    @property
    def tb(self):
        """
        returns the table builder
        :return:
        """
        return self._tb


class ConditionsBuilder(BaseBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        super().__init__(tb)
        if "condition" in kwargs:
            self.__conditions = kwargs["condition"].get_conditions()
            self.__default_condition = kwargs["condition"].get_default_condition()
        else:
            self.__conditions = []
            self.__default_condition = "AND"

    def where(self, expression: Union[str, Arithmetic, tuple],
              value: Union[str, int, float, 'SelectBuilder'], filter_operator: str = "=",
              *, subquery_operator: str = ''):
        """
        Adds a WHERE condition for an exact match of a column value.
        :param expression: a Column or an Arithmetic
        :param value:
        :param filter_operator:
        :param subquery_operator:
        :return:
        """
        self.__check_if_or_and()
        from .select_builder import SelectBuilder
        if isinstance(value, SelectBuilder):
            if subquery_operator != '' and subquery_operator not in [
                suop.ALL, suop.ANY, suop.EXISTS
            ]:
                raise TypeError(
                    'Unsupported subquery operator'
                )

            if isinstance(expression, tuple):
                expression_list_str: str = '(' + ', '.join(
                    [_get_tcn(self.tb, expr) for expr in expression]
                ) + ')'
            elif isinstance(expression, str):
                expression_list_str: str = _get_tcn(self.tb, expression)
            else:
                expression_list_str: str = str(expression)
            self.__conditions.append(
                f"{expression_list_str} {filter_operator} {subquery_operator}({value.get_sql()[:-1]})"
            )
        elif isinstance(expression, str):
            self.__conditions.append(f"{_get_tcn(self.tb, expression)} {filter_operator} "
                                          f"{_transform_value_valid(value)}")
        else:
            self.__conditions.append(f"{expression} {filter_operator} "
                                     f"{_transform_value_valid(value)}")
        return self

    def where_in(self, expression: Union[str, Arithmetic, tuple],
                 value: Union[Tuple[str, int, float], 'SelectBuilder']):
        """
        Adds a WHERE condition for a list of checked values in a column.
        :param expression: a Column or an Arithmetic
        :param value:
        :return:
        """
        self.__check_if_or_and()
        from .select_builder import SelectBuilder
        if isinstance(value, SelectBuilder):
            if isinstance(expression, tuple):
                expression_list_str: str = '(' + ', '.join(
                    [_get_tcn(self.tb, expr) for expr in expression]
                ) + ')'
            elif isinstance(expression, str):
                expression_list_str: str = _get_tcn(self.tb, expression)
            else:
                expression_list_str: str = str(expression)
            self.__conditions.append(f"{expression_list_str} IN ({value.get_sql()[:-1]})")
        elif isinstance(expression, str):
            self.__conditions.append(
                f"{_get_tcn(self.tb, expression)} IN {str(value)}"
            )
        else:
            self.__conditions.append(
                f"{expression} IN {str(value)}"
            )
        return self

    def where_in_not(self, expression: Union[str, Arithmetic, tuple],
                     value: Union[Tuple[str, int, float], 'SelectBuilder']):
        """
        Adds a WHERE condition for a list of unchecked values in a column.
        :param expression: a Column or an Arithmetic
        :param value:
        :return:
        """
        self.__check_if_or_and()
        from .select_builder import SelectBuilder
        if isinstance(value, SelectBuilder):
            if isinstance(expression, tuple):
                expression_list_str: str = '(' + ', '.join(
                    [_get_tcn(self.tb, expr) for expr in expression]
                ) + ')'
            elif isinstance(expression, str):
                expression_list_str: str = _get_tcn(self.tb, expression)
            else:
                expression_list_str: str = str(expression)
            self.__conditions.append(f"{expression_list_str} IN ({value.get_sql()[:-1]})")

        elif isinstance(expression, str):
            self.__conditions.append(
                f"{_get_tcn(self.tb, expression)} NOT IN {str(value)}"
            )
        else:
            self.__conditions.append(
                f"{expression} NOT IN {str(value)}"
            )
        return self

    def like(self, expression: Union[str, Arithmetic], value: Union[str, int, float]):
        """
        Adds a WHERE condition for a partial match of a column value.
        :param expression: a Column or an Arithmetic
        :param value:
        :return:
        """
        self.__check_if_or_and()
        if isinstance(expression, str):
            self.__conditions.append(
                f"{_get_tcn(self.tb, expression)} LIKE {_transform_value_valid(value)}"
            )
        else:
            self.__conditions.append(
                f"{expression} LIKE {_transform_value_valid(value)}"
            )
        return self

    def like_not(self, expression: Union[str, Arithmetic], value: Union[str, int, float]):
        """
        Adds a WHERE condition for a partial mismatch of a column value.
        :param expression: a Column or an Arithmetic
        :param value:
        :return:
        """
        self.__check_if_or_and()
        if isinstance(expression, str):
            self.__conditions.append(
                f"{_get_tcn(self.tb, expression)} NOT LIKE {_transform_value_valid(value)}"
            )
        else:
            self.__conditions.append(
                f"{expression} NOT LIKE {_transform_value_valid(value)}"
            )
        return self

    def between(self, expression: Union[str, Arithmetic],
                value1: Union[str, int, float, 'SelectBuilder'],
                value2: Union[str, int, float, 'SelectBuilder']):
        """
        Adds a WHERE condition for a range of values in a column.
        :param expression: a Column or an Arithmetic
        :param value1:
        :param value2:
        :return:
        """
        self.__check_if_or_and()
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            if value1 > value2:
                raise BetweenValueIsBigger("Value 1 is bigger then value 2")
        from .select_builder import SelectBuilder
        if isinstance(expression, str):
            if isinstance(value1, SelectBuilder):
                value1 = f"({value1.get_sql()[:-1]})"
            else:
                value1 = _transform_value_valid(value1)
            if isinstance(value2, SelectBuilder):
                value2 = f"({value2.get_sql()[:-1]})"
            else:
                value2 = _transform_value_valid(value2)
            self.__conditions.append(
                f"{_get_tcn(self.tb, expression)} "
                f"BETWEEN {value1} "
                f"AND {value2}"
            )
        else:
            self.__conditions.append(
                f"{expression} "
                f"BETWEEN {_transform_value_valid(value1)} "
                f"AND {_transform_value_valid(value2)}"
            )
        return self

    def between_not(self, expression: Union[str, Arithmetic],
                    value1: Union[str, int, float, 'SelectBuilder'],
                    value2: Union[str, int, float, 'SelectBuilder']):
        """
        Adds a WHERE condition for a range of values not in a column.
        :param expression: a Column or an Arithmetic
        :param value1:
        :param value2:
        :return:
        """
        self.__check_if_or_and()
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            if value1 > value2:
                raise BetweenValueIsBigger("Value 1 is bigger then value 2")
        from .select_builder import SelectBuilder
        if isinstance(expression, str):
            if isinstance(value1, SelectBuilder):
                value1 = f"({value1.get_sql()[:-1]})"
            else:
                value1 = _transform_value_valid(value1)
            if isinstance(value2, SelectBuilder):
                value2 = f"({value2.get_sql()[:-1]})"
            else:
                value2 = _transform_value_valid(value2)
            self.__conditions.append(
                f"{_get_tcn(self.tb, expression)} "
                f"NOT BETWEEN {value1} "
                f"AND {value2}"
            )
        else:
            self.__conditions.append(
                f"{expression} "
                f"NOT BETWEEN {_transform_value_valid(value1)} "
                f"AND {_transform_value_valid(value2)}"
            )
        return self

    def is_not_null(self, column: str):
        """
        Adds a WHERE condition for a column that is not NULL.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb, column)} IS NOT NULL")
        return self

    def is_null(self, column: str):
        """
        Adds a WHERE condition for a column that is NULL.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb, column)} IS NULL")
        return self

    def is_true(self, column: str):
        """
        Adds a WHERE condition for a column that is True.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb, column)} IS TRUE")
        return self

    def is_not_true(self, column: str):
        """
        Adds a WHERE condition for a column that is not True.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb, column)} IS NOT TRUE")
        return self

    def is_false(self, column: str):
        """
        Adds a WHERE condition for a column that is False.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb, column)} IS FALSE")
        return self

    def is_not_false(self, column: str):
        """
        Adds a WHERE condition for a column that is not False.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb, column)} IS NOT FALSE")
        return self

    def __check_if_or_and(self):
        """
        Checks if the last added condition is either "AND" or "OR"
        and adds the default condition if not.
        :return:
        """
        if not self.__conditions:
            return
        if self.__conditions[-1] not in ["AND", "OR"]:
            self.__conditions.append(self.__default_condition)

    def OR(self):
        """
        Adds an OR condition to the WHERE conditions.
        :return:
        """
        if not self.__conditions or self.__conditions[-1] == "OR":
            return self
        elif self.__conditions[-1] == "AND":
            self.__conditions.pop(-1)
        self.__conditions.append("OR")
        return self

    def AND(self):
        """
        Adds an AND condition to the WHERE conditions.
        :return:
        """
        if not self.__conditions or self.__conditions[-1] == "AND":
            return self
        elif self.__conditions[-1] == "OR":
            self.__conditions.pop(-1)
        self.__conditions.append("AND")
        return self

    def default_and(self):
        """
        Sets the default condition to "AND".
        :return:
        """
        self.__default_condition = "AND"
        return self

    def default_or(self):
        """
        Sets the default condition to "OR".
        :return:
        """
        self.__default_condition = "OR"
        return self

    def get_default_condition(self):
        """
        Returns the default condition.
        :return:
        """
        return self.__default_condition

    def get_conditions(self):
        """
        Returns a copy of the current WHERE conditions list.
        :return:
        """
        return self.__conditions.copy()

    def _get_where_sql(self) -> str:
        """
        Returns the WHERE clause SQL statement.
        :return:
        """
        if not self.__conditions:
            return ""
        return "WHERE " + " ".join(self.__conditions)

    def is_conditions(self) -> bool:
        """
        Returns if conditions or not
        :return:
        """
        return bool(self.__conditions)

    @abstractmethod
    def get_sql(self) -> str:
        """
        Get the sql script that was generated
        :return:
        """
