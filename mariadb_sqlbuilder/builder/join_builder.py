"""
    Maria DB SQL joins
    https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
from abc import ABC, abstractmethod, ABCMeta
from typing import Union

from .base_builder import _get_tcn


class _JoinBuilder(ABC):

    def __init__(self):
        self.from_table = ''
        pass

    @abstractmethod
    def get_sql(self) -> str:
        pass


class BaseJoinExtension:

    def __init__(self, tb, **kwargs):
        self.tb = tb
        self._join_builders = []
        self._joins = []

    def join(self, join_builder: _JoinBuilder):
        join_builder.from_table = self.tb.table
        self._join_builders.append(join_builder)
        self._joins.append(join_builder.get_sql())
        return self


class CrossJoinBuilder(_JoinBuilder):

    def __init__(self, table: str, **kwargs):
        super().__init__()
        self.table = table

    def get_sql(self) -> str:
        return f"CROSS JOIN {self.table} "


class _ConditionsBuilder(_JoinBuilder):
    def __init__(self, table: str):
        super().__init__()
        self.table = table
        self.conditions = []

    def condition(self, column_from_table: str, column_join_table: str):
        self.conditions.append([column_from_table, column_join_table])
        return self

    @abstractmethod
    def get_sql(self) -> str:
        pass


class InnerJoinBuilder(_ConditionsBuilder):

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(f"{_get_tcn(self.from_table, con[0])} = {_get_tcn(self.table, con[1])}")
        return f"INNER JOIN {self.table} ON {' AND '.join(conditions)} "


class LeftJoinBuilder(_ConditionsBuilder):

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(
            f"{_get_tcn(self.from_table, con[0])} = {_get_tcn(self.table, con[1])}")
        return f"Left JOIN {self.table} ON {' AND '.join(conditions)} "


class RightJoinBuilder(_ConditionsBuilder):

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(f"{_get_tcn(self.from_table, con[0])} = {_get_tcn(self.table, con[1])}")
        return f"RIGHT JOIN {self.table} ON {' AND '.join(conditions)} "
