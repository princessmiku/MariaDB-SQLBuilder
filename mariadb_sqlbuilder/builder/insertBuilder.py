from typing import Union

import builder


class InsertBuilder:

    def __init__(self, tb):
        self.tb = tb
        self.__ignore = False
        self.__toSet = {}

    def set(self, column, value: Union[str, int, None]):
        if isinstance(value, int):
            self.__toSet[column] = f"{str(value)}"
        elif value is None:
            self.__toSet[column] = f"NULL"
        else:
            self.__toSet[column] = f"'{str(value)}'"
        return self

    def ignore(self, _ignore: bool = True):
        self.__ignore = _ignore
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
        return f"INSERT {'IGNORE ' if self.__ignore else ''}INTO " \
            f"{self.tb.table} ({', '.join(self.__toSet.keys())}) VALUES ({', '.join(self.__toSet.values())})"

