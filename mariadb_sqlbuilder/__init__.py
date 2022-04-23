"""

    Maria DB SQL Builder

    Join:
    https://mariadb.com/kb/en/joining-tables-with-join-clauses/

"""
import typing

import mariadb
import sqlparse

from .builder import TableBuilder

__version__ = '0.2.1'


class Connect:

    def __init__(self, *, host: str, user: str, password: str, port: int = 3306,
                 database: str, pool_name: str = "sqlbuilder_pool",
                 pool_size: int = 3, pool_reset_connection: bool = False):
        self.connections = mariadb.ConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_connection=pool_reset_connection,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=True
        )
        self.cursors: list = []
        self.availableCursor: list = []
        i: int = 1
        while i <= pool_size:
            conn = self.connections.get_connection()
            cursor = conn.cursor()
            self.cursors.append(cursor)
            self.availableCursor.append(cursor)
            i += 1

    def table(self, name: str) -> TableBuilder:
        return TableBuilder(self, name)

    def getAvailableCursor(self):
        while not self.availableCursor:
            pass
        cursor = self.availableCursor[0]
        self.availableCursor.remove(cursor)
        return cursor

    def makeCursorAvailable(self, cursor):
        self.availableCursor.append(cursor)

    def resetAvailableCursors(self):
        self.availableCursor = []
        self.availableCursor += self.cursors

    def execute(self, sql: str) -> bool:
        """
        It will return only if it is successfully,
        only one statement.
        For more statements / a script use 'execute_script'
        :param sql:
        :return:
        """
        cursor = self.getAvailableCursor()
        result = builder.execute(cursor, sql)
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
            result = builder.execute(cursor, statement)
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
            result = builder.executeAll(cursor, sql)
        else:
            result = builder.executeOne(cursor, sql)
        self.makeCursorAvailable(cursor)
        return result
