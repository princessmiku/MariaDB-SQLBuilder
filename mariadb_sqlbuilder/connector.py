"""
The module is there to establish a connection to the database
"""

from typing import Union

import mariadb

from mariadb_sqlbuilder.helpful.validator_dummy import ValidatorDummy
from mariadb_sqlbuilder.helpful.validator import Validator
from mariadb_sqlbuilder.builder import TableBuilder
from mariadb_sqlbuilder.sqlscript.splitter import split_sql_script_in_parameters


class Connector:
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, host: str, user: str, password: str, database: str, *args, port: int = 3306,
                 pool_name: str = "sqlbuilder_pool",
                 pool_size: int = 3, pool_reset_connection: bool = False,
                 use_validator: bool = True, **kwargs):
        self.connections = mariadb.ConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_connection=pool_reset_connection,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            *args,
            **kwargs
        )
        self.__schema = database
        self.connections_list: list = []
        self.in_using_cursors = []
        self.available_cursor: list = []
        self.__is_in_reset = False
        i: int = 1
        while i <= pool_size:
            conn: mariadb.Connection = self.connections.get_connection()
            conn.auto_reconnect = True
            self.connections_list.append(conn)
            self.available_cursor.append(conn.cursor())
            i += 1
        self.__validator = None
        if use_validator:
            self.__validator = Validator(self)
        else:
            self.__validator = ValidatorDummy(self)

    def table(self, name: str) -> TableBuilder:
        """
        Get the functions for building the sql in the selected table.
        :param name: table name
        :return:
        """
        return TableBuilder(self, name)

    def get_available_cursor(self):
        """
        Function for the functionality of execute and fetching.
        The function is used to always give a cursor to an execution
        and let it wait as long as none is available
        :return:
        """
        while not self.available_cursor or self.is_in_reset:
            pass
        cursor = self.available_cursor[0]
        try:
            self.available_cursor.remove(cursor)
        except ValueError:
            cursor = self.get_available_cursor()
        self.in_using_cursors.append(cursor)
        return cursor

    def release_cursor(self, cursor):
        """
        If an execution finish, it releases a cursor and make it
        available for other executions.
        :param cursor:
        :return:
        """
        try:
            self.in_using_cursors.remove(cursor)
        except ValueError:
            cursor.close()
            return
        conn = cursor.connection
        cursor.close()
        cursor = conn.cursor()
        self.available_cursor.append(cursor)

    @property
    def is_in_reset(self) -> bool:
        """
        Get the internal variable if the cursors for
        the execution currently in reset
        :return:
        """
        return self.__is_in_reset

    def reset_available_cursors(self, not_the_save_way: bool = False):
        """
        In case of problems with the cursors, you can reset them.
        :param not_the_save_way: Whether to wait until all actions
        have been performed. Default = False
        :return:
        """
        if not not_the_save_way:
            while len(self.in_using_cursors) > 0:
                pass
        self.__is_in_reset = True
        for cursor in self.available_cursor:
            cursor.close()
        self.available_cursor = []
        self.in_using_cursors = []
        for conn in self.connections_list:
            conn.reset()
        list_of_cursors = []
        for conn in self.connections_list:
            list_of_cursors.append(conn.cursor())
        self.available_cursor = list_of_cursors.copy()
        self.__is_in_reset = False

    def get_active_used_cursors_count(self) -> int:
        """
        Get a count of current used coursers
        :return:
        """
        return len(self.connections_list) - len(self.available_cursor)

    def execute(self, sql: str):
        """
        It will return only if it is successfully,
        only one statement.
        For more statements / a script use 'execute_script'
        :param sql:
        :return:
        """
        cursor = self.get_available_cursor()
        cursor.execute(sql)
        cursor.connection.commit()
        self.release_cursor(cursor)

    def execute_script(self, sql_script: str):
        """
        It will return only if it is complete successfully,
        it will break when a line is not successful.
        :param sql_script:
        :return:
        """
        split_script = split_sql_script_in_parameters(sql_script)
        cursor = self.get_available_cursor()
        for statement in split_script:
            cursor.execute(statement)
        cursor.connection.commit()
        self.release_cursor(cursor)

    def execute_fetchone(self, sql: str):
        """
        Execute a statement with a return of the value
        :param sql:
        :return:
        """
        cursor = self.get_available_cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.release_cursor(cursor)
        return result

    def execute_fetchmany(self, sql: str):
        """
        Execute a statement with a return of the value
        :param sql:
        :return:
        """
        cursor = self.get_available_cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.release_cursor(cursor)
        return result

    @property
    def schema(self) -> str:
        """
        Returns the current schema, where you select your tables
        :return:
        """
        return self.__schema

    def recreate_validator(self):
        """
        Recreate the validator for table changes
        :return:
        """
        self.__validator = Validator(self)

    @property
    def validator(self) -> Union[Validator, ValidatorDummy]:
        """
        Returns the current used validator
        :return:
        """
        return self.__validator
