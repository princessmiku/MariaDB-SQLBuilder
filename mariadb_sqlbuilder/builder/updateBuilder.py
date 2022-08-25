from json import dumps
from typing import Union, Dict, List

from .dummy import TableBuilder
from ..execution import executeFunctions
from .baseBuilder import ConditionsBuilder, _getTCN, _transformValueValid
from .joinBuilder import BaseJoinExtension, _ConditionsBuilder


class UpdateBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb):
        ConditionsBuilder.__init__(self, tb)
        BaseJoinExtension.__init__(self, tb)
        # check if variable already exists, else init it
        self.__toSet = {}
        self.sureNotUseConditions = False
        self.__subSets = []
        self.__jsonBuildings = []

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
            raise PermissionError('Update Builder: You are not sure enough not to use where')
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
        for x in self.__jsonBuildings:
            self.__set_json(x[0], x[1])
        sql = f"UPDATE {self.tb.table} " \
              f"{' '.join(self._joins) if self._joins else ''} " \
              f"SET " \
              f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
              f"{self._getWhereSQL()};"
        return sql

    def __set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set values with a json, don't forget where
        :param json: dict with data example from select
        :param pop: pop keys from the json, if you have joins in select that not should insert
        :return:
        """
        if pop is None:
            pop = []
        key: str
        value: any
        join_keys = [x.table for x in self._joinBuilders]
        print(join_keys)
        for key, value in json.items():
            if isinstance(value, dict):
                if join_keys.__contains__(key) and not pop.__contains__(key):
                    for subKey, subValue in value.items(): self.joinSet(key, subKey, subValue)
                else:
                    self.set(key, dumps(value))
            else:
                self.set(key, value)
        return self

    def set_json(self, json: Dict[str, any], pop: List[str] = None):
        self.__jsonBuildings.append([json, pop])
        return self
