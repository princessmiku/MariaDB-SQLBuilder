from typing import List

from mariadb import IntegrityError
from sqlparse import split

echo_sql = False


def execute(cursor, sql: str):
    if echo_sql: print("EXECUTE:", sql)
    cursor.execute(sql)


def executeScript(cursor, sql: str):
    if echo_sql: print("EXECUTE SCRIPT:", sql)
    statements: List[str] = split(sql)
    errorStatement: List[str] = []
    for statement in statements:
        try:
            execute(cursor, statement)
        except IntegrityError:
            errorStatement.append(statement)
    if errorStatement:
        for statement in errorStatement:
            execute(cursor, statement)


def executeOne(cursor, sql: str):
    if echo_sql: print("EXECUTE WITH FETCHONE:", sql)
    cursor.execute(sql)
    return cursor.fetchone()


def executeAll(cursor, sql: str):
    if echo_sql: print("EXECUTE WITH FETCHALL:", sql)
    cursor.execute(sql)
    return cursor.fetchall()
