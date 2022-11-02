import abc
from json import dumps
from typing import Union, Dict, List

from .dummy import TableBuilder
from ..execution.executeFunctions import executeScript
from .baseBuilder import BaseBuilder, _transformValueValid


class InsertBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.__ignore = False
        self.__toSet = {}
        self.__jsonBuildings = []

    def set(self, column: str, value: Union[str, int, None]):
        if not self.__toSet.__contains__(self.tb.table):
            self.__toSet[self.tb.table] = {}
        self.__toSet[self.tb.table][column] = _transformValueValid(value)
        return self

    def addJoinTable(self, table: str):
        if self.__toSet.__contains__(table): return self
        self.__toSet[table] = {}
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
        for x in self.__jsonBuildings:
            self.__set_json(x[0], x[1])
        sql = ""
        key: str
        value: Dict[str, dict]
        for key, value in self.__toSet.items():
            if not value: continue
            sql += f"INSERT {'IGNORE ' if self.__ignore else ''}INTO " \
                   f"{key} ({', '.join(value.keys())}) VALUES ({', '.join(value.values())});"
        return sql

    def __set_json(self, json: Dict[str, any], pop: List[str] = None):
        if pop is None:
            pop = []
        key: str
        value: any
        join_keys = [x for x in self.__toSet.keys()]
        for key, value in json.items():
            if isinstance(value, dict):
                if join_keys.__contains__(key) and not pop.__contains__(key):
                    for subKey, subValue in value.items(): self.tableSet(key, subKey, subValue)
                else:
                    self.set(key, dumps(value))
            else:
                self.set(key, value)
        return self

    def set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set values with a json, don't forget where
        :param json: dict with data example from select
        :param pop: pop keys from the json, if you have keys inside that are not a table but a dict/list
        :return:
        """
        self.__jsonBuildings.append([json, pop])
        return self
