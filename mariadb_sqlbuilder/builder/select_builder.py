from typing import Union

import mariadb

from .base_builder import ConditionsBuilder, _get_tcn
from .join_builder import BaseJoinExtension
from .dict_converter import convert_to_dict_single, convert_to_dict_all


class SelectBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb, column, **kwargs):
        ConditionsBuilder.__init__(self, tb, **kwargs)
        BaseJoinExtension.__init__(self, tb, **kwargs)
        self.column = [_get_tcn(self.tb.table, c) for c in column.replace(", ", ",").split(",")]

    def join_select(self, join_table: str, column: str):
        column = column.replace(", ", ",").split(",")
        columns = []
        [columns.append(_get_tcn(join_table, c)) for c in column]
        self.column += columns
        return self

    def column_select(self, column: str):
        column = column.replace(", ", ",").split(",")
        columns = []
        [columns.append(_get_tcn(self.tb.table, c)) for c in column]
        self.column += columns
        return self

    def fetchone(self):
        cursor = self.tb.connect.getAvailableCursor()
        cursor.execute(
            self.get_sql()
        )
        result = cursor.fetchone()
        cursor.connection.commit()
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchone_json(self):
        return convert_to_dict_single(self.tb.table, self.column, self.fetchone())

    def fetchall(self):
        cursor = self.tb.connect.get_available_cursor()
        cursor.execute(
            self.get_sql()
        )
        result = cursor.fetchall()
        cursor.connection.commit()
        self.tb.connect.release_cursor(cursor)
        return result

    def fetchall_json(self):
        return convert_to_dict_all(self.tb.table, self.column, self.fetchall())

    def get_sql(self) -> str:
        return f"SELECT {', '.join(self.column)} FROM {self.tb.table} " \
               f"{' '.join(self._joins) if self._joins else ''} " \
            f"{self._get_where_sql()};"
