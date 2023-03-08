"""
This modul is there for the basic functions of all query's
"""
from abc import ABC, abstractmethod
from typing import Union, Tuple


# get the name of a table column
def _get_tcn(table: str, column: str) -> str:
    return table + "." + column


def _transform_value_valid(value: Union[str, int]) -> str:
    if value is None:
        return "NULL"
    elif isinstance(value, int):
        return str(value)
    return f"'{value}'"


class BaseBuilder(ABC):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        self._tb = tb
        self.__kwargs = kwargs

    @abstractmethod
    def get_sql(self) -> str:
        """
        Get the sql script that was generated
        :return:
        """
        pass

    @property
    def tb(self):
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

    def where(self, column: str, value: Union[str, int], filter_operator: str = "="):
        """
        Adds a WHERE condition for an exact match of a column value.
        :param column:
        :param value:
        :param filter_operator:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} {filter_operator} "
                                      f"{_transform_value_valid(value)}")
        return self

    def where_in(self, column: str, checked_list: Tuple[str, int]):
        """
        Adds a WHERE condition for a list of checked values in a column.
        :param column:
        :param checked_list:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IN {str(checked_list)}")
        return self

    def where_in_not(self, column: str, checked_list: Tuple[str, int]):
        """
        Adds a WHERE condition for a list of unchecked values in a column.
        :param column:
        :param checked_list:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} NOT IN {str(checked_list)}")
        return self

    def like(self, column: str, value: Union[str, int]):
        """
        Adds a WHERE condition for a partial match of a column value.
        :param column:
        :param value:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(
            f"{_get_tcn(self.tb.table, column)} LIKE {_transform_value_valid(value)}"
        )
        return self

    def like_not(self, column: str, value: Union[str, int]):
        """
        Adds a WHERE condition for a partial mismatch of a column value.
        :param column:
        :param value:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(
            f"{_get_tcn(self.tb.table, column)} NOT LIKE {_transform_value_valid(value)}"
        )
        return self

    def between(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        """
        Adds a WHERE condition for a range of values in a column.
        :param column:
        :param value1:
        :param value2:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(
            f"{_get_tcn(self.tb.table, column)} "
            f"BETWEEN {_transform_value_valid(value1)} "
            f"AND {_transform_value_valid(value2)}"
        )
        return self

    def between_not(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        """
        Adds a WHERE condition for a range of values not in a column.
        :param column:
        :param value1:
        :param value2:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(
            f"{_get_tcn(self.tb.table, column)} "
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
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IS NOT NULL")
        return self

    def is_null(self, column: str):
        """
        Adds a WHERE condition for a column that is NULL.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IS NULL")
        return self

    def is_true(self, column: str):
        """
        Adds a WHERE condition for a column that is True.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IS TRUE")
        return self

    def is_not_true(self, column: str):
        """
        Adds a WHERE condition for a column that is not True.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IS NOT TRUE")
        return self

    def is_false(self, column: str):
        """
        Adds a WHERE condition for a column that is False.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IS FALSE")
        return self

    def is_not_false(self, column: str):
        """
        Adds a WHERE condition for a column that is not False.
        :param column:
        :return:
        """
        self.__check_if_or_and()
        self.__conditions.append(f"{_get_tcn(self.tb.table, column)} IS NOT FALSE")
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
        return True if self.__conditions else False

    @abstractmethod
    def get_sql(self) -> str:
        """
        Get the sql script that was generated
        :return:
        """
        pass
