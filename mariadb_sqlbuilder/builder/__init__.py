from typing import Union
from .selectBuilder import SelectBuilder
from .updateBuilder import UpdateBuilder
from .insertBuilder import InsertBuilder
from .upsertBuilder import UpsertBuilder
from .deleteBuilder import DeleteBuilder

echo_sql = True


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

