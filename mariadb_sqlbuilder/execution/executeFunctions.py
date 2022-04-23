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


