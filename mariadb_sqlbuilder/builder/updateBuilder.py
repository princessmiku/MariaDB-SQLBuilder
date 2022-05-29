from typing import Union

from ..execution import executeFunctions
from .baseBuilder import ConditionsBuilder, _getTCN, _transformValueValid
from .joinBuilder import BaseJoinExtension


class UpdateBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb):
        super().__init__(tb)
        # check if variable already exists, else init it
        self.__toSet = {}
        self.sureNotUseWhere = False

    def set(self, column, value: Union[str, int, None]):
        self.__toSet[_getTCN(self.tb.table, column)] = _transformValueValid(value)
        return self

    def joinSet(self, joinTable: str, joinColumn: str, value: [Union[str, int, None]]):
        self.__toSet[_getTCN(joinTable, joinColumn)] = _transformValueValid(value)
        return self

    def imSureImNotUseWhere(self, imSure: bool = False):
        self.sureNotUseWhere = imSure

    def execute(self) -> bool:
        if not self._where_conditions and not self.sureNotUseWhere:
            raise PermissionError('You are not sure enough not to use where')
        cursor = self.tb.connect.getAvailableCursor()
        result = executeFunctions.execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result


    def get_sql(self) -> str:
        return f"UPDATE {self.tb.table} " \
               f"{' '.join(self.__joins) if self.__joins else ''} " \
               f"SET " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
            f"{'WHERE ' + ' AND '.join(self._where_conditions) if self._where_conditions else ''}"

