from json import dumps
from typing import Union, Dict, List

from .base_builder import ConditionsBuilder, _get_tcn, _transform_value_valid
from .join_builder import BaseJoinExtension


class UpdateBuilder(ConditionsBuilder, BaseJoinExtension):

    def __init__(self, tb, **kwargs):
        ConditionsBuilder.__init__(self, tb, **kwargs)
        BaseJoinExtension.__init__(self, tb, **kwargs)
        # check if variable already exists, else init it
        self.__toSet = {}
        self.sureNotUseConditions = False
        self.__subSets = []
        self.__jsonBuildings = []

    def set(self, column, value: Union[str, int, None]):
        self.__toSet[_get_tcn(self.tb.table, column)] = _transform_value_valid(value)
        return self

    def join_set(self, join_table: str, join_column: str, value: [Union[str, int, None]]):
        self.__toSet[_get_tcn(join_table, join_column)] = _transform_value_valid(value)
        return self

    def im_sure_im_not_use_conditions(self, im_sure: bool = True):
        self.sureNotUseConditions = im_sure
        return self

    def execute(self):
        if not self._where_conditions and not self.sureNotUseConditions:
            raise PermissionError('Update Builder: You are not sure enough not to use where')
        cursor = self.tb.connect.get_available_cursor()
        cursor.execute(
            self.get_sql()
        )
        if self.__subSets:
            for s in self.__subSets:
                cursor.execute(s.get_sql())
        cursor._connection.commit()
        self.tb.connect.release_cursor(cursor)

    def get_sql(self) -> str:
        for x in self.__jsonBuildings:
            self.__set_json(x[0], x[1])
        sql = f"UPDATE {self.tb.table} " \
              f"{' '.join(self._joins) if self._joins else ''} " \
              f"SET " \
              f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
              f"{self._get_where_sql()};"
        return sql

    def __set_json(self, json: Dict[str, any], pop: List[str] = None):
        if pop is None:
            pop = []
        key: str
        value: any
        join_keys = [x.table for x in self._join_builders]
        for key, value in json.items():
            if isinstance(value, dict):
                if join_keys.__contains__(key) and not pop.__contains__(key):
                    for subKey, subValue in value.items(): self.join_set(key, subKey, subValue)
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
