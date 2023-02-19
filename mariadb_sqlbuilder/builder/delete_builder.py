from typing import Union

from .base_builder import ConditionsBuilder


class DeleteBuilder(ConditionsBuilder):

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.sureNotUseConditions = False

    def im_sure_im_not_use_conditions(self, im_sure: bool = True):
        self.sureNotUseConditions = im_sure
        return self

    def execute(self) -> bool:
        if not self._where_conditions and not self.sureNotUseConditions:
            raise PermissionError('Delete Builder: You are not sure enough not to use where')
        cursor = self.tb.connect.get_available_cursor()
        cursor.execute(
            self.get_sql()
        )
        cursor._connection.commit()
        self.tb.connect.release_cursor(cursor)

    def get_sql(self) -> str:
        return f"DELETE FROM {self.tb.table} " \
            f"{self._get_where_sql()};"

