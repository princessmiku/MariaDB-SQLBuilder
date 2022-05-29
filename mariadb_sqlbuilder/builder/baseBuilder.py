from abc import ABC, abstractmethod
from typing import Union


# get the name of a table column
def _getTCN(table: str, column: str) -> str:
    return table + "." + column


def _transformValueValid(value: Union[str, int]) -> str:
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

    def where(self, column: str, value: Union[str, int], filter_operator: str = "="):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} {filter_operator} {_transformValueValid(value)}")
        return self

    def whereIn(self, column: str, checkedList: tuple[str, int]):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IN {str(checkedList)}")
        return self

    def whereInNot(self, column: str, checkedList: tuple[str, int]):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} NOT IN {str(checkedList)}")
        return self

    def like(self, column: str, value: Union[str, int]):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} LIKE {_transformValueValid(value)}")
        return self

    def likeNot(self, column: str, value: Union[str, int]):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} NOT LIKE {_transformValueValid(value)}")
        return self

    def between(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} BETWEEN {_transformValueValid(value1)} AND {_transformValueValid(value2)}")
        return self

    def betweenNot(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} NOT BETWEEN {_transformValueValid(value1)} AND {_transformValueValid(value2)}")
        return self

    def isNotNull(self, column: str):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NOT NULL")
        return self

    def isNull(self, column: str):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NULL")
        return self

    def isTrue(self, column: str):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS TRUE")
        return self

    def isNotTrue(self, column: str):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NOT TRUE")
        return self

    def isFalse(self, column: str):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS FALSE")
        return self

    def isNotFalse(self, column: str):
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NOT FALSE")
        return self

    @abstractmethod
    def get_sql(self) -> str:
        pass
