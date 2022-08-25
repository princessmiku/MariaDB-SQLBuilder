import abc
from json import dumps
from typing import Union, Dict, List

from .dummy import TableBuilder
from ..execution import executeFunctions
from .baseBuilder import BaseBuilder, _transformValueValid


class InsertBuilder(BaseBuilder):

    def __init__(self, tb):
        super().__init__(tb)
        self.__ignore = False
        self.__toSet = {}
        self.__subSets = []

    def set(self, column: str, value: Union[str, int, None]):
        self.__toSet[column] = _transformValueValid(value)
        return self

    def ignore(self, _ignore: bool = True):
        self.__ignore = _ignore
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = executeFunctions.execute(
            cursor,
            self.get_sql()
        )
        if self.__subSets:
            for s in self.__subSets:
                executeFunctions.execute(cursor, s.get_sql())
        cursor._connection.commit()
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        sql = f"INSERT {'IGNORE ' if self.__ignore else ''}INTO " \
            f"{self.tb.table} ({', '.join(self.__toSet.keys())}) VALUES ({', '.join(self.__toSet.values())});"
        if self.__subSets:
            for x in self.__subSets:
                sql += "\n" + x.get_sql()
        return sql

    def set_json(self, json: Dict[str, any], join: Union[bool, List[str]] = False, pop: List[str] = None):
        """
        Set values with a json
        :param json: dict with data example from select
        :param join: should if join in join tables and edit the data? Set specific keys of the json or use a detection,
        but there will be problems if you have json formats in individual keys that are not intended for join.
        :param pop: pop keys from the json, if you have joins in select that not should insert
        :return:
        """
        key: str
        value: any
        for key, value in zip(json.keys(), json.values()):
            if isinstance(value, dict):
                if isinstance(join, list):
                    if key in join: self.__subSets.append(InsertBuilder(TableBuilder(self.tb.connect, key)).set_json(value))
                    else: self.set(key, dumps(value))
                else:
                    if join: self.__subSets.append(InsertBuilder(TableBuilder(self.tb.connect, key)).set_json(value))
                    else: self.set(key, dumps(value))
            else:
                self.set(key, value)
        return self
