"""
This modul is there for build a sql select query
"""
from .base_builder import ConditionsBuilder, _get_tcn
from .dict_converter import convert_to_dict_single, convert_to_dict_all
from .join_builder import BaseJoinExtension


class SelectBuilder(ConditionsBuilder, BaseJoinExtension):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, column, **kwargs):
        ConditionsBuilder.__init__(self, tb, **kwargs)
        BaseJoinExtension.__init__(self, tb, **kwargs)
        self.column = [_get_tcn(self.tb.table, c) for c in column.replace(", ", ",").split(",")]

    def join_select(self, join_table: str, column: str):
        """
        Adds a JOIN clause to the SELECT query with the provided table and column.
        :param join_table:
        :param column:
        :return:
        """
        column = column.replace(", ", ",").split(",")
        columns = []
        for c in column:
            columns.append(_get_tcn(join_table, c))
        self.column += columns
        return self

    def column_select(self, column: str):
        """
        Adds additional columns to the SELECT query.
        :param column:
        :return:
        """
        column = column.replace(", ", ",").split(",")
        columns = []
        for c in column:
            columns.append(_get_tcn(self.tb.table, c))
        self.column += columns
        return self

    def fetchone(self):
        """
        Executes the SELECT query and returns the first row of the result.
        :return:
        """
        cursor = self.tb.connect.getAvailableCursor()
        cursor.execute(
            self.get_sql()
        )
        result = cursor.fetchone()
        cursor.connection.commit()
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchone_json(self):
        """
        Executes the SELECT query and returns the first row of the result in a JSON format.
        :return:
        """
        return convert_to_dict_single(self.tb.table, self.column, self.fetchone())

    def fetchall(self):
        """
        Executes the SELECT query and returns all the rows of the result.
        :return:
        """
        cursor = self.tb.connect.get_available_cursor()
        cursor.execute(
            self.get_sql()
        )
        result = cursor.fetchall()
        cursor.connection.commit()
        self.tb.connect.release_cursor(cursor)
        return result

    def fetchall_json(self):
        """
        Executes the SELECT query and returns all the rows of the result in a JSON format.
        :return:
        """
        return convert_to_dict_all(self.tb.table, self.column, self.fetchall())

    def get_sql(self) -> str:
        """
        Builds the SELECT query and returns it as a string.
        :return:
        """
        return f"SELECT {', '.join(self.column)} FROM {self.tb.table} " \
               f"{' '.join(self._joins) if self._joins else ''} " \
            f"{self._get_where_sql()};"
