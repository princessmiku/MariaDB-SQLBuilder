from abc import abstractmethod

from builder.base_builder import ConditionsBuilder


class _DummyTB:

    def __init__(self, table: str):
        self.__table = table

    @property
    def table(self):
        return self.__table


class ConditionsSaver(ConditionsBuilder):

    def __init__(self, table: str, **kwargs):
        super().__init__(_DummyTB(table), **kwargs)

    def get_sql(self) -> str:
        return self._get_where_sql()
