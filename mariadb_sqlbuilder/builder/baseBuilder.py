from abc import ABC, abstractmethod
from typing import Union, Tuple


# get the name of a table column
def _get_tcn(table: str, column: str) -> str:
    return table + "." + column


def _transform_value_valid(value: Union[str, int]) -> str:
    if value is None: return "NULL"
    elif isinstance(value, int): return str(value)
    else: return f"'{value}'"


class BaseBuilder(ABC):

    def __init__(self, tb):
        self.tb = tb

    @abstractmethod
    def get_sql(self) -> str:
        pass


class ConditionsBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self._where_conditions = []
        self.__defaultCondition = "AND"

    def where(self, column: str, value: Union[str, int], filter_operator: str = "="):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} {filter_operator} "
                                      f"{_transform_value_valid(value)}")
        return self

    def where_in(self, column: str, checked_list: Tuple[str, int]):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IN {str(checked_list)}")
        return self

    def where_in_not(self, column: str, checked_list: Tuple[str, int]):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} NOT IN {str(checked_list)}")
        return self

    def like(self, column: str, value: Union[str, int]):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} LIKE {_transform_value_valid(value)}")
        return self

    def like_not(self, column: str, value: Union[str, int]):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} NOT LIKE {_transform_value_valid(value)}")
        return self

    def between(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} BETWEEN {_transform_value_valid(value1)} AND "
                                      f"{_transform_value_valid(value2)}")
        return self

    def between_not(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} NOT BETWEEN {_transform_value_valid(value1)} "
                                      f"AND {_transform_value_valid(value2)}")
        return self

    def is_not_null(self, column: str):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IS NOT NULL")
        return self

    def is_null(self, column: str):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IS NULL")
        return self

    def is_true(self, column: str):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IS TRUE")
        return self

    def is_not_true(self, column: str):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IS NOT TRUE")
        return self

    def is_false(self, column: str):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IS FALSE")
        return self

    def is_not_false(self, column: str):
        self.__check_if_or_and()
        self._where_conditions.append(f"{_get_tcn(self.tb.table, column)} IS NOT FALSE")
        return self

    def __check_if_or_and(self):
        if not self._where_conditions: return
        if self._where_conditions[-1] not in ["AND", "OR"]: self._where_conditions.append(self.__defaultCondition)

    def OR(self):
        if not self._where_conditions: return
        elif self._where_conditions[-1] == "OR": return
        elif self._where_conditions[-1] == "AND": self._where_conditions.pop(-1)
        self._where_conditions.append("OR")
        return self

    def AND(self):
        if not self._where_conditions: return
        elif self._where_conditions[-1] == "AND": return
        elif self._where_conditions[-1] == "OR": self._where_conditions.pop(-1)
        self._where_conditions.append("AND")
        return self

    def default_and(self):
        self.__defaultCondition = "AND"
        return self

    def default_or(self):
        self.__defaultCondition = "OR"
        return self

    def _get_where_sql(self) -> str:
        if not self._where_conditions: return ""
        return "WHERE " + " ".join(self._where_conditions)

    @abstractmethod
    def get_sql(self) -> str:
        pass
