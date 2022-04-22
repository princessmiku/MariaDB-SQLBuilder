from typing import Union

from .baseBuilder import BaseBuilder
from .joinBuilder import _JoinBuilder
import builder


class SelectBuilder(BaseBuilder):

    def __init__(self, tb, column):
        super().__init__(tb)
        self.column = column
        self.__where_conditions = []
        self.__joins = []

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{column} = {value}")
        else:
            self.__where_conditions.append(f"{column} = '{value}'")
        return self

    def join(self, joinBuilder: _JoinBuilder):
        joinBuilder.from_table = self.tb.table
        print(joinBuilder.get_sql())
        self.__joins.append(joinBuilder.get_sql())
        return self

    def fetchone(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = builder.executeOne(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchall(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = builder.executeAll(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"SELECT {self.column} FROM {self.tb.table} " \
               f"{' '.join(self.__joins) if self.__joins else ''} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"
