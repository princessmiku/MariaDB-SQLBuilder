"""
This modul is there for build sql joins for your query

Maria DB SQL joins
https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
from abc import ABC, abstractmethod

from .base_builder import _get_tcn


class _JoinBuilder(ABC):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self):
        self.from_table = ''
        pass

    @abstractmethod
    def get_sql(self) -> str:
        """
        Abstract method that should be implemented by the subclasses.
        :return:
        """
        pass


class BaseJoinExtension:
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        self.tb = tb
        self._join_builders = []
        self._joins = []
        self.__kwargs = kwargs

    def join(self, join_builder: _JoinBuilder):
        """
        Adds a join statement to the query.
        :param join_builder:
        :return:
        """
        join_builder.from_table = self.tb.table
        self._join_builders.append(join_builder)
        self._joins.append(join_builder.get_sql())
        return self


class CrossJoinBuilder(_JoinBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, table: str, **kwargs):
        """
        Adds a join statement to the query.
        :param table:
        :param kwargs:
        """
        super().__init__()
        self.table = table
        self.__kwargs = kwargs

    def get_sql(self) -> str:
        """
        Builds the SQL query for the CROSS JOIN statement.
        :return:
        """
        return f"CROSS JOIN {self.table} "


class _ConditionsBuilder(_JoinBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, table: str):
        super().__init__()
        self.table = table
        self.conditions = []

    def condition(self, column_from_table: str, column_join_table: str):
        """
        Adds a join condition to the query.
        :param column_from_table:
        :param column_join_table:
        :return:
        """
        self.conditions.append([column_from_table, column_join_table])
        return self

    @abstractmethod
    def get_sql(self) -> str:
        """
        Abstract method that should be implemented by the subclasses.
        :return:
        """
        pass


class InnerJoinBuilder(_ConditionsBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def get_sql(self) -> str:
        """
        Builds the SQL query for the INNER JOIN statement.
        :return:
        """
        conditions = []
        for con in self.conditions:
            conditions.append(
                f"{_get_tcn(self.from_table, con[0])} = {_get_tcn(self.table, con[1])}"
            )
        return f"INNER JOIN {self.table} ON {' AND '.join(conditions)} "


class LeftJoinBuilder(_ConditionsBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def get_sql(self) -> str:
        """
        Returns a string representation of the left join operation between the two tables.
        :return:
        """
        conditions = []
        for con in self.conditions:
            conditions.append(
            f"{_get_tcn(self.from_table, con[0])} = {_get_tcn(self.table, con[1])}")
        return f"Left JOIN {self.table} ON {' AND '.join(conditions)} "


class RightJoinBuilder(_ConditionsBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def get_sql(self) -> str:
        """
        Returns a string representation of the right join operation between the two tables.
        :return:
        """
        conditions = []
        for con in self.conditions:
            conditions.append(
                f"{_get_tcn(self.from_table, con[0])} = {_get_tcn(self.table, con[1])}"
            )
        return f"RIGHT JOIN {self.table} ON {' AND '.join(conditions)} "
