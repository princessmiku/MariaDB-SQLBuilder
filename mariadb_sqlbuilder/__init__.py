"""

    Maria DB SQL Builder

    Join:
    https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
import mariadb

from sqlscript.splitter import split_sql_script_in_parameters
from .builder import TableBuilder


class Connect:

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306, pool_name: str = "sqlbuilder_pool",
                 pool_size: int = 3, pool_reset_connection: bool = False, *args, **kwargs):
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

    def table(self, name: str) -> TableBuilder:
        return TableBuilder(self, name)

    def get_available_cursor(self):
        while not self.available_cursor or self.is_in_reset:
            pass
        cursor = self.available_cursor[0]
        try:
            self.available_cursor.remove(cursor)
        except ValueError as e:
            cursor = self.get_available_cursor()
        self.in_using_cursors.append(cursor)
        return cursor

    def release_cursor(self, cursor):
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
    def is_in_reset(self):
        return self.__is_in_reset

    def reset_available_cursors(self, not_the_save_way: bool = False):
        if not not_the_save_way:
            while len(self.in_using_cursors) > 0:
                pass
        self.__is_in_reset = True
        for cursor in self.available_cursor: cursor.close()
        self.available_cursor = []
        self.in_using_cursors = []
        for conn in self.connections_list: conn.reset()
        list_of_cursors = []
        for conn in self.connections_list: list_of_cursors.append(conn.cursor())
        self.available_cursor = list_of_cursors.copy()
        self.__is_in_reset = False

    def get_active_used_cursors_count(self) -> int:
        return len(self.connections_list) - len(self.available_cursor)

    def execute(self, sql: str):
        """
        It will return only if it is successfully,
        only one statement.
        For more statements / a script use 'execute_script'
        :param sql:
        :param commit
        :return:
        """
        cursor = self.get_available_cursor()
        cursor.execute(sql)
        cursor._connection.commit()
        self.release_cursor(cursor)

    def execute_script(self, sql_script: str):
        """
        It will return only if it is complete successfully,
        it will break when a line is not successful.
        :param sql_script:
        :param commit: commit changes?
        :return:
        """
        split_script = split_sql_script_in_parameters(sql_script)
        cursor = self.get_available_cursor()
        for statement in split_script:
            cursor.execute(statement)
        cursor._connection.commit()
        self.release_cursor(cursor)

    def execute_fetchone(self, sql: str):
        """
        Execute a statement with a return of the value
        :param sql:
        :param many:
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
        :param many:
        :return:
        """
        cursor = self.get_available_cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.release_cursor(cursor)
        return result
