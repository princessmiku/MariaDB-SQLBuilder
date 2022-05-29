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
        self.__defaultCondition = "AND"

    def where(self, column: str, value: Union[str, int], filter_operator: str = "="):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} {filter_operator} {_transformValueValid(value)}")
        return self

    def whereIn(self, column: str, checkedList: tuple[str, int]):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IN {str(checkedList)}")
        return self

    def whereInNot(self, column: str, checkedList: tuple[str, int]):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} NOT IN {str(checkedList)}")
        return self

    def like(self, column: str, value: Union[str, int]):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} LIKE {_transformValueValid(value)}")
        return self

    def likeNot(self, column: str, value: Union[str, int]):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} NOT LIKE {_transformValueValid(value)}")
        return self

    def between(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} BETWEEN {_transformValueValid(value1)} AND {_transformValueValid(value2)}")
        return self

    def betweenNot(self, column: str, value1: Union[str, int], value2: Union[str, int]):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} NOT BETWEEN {_transformValueValid(value1)} AND {_transformValueValid(value2)}")
        return self

    def isNotNull(self, column: str):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NOT NULL")
        return self

    def isNull(self, column: str):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NULL")
        return self

    def isTrue(self, column: str):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS TRUE")
        return self

    def isNotTrue(self, column: str):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NOT TRUE")
        return self

    def isFalse(self, column: str):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS FALSE")
        return self

    def isNotFalse(self, column: str):
        self.__checkIfORAND()
        self._where_conditions.append(f"{_getTCN(self.tb.table, column)} IS NOT FALSE")
        return self

    def __checkIfORAND(self):
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

    def defaultAND(self):
        self.__defaultCondition = "AND"
        return self

    def defaultOR(self):
        self.__defaultCondition = "OR"
        return self

    def _getWhereSQL(self) -> str:
        if not self._where_conditions: return ""
        return "WHERE " + " ".join(self._where_conditions)

    @abstractmethod
    def get_sql(self) -> str:
        pass
