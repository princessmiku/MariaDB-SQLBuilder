import abc
from json import dumps
from typing import Union, Dict, List

from .dummy import TableBuilder
from execution.executeFunctions import executeScript
from .baseBuilder import BaseBuilder, _transformValueValid


class InsertBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.__ignore = False
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

    def ignore(self, _ignore: bool = True):
        self.__ignore = _ignore
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
        key: str
        value: Dict[str, dict]
        for key, value in self.__toSet.items():
            sql += f"INSERT {'IGNORE ' if self.__ignore else ''}INTO " \
                   f"{key} ({', '.join(value.keys())}) VALUES ({', '.join(value.values())});"
        return sql
