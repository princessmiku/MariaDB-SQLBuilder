from typing import Union

from execution.executeFunctions import executeAll, executeOne
from .baseBuilder import ConditionsBuilder, _getTCN
from .joinBuilder import BaseJoinExtension
from .dict_converter import convert_to_dict_single, convert_to_dict_all


class SelectBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb, column):
        ConditionsBuilder.__init__(self, tb)
        BaseJoinExtension.__init__(self, tb)
        self.column = [_getTCN(self.tb.table, c) for c in column.replace(", ", ",").split(",")]

    def joinSelect(self, joinTable: str, column: str):
        column = column.replace(", ", ",").split(",")
        columns = []
        [columns.append(_getTCN(joinTable, c)) for c in column]
        self.column += columns
        return self

    def columnSelect(self, column: str):
        column = column.replace(", ", ",").split(",")
        columns = []
        [columns.append(_getTCN(self.tb.table, c)) for c in column]
        self.column += columns
        return self

    def fetchone(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = executeOne(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchone_json(self):
        return convert_to_dict_single(self.tb.table, self.column, self.fetchone())

    def fetchall(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = executeAll(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchall_json(self):
        return convert_to_dict_all(self.tb.table, self.column, self.fetchall())

    def get_sql(self) -> str:
        return f"SELECT {', '.join(self.column)} FROM {self.tb.table} " \
               f"{' '.join(self._joins) if self._joins else ''} " \
            f"{self._getWhereSQL()};"
