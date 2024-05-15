"""
This modul is there for build a sql upsert query
"""
from datetime import timedelta, datetime
from json import dumps
from typing import Union, Dict, List

from _decimal import Decimal

from mariadb_sqlbuilder.helpful.arithmetic import Arithmetic
from .base_builder import BaseBuilder


class UpsertBuilder(BaseBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.__toSet = {}
        self.__jsonBuildings = []

    def set(self, column: str,  value: Union[str, int, float, bool,
        Arithmetic, timedelta, datetime, Decimal]):
        """
        Set a column value for the current table.
        :param column:
        :param value:
        :return:
        """
        self.tb.validator.check_value_type(self.tb.table, column, value)
        if self.tb.table not in self.__toSet:
            self.__toSet[self.tb.table] = {}
        self.__toSet[self.tb.table][column] = value
        return self

    def add_join_table(self, table: str):
        """
        Add a join table to the UpsertBuilder object.
        :param table:
        :return:
        """
        if table in self.__toSet:
            return self
        self.__toSet[table] = {}
        return self

    def table_set(self, table: str, column: str, value: Union[str, int, float, bool,
        Arithmetic, timedelta, datetime, Decimal]):
        """
        Set a column value for a specific table.
        :param table:
        :param column:
        :param value:
        :return:
        """
        self.tb.validator.check_value_type(table, column, value)
        if table not in self.__toSet:
            self.__toSet[table] = {}
        self.__toSet[table][column] = value
        return self

    def execute(self):
        """
        Execute the UpsertBuilder object's SQL query and commit the changes.
        :return:
        """
        cursor = self.tb.connector.get_available_cursor()
        cursor.execute(
            self.get_sql(),
            self.values_for_execute
        )
        cursor.connection.commit()
        self.tb.connector.release_cursor(cursor)

    def get_sql(self) -> str:
        """
        Get the SQL query string for the UpsertBuilder object.
        :return:
        """
        self._values_for_execute.clear()
        for element in self.__jsonBuildings:
            self.__set_json(element[0], element[1])
        sql = ""
        _key: str
        _value: Dict[str, dict]
        for _key, _value in self.__toSet.items():
            self._values_for_execute += _value.values()  # first add is for INSERT values
            self._values_for_execute += _value.values()  # second add is for on duplicate values
            sql += f"INSERT INTO " \
                   f"{_key} ({', '.join(_value.keys())}) VALUES ({', '.join(['?'] * len(_value.values()))}) " \
                   f"ON DUPLICATE KEY UPDATE " \
                   f"{', '.join([f'{key} = ?' for key in _value.keys()])};"
        return sql

    def __set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set column values using a JSON object.
        :param json:
        :param pop:
        :return:
        """
        if pop is None:
            pop = []
        key: str
        value: any
        join_keys = list(self.__toSet)
        for key, value in json.items():
            if isinstance(value, dict):
                if key in join_keys and not key in pop:
                    for sub_key, sub_value in value.items():
                        self.table_set(key, sub_key, sub_value)
                else:
                    self.set(key, dumps(value))
            else:
                self.set(key, value)
        return self

    def set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set values with a json.
        :param json: dict with data example from select
        :param pop: pop keys from the json,
        if you have keys inside that are not a table but a dict/list
        :return:
        """
        self.__jsonBuildings.append([json, pop])
        return self

    def __str__(self):
        return self.get_sql()
