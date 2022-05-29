"""

    Maria DB SQL Builder

    Join:
    https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
import typing

import mariadb
import sqlparse

from .builder import TableBuilder
from .execution.executeFunctions import execute, executeOne, executeAll

__version__ = '0.3.2'


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
            autocommit=True,
            *args,
            **kwargs
        )
        self.connectionsList: list = []
        self.inUsingCursors = []
        self.availableCursor: list = []
        self.isInReset = False
        i: int = 1
        while i <= pool_size:
            conn: mariadb.connection = self.connections.get_connection()
            conn.auto_reconnect = True
            self.connectionsList.append(conn)
            cursor = conn.cursor()
            self.availableCursor.append(cursor)
            i += 1

    def table(self, name: str) -> TableBuilder:
        return TableBuilder(self, name)

    def getAvailableCursor(self):
        while not self.availableCursor or self.isInReset:
            pass
        cursor = self.availableCursor[0]
        try:
            self.availableCursor.remove(cursor)
        except ValueError as e:
            cursor = self.getAvailableCursor()
        self.inUsingCursors.append(cursor)
        return cursor

    def makeCursorAvailable(self, cursor):
        try:
            self.inUsingCursors.remove(cursor)
        except ValueError:
            cursor.close()
            return
        conn = cursor.connection
        cursor.close()
        cursor = conn.cursor()
        self.availableCursor.append(cursor)

    def resetAvailableCursors(self, notTheSaveWay: bool = False):
        if not notTheSaveWay:
            while len(self.inUsingCursors) > 0:
                pass
        self.isInReset = True
        [cursor.close() for cursor in self.availableCursor]
        self.availableCursor = []
        self.inUsingCursors = []
        [conn.reset() for conn in self.connectionsList]
        listOfCursors = [conn.cursor() for conn in self.connectionsList]
        self.availableCursor = listOfCursors.copy()

    def getActiveUsedCursorsCount(self) -> int:
        return len(self.connectionsList) - len(self.availableCursor)


    def execute(self, sql: str) -> bool:
        """
        It will return only if it is successfully,
        only one statement.
        For more statements / a script use 'execute_script'
        :param sql:
        :return:
        """
        cursor = self.getAvailableCursor()
        result = execute(cursor, sql)
        self.makeCursorAvailable(cursor)
        return result

    def execute_script(self, sql_script: str) -> bool:
        """
        It will return only if it is complete successfully,
        it will break when a line is not successful.
        Changes since then will be available, so be careful
        :param sql_script:
        :return:
        """
        cursor = self.getAvailableCursor()
        statements: list[str] = sqlparse.split(sql_script)
        result = False
        for statement in statements:
            result = execute(cursor, statement)
            if not result: break
        self.makeCursorAvailable(cursor)
        return result

    def execute_fetch(self, sql: str, many: bool = False):
        """
        Execute a statement with a return of the value
        :param sql:
        :param many:
        :return:
        """
        cursor = self.getAvailableCursor()
        if many:
            result = executeAll(cursor, sql)
        else:
            result = executeOne(cursor, sql)
        self.makeCursorAvailable(cursor)
        return result
