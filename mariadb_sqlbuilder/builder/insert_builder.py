"""
This modul is there for build a sql insert query
"""
from json import dumps
from typing import Union, Dict, List

from .base_builder import BaseBuilder


class InsertBuilder(BaseBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.__ignore = False
        self.__toSet = {}
        self.__jsonBuildings = []
        self.__values_for_execute= []

    def set(self, column: str, value: Union[str, int, None]):
        """
        Set the value for a column in the table.
        :param column:
        :param value:
        :return:
        """
        if not self.tb.table in self.__toSet:
            self.__toSet[self.tb.table] = {}
        self.tb.validator.check_value_type(self.tb.table, column, value)
        self.__toSet[self.tb.table][column] = value
        return self

    def add_join_table(self, table: str):
        """
        Add a join table to the set of tables to insert data into.
        :param table:
        :return:
        """
        if table in self.__toSet:
            return self
        self.__toSet[table] = {}
        return self

    def table_set(self, table: str, column: str, value: Union[str, int, None]):
        """
        Insert data into another table in one insert.
        :param table:
        :param column:
        :param value:
        :return:
        """
        if not table in self.__toSet:
            self.__toSet[table] = {}
        self.tb.validator.check_value_type(table, column, value)
        self.__toSet[table][column] = value
        return self

    def ignore(self, _ignore: bool = True):
        """
        Set whether to ignore errors during the insert.
        :param _ignore:
        :return:
        """
        self.__ignore = _ignore
        return self

    def execute(self) -> bool:
        """
        Execute the insert query.
        :return:
        """
        cursor = self.tb.connector.get_available_cursor()
        sql_script = self.get_sql()
        result = cursor.execute(
            sql_script,
            self.values_for_execute
        )
        cursor.connection.commit()
        self.tb.connector.release_cursor(cursor)
        return result

    def get_sql(self) -> str:
        """
        Get the SQL query string for the insert.
        :return:
        """
        self._values_for_execute.clear()
        for element in self.__jsonBuildings:
            self.__set_json(element[0], element[1])
        sql = ""
        key: str
        value: Dict[str, dict]
        for key, value in self.__toSet.items():
            if not value:
                continue
            self._values_for_execute += value.values()
            sql += f"INSERT {'IGNORE ' if self.__ignore else ''}INTO " \
                   f"{key} {'(' + ', '.join(value.keys()) + ') VALUES (' + ', '.join(['?'] * len(value.values())) + ')'};"
        return sql

    def __set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set values using a JSON object.
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
        Set values with a json, don't forget where
        :param json: dict with data example from select
        :param pop: pop keys from the json,
        if you have keys inside that are not a table but a dict/list
        :return:
        """
        self.__jsonBuildings.append([json, pop])
        return self

    def __str__(self):
        return self.get_sql()
