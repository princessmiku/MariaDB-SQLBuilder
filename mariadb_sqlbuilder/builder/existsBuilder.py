from typing import Union

import mariadb

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder


class ExistsBuilder(BaseBuilder):


    def __init__(self, tb):
        super().__init__(tb)
        self.columnList = []

    def column(self, column: str):
        self.columnList.append(column)
        return self

    def columns(self, columns: str):
        self.columnList += columns.replace(", ", ",").split(",")
        return self

    def checkExists(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        try:
            result = executeFunctions.executeOne(
                cursor,
                self.get_sql()
            )
        except mariadb.OperationalError as e:
            if "Unknown column" in e.args[0]: result = (0,)
            else: raise mariadb.OperationalError(e)
        self.tb.connect.makeCursorAvailable(cursor)
        return bool(result[0])

    def get_sql(self) -> str:
        return f"SELECT EXISTS(SELECT {', '.join(self.columnList) if self.columnList else '*'} FROM {self.tb.table} " \
               f"{'WHERE ' + ' AND '.join(self._where_conditions) if self._where_conditions else ''})"
