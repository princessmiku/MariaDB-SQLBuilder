from typing import Union

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder


# get the name of a table column
def _getTCN(table: str, column: str) -> str:
    return table + "." + column


class DeleteBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.__where_conditions = []
        self.sureNotUseWhere = False

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{_getTCN(self.tb.table, column)} = {value}")
        else:
            self.__where_conditions.append(f"{_getTCN(self.tb.table, column)} = '{value}'")
        return self

    def imSureImNotUseWhere(self, imSure: bool = False):
        self.sureNotUseWhere = imSure
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        if not self.__where_conditions and not self.sureNotUseWhere:
            raise PermissionError('You are not sure enough not to use where')
        result = executeFunctions.execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"DELETE FROM {self.tb.table} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"

