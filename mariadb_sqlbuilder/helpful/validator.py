"""
Validator is a connector used class for
checking if a request possible, or it will throw errors

It checks

- if the table exists
- if the column exists
- if the value type the required type of the column

"""
from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from _decimal import Decimal

from mariadb_sqlbuilder.exepetions import InvalidColumnType


class _Column:

    def __init__(self, name: str, data_type: str, length: int, nullable: bool,
                 unsigned: bool, collation_name: str):
        self.name = name
        self.nullable = nullable
        self.range: Tuple[int, int] = (0, 0)
        self.length = length
        self.unsigned = unsigned
        self.data_type_name = data_type
        if data_type in ["varchar", "text"]:
            self.data_type = str
        elif data_type in ["int", "bigint", "smallint", "mediumint", "tinyint"]:
            self.data_type = int
            if data_type == "int":
                if unsigned:
                    if length < 10:
                        self.range = (0, int("9" * length))
                    else:
                        self.range = (0, 4294967295)
                else:
                    if length < 10:
                        self.range = (-int("9" * length), int("9" * length))
                    else:
                        self.range = (-2147483648, 2147483647)
            elif data_type == "bigint":
                if unsigned:
                    if length < 20:
                        self.range = (0, int("9" * length))
                    else:
                        self.range = (0, 18446744073709551615)
                else:
                    if length < 20:
                        self.range = (-int("9" * length), int("9" * length))
                    else:
                        self.range = (-9223372036854775808, 9223372036854775807)
            elif data_type == "smallint":
                if unsigned:
                    if length < 5:
                        self.range = (0, int("9" * length))
                    else:
                        self.range = (0, 65535)
                else:
                    if length < 5:
                        self.range = (-int("9" * length), int("9" * length))
                    else:
                        self.range = (-32768, 32767)
            elif data_type == "mediumint":
                if unsigned:
                    if length < 8:
                        self.range = (0, int("9" * length))
                    else:
                        self.range = (0, 16777215)
                else:
                    if length < 7:
                        self.range = (-int("9" * length), int("9" * length))
                    else:
                        self.range = (-8388608, 8388607)
            elif data_type == "tinyint":
                if unsigned:
                    if length < 3:
                        self.range = (0, int("9" * length))
                    else:
                        self.range = (0, 255)
                else:
                    if length < 3:
                        self.range = (-int("9" * length), int("9" * length))
                    else:
                        self.range = (-128, 127)
        elif data_type in ["decimal"]:
            self.data_type = Decimal
        elif data_type in ["float", "double"]:
            self.data_type = float
            # I do not check it because they are to many
            # variables of the size of a float or double
            # https://mariadb.com/kb/en/float/
            # https://mariadb.com/kb/en/double/
        elif data_type in [
            "blob", "mediumblob", "longblob",
            "char", "inet4", "inet6",
            "mediumtext", "longtext", "text",
            "tinytext", "varchar", "tinyblob"
        ]:
            self.data_type = str
            if data_type == "text":
                if length is 0:
                    self.length = 65535
            elif data_type == "tinytext":
                if length is 0:
                    self.length = 255
            elif data_type == "mediumtext":
                if length is 0:
                    self.length = 16777215
            elif data_type == "longtext":
                if length is 0:
                    self.length = 4294967295
            elif data_type == "char":
                if length == 0:
                    self.length = 255
            elif data_type == "varchar":
                if length == 0:
                    if "utf8" in collation_name:
                        self.length = 21844
                    else:
                        self.length = 65532
            elif data_type == "blob":
                if length == 0:
                    self.length = 65535
            elif data_type == "mediumblob":
                if length == 0:
                    self.length = 16777215
            elif data_type == "longblob":
                if length == 0:
                    self.length = 4294967295
            elif data_type == "tinyblob":
                if length == 0:
                    self.length = 255
        elif data_type in ["uuid"]:
            self.data_type = UUID
        elif data_type in ["date", "datetime", "timestamp", "time", "year"]:
            self.data_type = datetime
        elif data_type in ["enum"]:
            # Why i do not a checking
            # https://mariadb.com/kb/en/enum/
            self.data_type = List[str]
        else:
            raise InvalidColumnType(
                f"The column '{name}' has an unsupported validator type -> {data_type}"
            )

    #def check(self, value: any):


class Validator:

    def __init__(self, conn):
        self._conn = conn
        tables: List[List[str]] = conn.execute_fetchmany("SHOW tables;")
        self.__tables: List[str] = [table[0] for table in tables]
        self.__structure = {}
        table: str
        for table in self.__tables:
            self.__structure[table] = {}
            columns = conn.execute_fetchmany(
                "SELECT COLUMN_NAME, COLUMN_TYPE " +
                "FROM information_schema.COLUMNS " +
                f"WHERE TABLE_NAME = N'{table}' and TABLE_SCHEMA = N'{self._conn.schema}';"
            )
            print(table, columns)
