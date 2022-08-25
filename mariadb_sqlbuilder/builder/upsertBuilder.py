from typing import Union, Dict

from execution.executeFunctions import executeScript
from .baseBuilder import BaseBuilder, _transformValueValid


class UpsertBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.tb = tb
        self.__toSet = {}

    def set(self, column: str, value: Union[str, int, None]):
        if not self.__toSet.__contains__(self.tb.table):
            self.__toSet[self.tb.table] = {}
        self.__toSet[self.tb.table][column] = _transformValueValid(value)
        return self

    def tableSet(self, table: str, column: str, value: Union[str, int, None]):
        """
        Insert data in other table in one insert
        :param table:
        :param column:
        :param value:
        :return:
        """
        if not self.__toSet.__contains__(table):
            self.__toSet[table] = {}
        self.__toSet[table][column] = _transformValueValid(value)
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = executeScript(
            cursor,
            self.get_sql()
        )
        cursor._connection.commit()
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        sql = ""
        _key: str
        _value: Dict[str, dict]
        for _key, _value in self.__toSet.items():
            sql += f"INSERT INTO " \
                   f"{_key} ({', '.join(_value.keys())}) VALUES ({', '.join(_value.values())})" \
                   f"ON DUPLICATE KEY UPDATE " \
                   f"{', '.join(['%s = %s' % (key, value) for (key, value) in _value.items()])};"
        return sql