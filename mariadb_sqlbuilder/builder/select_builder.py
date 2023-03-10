"""
This modul is there for build a sql select query
"""
from typing import Union

from mariadb_sqlbuilder.helpful.arithmetic import Arithmetic
from .base_builder import ConditionsBuilder, _get_tcn
from .dict_converter import convert_to_dict_single, convert_to_dict_all
from .join_builder import BaseJoinExtension


class SelectBuilder(ConditionsBuilder, BaseJoinExtension):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, expressions: Union[str, list], *args, **kwargs):
        ConditionsBuilder.__init__(self, tb, **kwargs)
        BaseJoinExtension.__init__(self, tb, **kwargs)
        self._contains_arithmetic = False
        self.expressions = []
        self._loop_tb_expressions_add(self.tb.table, expressions, *args)

    def join_select(self, join_table: str, expressions: Union[str, list], *args):
        """
        Adds a JOIN clause to the SELECT query with the provided table and column.
        :param join_table:
        :param expressions:
        :return:
        """
        self._loop_tb_expressions_add(join_table, expressions, *args)
        return self

    def column_select(self, expressions: Union[str, list], *args):
        """
        Adds additional columns to the SELECT query.
        :param expressions:
        :return:
        """
        self._loop_tb_expressions_add(self.tb.table, expressions, *args)
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
        return f"SELECT {', '.join(self.expressions)} FROM {self.tb.table} " \
               f"{' '.join(self._joins) if self._joins else ''} " \
            f"{self._get_where_sql()};"

    def _loop_tb_expressions_add(self, tb: str, expressions: Union[str, Arithmetic], *args):
        """
        Handle different types of expressions and add it correctly in the expressions list
        :param tb:
        :param expressions:
        :param args:
        :return:
        """
        if isinstance(expressions, str):
            self.expressions += [_get_tcn(tb, c) for c in expressions.replace(", ", ",").split(",")]
        if isinstance(expressions, list) or args:
            loop_expressions = []
            if isinstance(expressions, list):
                loop_expressions += expressions
            if args:
                loop_expressions += args
            for expression in loop_expressions:
                if isinstance(expression, Arithmetic):
                    self._contains_arithmetic = True
                    self.expressions.append(str(expression))
                else:
                    self.expressions.append(_get_tcn(self.tb.table, expression))
