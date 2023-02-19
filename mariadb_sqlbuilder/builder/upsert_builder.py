from json import dumps
from typing import Union, Dict, List

from .base_builder import BaseBuilder, _transform_value_valid


class UpsertBuilder(BaseBuilder):

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.tb = tb
        self.__toSet = {}
        self.__jsonBuildings = []

    def set(self, column: str, value: Union[str, int, None]):
        if not self.__toSet.__contains__(self.tb.table):
            self.__toSet[self.tb.table] = {}
        self.__toSet[self.tb.table][column] = _transform_value_valid(value)
        return self

    def add_join_table(self, table: str):
        if self.__toSet.__contains__(table): return self
        self.__toSet[table] = {}
        return self

    def table_set(self, table: str, column: str, value: Union[str, int, None]):
        """
        Insert data in other table in one insert
        :param table:
        :param column:
        :param value:
        :return:
        """
        if not self.__toSet.__contains__(table):
            self.__toSet[table] = {}
        self.__toSet[table][column] = _transform_value_valid(value)
        return self

    def execute(self):
        cursor = self.tb.connect.get_available_cursor()
        cursor.execute(
            self.get_sql()
        )
        cursor._connection.commit()
        self.tb.connect.release_cursor(cursor)

    def get_sql(self) -> str:
        for x in self.__jsonBuildings:
            self.__set_json(x[0], x[1])
        sql = ""
        _key: str
        _value: Dict[str, dict]
        for _key, _value in self.__toSet.items():

            sql += f"INSERT INTO " \
                   f"{_key} ({', '.join(_value.keys())}) VALUES ({', '.join(_value.values())})" \
                   f"ON DUPLICATE KEY UPDATE " \
                   f"{', '.join(['%s = %s' % (key, value) for (key, value) in _value.items()])};"
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
                    for subKey, subValue in value.items(): self.table_set(key, subKey, subValue)
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
