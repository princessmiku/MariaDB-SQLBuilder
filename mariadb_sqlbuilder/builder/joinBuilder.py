"""
    Maria DB SQL joins
    https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
from abc import ABC, abstractmethod, ABCMeta
from typing import Union

from .baseBuilder import _getTCN


class _JoinBuilder(ABC):

    def __init__(self):
        self.from_table = ''
        pass

    @abstractmethod
    def get_sql(self) -> str:
        pass


class BaseJoinExtension:

    def __init__(self, tb):
        self.tb = tb
        self._joins = []

    def join(self, joinBuilder: _JoinBuilder):
        joinBuilder.from_table = self.tb.table
        self._joins.append(joinBuilder.get_sql())
        return self


class CrossJoinBuilder(_JoinBuilder):

    def __init__(self, table: str):
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
        for con in self.conditions: conditions.append(f"{_getTCN(self.from_table, con[0])} = {_getTCN(self.table, con[1])}")
        return f"INNER JOIN {self.table} ON {' AND '.join(conditions)} "


class LeftJoinBuilder(_ConditionsBuilder):

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(
            f"{_getTCN(self.from_table, con[0])} = {_getTCN(self.table, con[1])}")
        return f"Left JOIN {self.table} ON {' AND '.join(conditions)} "


class RightJoinBuilder(_ConditionsBuilder):

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(f"{_getTCN(self.from_table, con[0])} = {_getTCN(self.table, con[1])}")
        return f"RIGHT JOIN {self.table} ON {' AND '.join(conditions)} "
