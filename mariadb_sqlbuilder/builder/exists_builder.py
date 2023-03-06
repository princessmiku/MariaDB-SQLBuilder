from typing import Union

import mariadb

from .base_builder import ConditionsBuilder


class ExistsBuilder(ConditionsBuilder):

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.column_list = []

    def column(self, column: str):
        self.column_list.append(column)
        return self

    def columns(self, columns: str):
        self.column_list += columns.replace(", ", ",").split(",")
        return self

    def check_exists(self) -> bool:
        cursor = self.tb.connect.get_available_cursor()
        try:
            cursor.execute(
                self.get_sql()
            )
            result = cursor.fetchone()
        except mariadb.OperationalError as err:
            if "Unknown column" in err.args[0]: result = (0,)
            else: raise mariadb.OperationalError(err)
        self.tb.connect.release_cursor(cursor)
        if result is None:
            return False
        return bool(result[0])

    def get_sql(self) -> str:
        if not self.column_list and not self._where_conditions:
            return f"SHOW TABLES LIKE '{self.tb.table}'"
        return f"SELECT EXISTS(SELECT {', '.join(self.column_list) if self.column_list else '*'} FROM {self.tb.table} " \
               f"{self._get_where_sql() if self._where_conditions else ''});"
