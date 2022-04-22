"""
    Maria DB SQL joins
    https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
from abc import ABC, abstractmethod


class _JoinBuilder(ABC):

    def __init__(self):
        self.from_table = ''
        pass

    @abstractmethod
    def get_sql(self) -> str:
        pass


class InnerJoinBuilder(_JoinBuilder):

    def __init__(self, table: str):
        super().__init__()
        self.table = table
        self.conditions = []

    def condition(self, column_from_table: str, column_join_table: str):
        self.conditions.append([column_from_table, column_join_table])
        return self

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(f"{self.from_table}.{con[0]} = {self.table}.{con[1]}")
        return f"INNER JOIN {self.table} ON {' AND '.join(conditions)} "


class CrossJoinBuilder(_JoinBuilder):

    def __init__(self, table: str):
        super().__init__()
        self.table = table

    def get_sql(self) -> str:
        return f"CROSS JOIN {self.table} "


class LeftJoinBuilder(_JoinBuilder):

    def __init__(self, table: str):
        super().__init__()
        self.table = table
        self.conditions = []

    def condition(self, column_from_table: str, column_join_table: str):
        self.conditions.append([column_from_table, column_join_table])
        return self

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(f"{self.from_table}.{con[0]} = {self.table}.{con[1]}")
        return f"Left JOIN {self.table} ON {' AND '.join(conditions)} "


class RightJoinBuilder(_JoinBuilder):


    def __init__(self, table: str):
        super().__init__()
        self.table = table
        self.conditions = []

    def condition(self, column_from_table: str, column_join_table: str):
        self.conditions.append([column_from_table, column_join_table])
        return self

    def get_sql(self) -> str:
        conditions = []
        for con in self.conditions: conditions.append(f"{self.from_table}.{con[0]} = {self.table}.{con[1]}")
        return f"RIGHT JOIN {self.table} ON {' AND '.join(conditions)} "
