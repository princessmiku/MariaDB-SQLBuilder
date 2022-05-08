from typing import Union

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder


class DeleteBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.sureNotUseWhere = False

    def imSureImNotUseWhere(self, imSure: bool = False):
        self.sureNotUseWhere = imSure
        return self

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
        return f"DELETE FROM {self.tb.table} " \
            f"{'WHERE ' + ' AND '.join(self._where_conditions) if self._where_conditions else ''}"

