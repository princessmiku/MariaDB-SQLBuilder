from typing import Union

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder
from .joinBuilder import _JoinBuilder


# get the name of a table column
def _getTCN(table: str, column: str) -> str:
    return table + "." + column


class UpdateBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.__toSet = {}
        self.__where_conditions = []
        self.__joins = []

    def set(self, column, value: Union[str, int, None]):
        if isinstance(value, int):
            self.__toSet[_getTCN(self.tb.table, column)] = f"{str(value)}"
        elif value is None:
            self.__toSet[_getTCN(self.tb.table, column)] = f"NULL"
        else:
            self.__toSet[_getTCN(self.tb.table, column)] = f"'{str(value)}'"
        return self

    def join(self, joinBuilder: _JoinBuilder):
        joinBuilder.from_table = self.tb.table
        self.__joins.append(joinBuilder.get_sql())
        return self

    def joinSet(self, joinTable: str, joinColumn: str, value: [Union[str, int, None]]):
        if isinstance(value, int):
            self.__toSet[_getTCN(joinTable, joinColumn)] = f"{str(value)}"
        elif value is None:
            self.__toSet[_getTCN(joinTable, joinColumn)] = f"NULL"
        else:
            self.__toSet[_getTCN(joinTable, joinColumn)] = f"'{str(value)}'"
        return self

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{_getTCN(self.tb.table, column)} = {value}")
        else:
            self.__where_conditions.append(f"{_getTCN(self.tb.table, column)} = '{value}'")
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = executeFunctions.execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result


    def get_sql(self) -> str:
        return f"UPDATE {self.tb.table} " \
               f"{' '.join(self.__joins) if self.__joins else ''} " \
               f"SET " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"

