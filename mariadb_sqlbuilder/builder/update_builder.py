"""
This modul is there for build a sql update query
"""
from datetime import timedelta, datetime
from json import dumps
from typing import Union, Dict, List

from _decimal import Decimal

from mariadb_sqlbuilder.helpful.arithmetic import Arithmetic
from .base_builder import ConditionsBuilder, _get_tcn_without_validator
from .join_builder import BaseJoinExtension


class UpdateBuilder(ConditionsBuilder, BaseJoinExtension):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        ConditionsBuilder.__init__(self, tb, **kwargs)
        BaseJoinExtension.__init__(self, tb, **kwargs)
        # check if variable already exists, else init it
        self.__toSet = {}
        self.sure_not_use_conditions = False
        self.__subSets = []
        self.__jsonBuildings = []

    def set(self, column, value: Union[str, int, float, bool,
        Arithmetic, timedelta, datetime, Decimal]):
        """
        Set a value for a column in the table to update.
        :param column:
        :param value:
        :return:
        """
        self.tb.validator.check_value_type(self.tb.table, column, value)
        self.__toSet[
            _get_tcn_without_validator(self.tb.table, column)
        ] = value
        return self

    def join_set(self, join_table: str, join_column: str, value: Union[str, int, float, bool,
        Arithmetic, timedelta, datetime, Decimal]):
        """
        Set a value for a column in a join table.
        :param join_table:
        :param join_column:
        :param value:
        :return:
        """
        self.tb.validator.check_value_type(join_table, join_column, value)
        self.__toSet[
            _get_tcn_without_validator(join_table, join_column)
        ] = value
        return self

    def im_sure_im_not_use_conditions(self, im_sure: bool = True):
        """
        Set a flag to indicate that the where conditions are not needed.
        :param im_sure:
        :return:
        """
        self.sure_not_use_conditions = im_sure
        return self

    def execute(self):
        """
        Execute the update statement.
        :return:
        """
        if not self.is_conditions() and not self.sure_not_use_conditions:
            raise PermissionError('Update Builder: You are not sure enough not to use where')
        cursor = self.tb.connector.get_available_cursor()
        sql_script = self.get_sql()
        result = cursor.execute(
            sql_script,
            self.values_for_execute
        )
        if self.__subSets:
            for subset in self.__subSets:
                cursor.execute(subset.get_sql())
        cursor.connection.commit()
        self.tb.connector.release_cursor(cursor)

    def _get_value_string(self):
        elements = []
        for key, value in self.__toSet.items():
            elements.append(key + ' = ?')
            self._values_for_execute.append(value)
        return ', '.join(elements) + ' '

    def get_sql(self) -> str:
        """
        Get the SQL statement to execute.
        :return:
        """
        self._values_for_execute.clear()  # clear the execution values
        for element in self.__jsonBuildings:
            self.__set_json(element[0], element[1])

        sql = ((f"UPDATE {self.tb.table} "
               f"{' '.join(self._joins) if self._joins else ''} "
               f"SET ") + self._get_value_string() +
               f" {self._get_where_sql()};")
        return sql

    def __set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set values from a json object.
        :param json:
        :param pop:
        :return:
        """
        if pop is None:
            pop = []
        key: str
        value: any
        join_keys = [x.table for x in self._join_builders]
        for key, value in json.items():
            if isinstance(value, dict):
                if key in join_keys and not key in pop:
                    for sub_key, sub_value in value.items():
                        self.join_set(key, sub_key, sub_value)
                else:
                    self.set(key, dumps(value))
            else:
                self.set(key, value)
        return self

    def set_json(self, json: Dict[str, any], pop: List[str] = None):
        """
        Set values with a json object.
        :param json: dict with data example from select
        :param pop: pop keys from the json,
        if you have keys inside that are not a table but a dict/list
        :return:
        """
        self.__jsonBuildings.append([json, pop])
        return self

    def __str__(self):
        return self.get_sql()
