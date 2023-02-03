from typing import Union

import mariadb

from .baseBuilder import ConditionsBuilder


class ExistsBuilder(ConditionsBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.columnList = []

    def column(self, column: str):
        self.columnList.append(column)
        return self

    def columns(self, columns: str):
        self.columnList += columns.replace(", ", ",").split(",")
        return self

    def check_exists(self) -> bool:
        cursor = self.tb.connect.get_available_cursor()
        try:
            result = cursor.execute(
                cursor,
                self.get_sql()
            )
        except mariadb.OperationalError as e:
            if "Unknown column" in e.args[0]: result = (0,)
            else: raise mariadb.OperationalError(e)
        self.tb.connect.release_cursor(cursor)
        return bool(result[0])

    def get_sql(self) -> str:
        return f"SELECT EXISTS(SELECT {', '.join(self.columnList) if self.columnList else '*'} FROM {self.tb.table} " \
               f"{'WHERE ' + ' AND '.join(self._where_conditions) if self._where_conditions else ''});"
