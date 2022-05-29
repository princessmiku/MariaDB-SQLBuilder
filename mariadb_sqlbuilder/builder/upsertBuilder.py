from typing import Union

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder, _transformValueValid


class UpsertBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.tb = tb
        self.__toSet = {}

    def set(self, column, value: Union[str, int, None]):
        self.__toSet[column] = _transformValueValid(value)
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = executeFunctions.execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"INSERT INTO " \
            f"{self.tb.table} ({', '.join(self.__toSet.keys())}) VALUES ({', '.join(self.__toSet.values())})" \
            f"ON DUPLICATE KEY UPDATE " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])}"
