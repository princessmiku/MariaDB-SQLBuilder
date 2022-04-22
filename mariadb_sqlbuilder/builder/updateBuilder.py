from typing import Union

import builder
from builder.baseBuilder import BaseBuilder


class UpdateBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.__toSet = {}
        self.__where_conditions = []

    def set(self, column, value: Union[str, int, None]):
        if isinstance(value, int):
            self.__toSet[column] = f"{str(value)}"
        elif value is None:
            self.__toSet[column] = f"NULL"
        else:
            self.__toSet[column] = f"'{str(value)}'"
        return self

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{column} = {value}")
        else:
            self.__where_conditions.append(f"{column} = '{value}'")
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = builder.execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result


    def get_sql(self) -> str:
        return f"UPDATE {self.tb.table} SET " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"

