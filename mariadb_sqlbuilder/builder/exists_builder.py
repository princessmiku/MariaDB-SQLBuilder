from typing import Union

import mariadb

from .base_builder import ConditionsBuilder


class ExistsBuilder(ConditionsBuilder):

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
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
            cursor.execute(
                self.get_sql()
            )
            result = cursor.fetchone()
        except mariadb.OperationalError as e:
            if "Unknown column" in e.args[0]: result = (0,)
            else: raise mariadb.OperationalError(e)
        self.tb.connect.release_cursor(cursor)
        if result is None:
            return False
        return bool(result[0])

    def get_sql(self) -> str:
        if not self.columnList and not self._where_conditions:
            return f"SHOW TABLES LIKE '{self.tb.table}'"
        return f"SELECT EXISTS(SELECT {', '.join(self.columnList) if self.columnList else '*'} FROM {self.tb.table} " \
               f"{self._get_where_sql() if self._where_conditions else ''});"
