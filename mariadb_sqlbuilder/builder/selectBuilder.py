from typing import Union

import builder


class SelectBuilder:

    def __init__(self, tb, column):
        self.tb = tb
        self.column = column
        self.__where_conditions = []

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{column} = {value}")
        else:
            self.__where_conditions.append(f"{column} = '{value}'")
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
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"
