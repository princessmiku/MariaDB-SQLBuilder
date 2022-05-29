from typing import Union

from ..execution import executeFunctions
from .baseBuilder import ConditionsBuilder, _getTCN, _transformValueValid
from .joinBuilder import BaseJoinExtension


class UpdateBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb):
        ConditionsBuilder.__init__(self, tb)
        BaseJoinExtension.__init__(self, tb)
        # check if variable already exists, else init it
        self.__toSet = {}
        self.sureNotUseConditions = False

    def set(self, column, value: Union[str, int, None]):
        self.__toSet[_getTCN(self.tb.table, column)] = _transformValueValid(value)
        return self

    def joinSet(self, joinTable: str, joinColumn: str, value: [Union[str, int, None]]):
        self.__toSet[_getTCN(joinTable, joinColumn)] = _transformValueValid(value)
        return self

    def imSureImNotUseConditions(self, imSure: bool = False):
        self.sureNotUseConditions = imSure
        return self

    def execute(self) -> bool:
        if not self._where_conditions and not self.sureNotUseConditions:
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
               f"{' '.join(self._joins) if self._joins else ''} " \
               f"SET " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
            f"{self._getWhereSQL()}"

