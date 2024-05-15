"""
This modul is there to check your database of existing entry's
"""
import mariadb

from .base_builder import ConditionsBuilder


class ExistsBuilder(ConditionsBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.column_list = []

    def column(self, column: str):
        """
        Adds a column to the list of columns to select in the EXISTS subquery.
        :param column:
        :return:
        """
        self.column_list.append(column)
        return self

    def columns(self, columns: str):
        """
        Adds multiple columns to the list of columns to select in the EXISTS subquery.
        :param columns:
        :return:
        """
        self.column_list += columns.replace(", ", ",").split(",")
        return self

    def check_exists(self) -> bool:
        """
        Checks if a row exists in the table that matches the specified conditions.
        :return:
        """
        cursor = self.tb.connector.get_available_cursor()
        try:
            cursor.execute(
                self.get_sql(),
                self.values_for_execute
            )
            result = cursor.fetchone()
        except mariadb.OperationalError as err:
            if "Unknown column" in err.args[0]:
                result = (0,)
            else:
                self.tb.connector.release_cursor(cursor)
                raise mariadb.OperationalError(err)
        self.tb.connector.release_cursor(cursor)
        if result is None:
            return False
        return bool(result[0])

    def get_sql(self) -> str:
        """
        Generates the SQL query string to check for the existence of a row in the table.
        :return:
        """
        if not self.column_list and not self.is_conditions():
            return f"SHOW TABLES LIKE '{self.tb.table}'"
        return f"SELECT EXISTS(SELECT " \
               f"{', '.join(self.column_list) if self.column_list else '*'} " \
               f"FROM {self.tb.table} " \
               f"{self._get_where_sql()};"

    def __str__(self):
        return self.get_sql()
