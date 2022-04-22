"""

    Part of building the sql script

"""
from typing import Union

echo_sql = False


def execute(cursor, sql: str):
    if echo_sql: print("EXECUTE:", sql)
    try:
        cursor.execute(sql)
        return True
    except Exception as e:
        print(e)
        return False


def executeOne(cursor, sql: str):
    if echo_sql: print("EXECUTE WITH FETCHONE:", sql)
    try:
        cursor.execute(sql)
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


def executeAll(cursor, sql: str):
    if echo_sql: print("EXECUTE WITH FETCHALL:", sql)
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None


class SelectBuilder:

    def __init__(self, tb, column):
        self.tb = tb
        self.column = column
        self.__where_conditions = []

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{column} = {value}")
        else:
            self.__where_conditions.append(f"{column} = '{value}'")
        return self


    def fetchone(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = executeOne(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def fetchall(self):
        cursor = self.tb.connect.getAvailableCursor()
        result = executeAll(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"SELECT {self.column} FROM {self.tb.table} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"


class UpdateBuilder:

    def __init__(self, tb):
        self.tb = tb
        self.__toSet = {}
        self.__where_conditions = []

    def set(self, column, value: Union[str, int, None]):
        if isinstance(value, int):
            self.__toSet[column] = f"{str(value)}"
        elif value is None:
            self.__toSet[column] = f"NULL"
        else:
            self.__toSet[column] = f"'{str(value)}'"
        return self

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{column} = {value}")
        else:
            self.__where_conditions.append(f"{column} = '{value}'")
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result


    def get_sql(self) -> str:
        return f"UPDATE {self.tb.table} SET " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"


class InsertBuilder:

    def __init__(self, tb):
        self.tb = tb
        self.__ignore = False
        self.__toSet = {}

    def set(self, column, value: Union[str, int, None]):
        if isinstance(value, int):
            self.__toSet[column] = f"{str(value)}"
        elif value is None:
            self.__toSet[column] = f"NULL"
        else:
            self.__toSet[column] = f"'{str(value)}'"
        return self

    def ignore(self, _ignore: bool = True):
        self.__ignore = _ignore
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"INSERT {'IGNORE ' if self.__ignore else ''}INTO " \
            f"{self.tb.table} ({', '.join(self.__toSet.keys())}) VALUES ({', '.join(self.__toSet.values())})"


class UpsertBuilder:

    def __init__(self, tb):
        self.tb = tb
        self.__toSet = {}

    def set(self, column, value: Union[str, int, None]):
        if isinstance(value, int):
            self.__toSet[column] = f"{str(value)}"
        elif value is None:
            self.__toSet[column] = f"NULL"
        else:
            self.__toSet[column] = f"'{str(value)}'"
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        result = execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"INSERT INTO " \
            f"{self.tb.table} ({', '.join(self.__toSet.keys())}) VALUES ({', '.join(self.__toSet.values())})" \
            f"ON DUPLICATE KEY UPDATE " \
            f"{', '.join(['%s = %s' % (key, value) for (key, value) in self.__toSet.items()])}"


class DeleteBuilder:

    def __init__(self, tb):
        self.tb = tb
        self.__where_conditions = []
        self.sureNotUseWhere = False

    def where(self, column: str, value: Union[str, int]):
        if isinstance(value, int):
            self.__where_conditions.append(f"{column} = {value}")
        else:
            self.__where_conditions.append(f"{column} = '{value}'")
        return self

    def imSureImNotUseWhere(self, imSure: bool = False):
        self.sureNotUseWhere = imSure
        return self

    def execute(self) -> bool:
        cursor = self.tb.connect.getAvailableCursor()
        if not self.__where_conditions and not self.sureNotUseWhere:
            raise PermissionError('You are not sure enough not to use where')
        result = execute(
            cursor,
            self.get_sql()
        )
        self.tb.connect.makeCursorAvailable(cursor)
        return result

    def get_sql(self) -> str:
        return f"DELETE FROM {self.tb.table} " \
            f"{'WHERE ' + ' AND '.join(self.__where_conditions) if self.__where_conditions else ''}"


class TableBuilder:

    def __init__(self, connect, table: str):
        self.connect = connect
        self.table = table

    def select(self, column: str) -> SelectBuilder:
        return SelectBuilder(self, column)

    def update(self) -> UpdateBuilder:
        return UpdateBuilder(self)

    def insert(self) -> InsertBuilder:
        return InsertBuilder(self)

    def upsert(self) -> UpsertBuilder:
        return UpsertBuilder(self)

    def delete(self) -> DeleteBuilder:
        return DeleteBuilder(self)

