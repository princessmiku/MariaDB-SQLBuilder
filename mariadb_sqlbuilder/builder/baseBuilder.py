from abc import ABC, abstractmethod
from typing import Union


# get the name of a table column
def _getTCN(table: str, column: str) -> str:
    return table + "." + column


class BaseBuilder(ABC):

    def __init__(self, tb):
        self.tb = tb
        self._where_conditions = []

    @abstractmethod
    def get_sql(self) -> str:
        pass

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self._where_conditions.append(f"{_getTCN(self.tb.table, column)} = {value}")
        else:
            self._where_conditions.append(f"{_getTCN(self.tb.table, column)} = '{value}'")
        return self
