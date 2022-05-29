from typing import Union

from ..execution import executeFunctions
from .baseBuilder import ConditionsBuilder


class DeleteBuilder(ConditionsBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.sureNotUseConditions = False

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
        return f"DELETE FROM {self.tb.table} " \
            f"{self._getWhereSQL()}"

