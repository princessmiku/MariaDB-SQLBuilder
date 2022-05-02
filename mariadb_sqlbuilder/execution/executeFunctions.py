echo_sql = False


def execute(cursor, sql: str):
    if echo_sql: print("EXECUTE:", sql)
    cursor.execute(sql)


def executeOne(cursor, sql: str):
    if echo_sql: print("EXECUTE WITH FETCHONE:", sql)
    cursor.execute(sql)
    return cursor.fetchone()


def executeAll(cursor, sql: str):
    if echo_sql: print("EXECUTE WITH FETCHALL:", sql)
    cursor.execute(sql)
    return cursor.fetchall()


