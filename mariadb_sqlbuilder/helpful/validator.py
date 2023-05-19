"""
Validator is a connector used class for
checking if a request possible, or it will throw errors

It checks

- if the table exists
- if the column exists
- if the value type the required type of the column

"""
import re
from datetime import datetime, timedelta
from typing import List, Tuple
from uuid import UUID

from _decimal import Decimal

from mariadb_sqlbuilder.exepetions import InvalidColumnType, ValidatorType,\
    ValidatorLength, ValidatorUnknown, ValidatorRange, ValidatorTableNotFound,\
    ValidatorColumnNotFound


class _Column:
    """
    This class contains all need data for checking if a value
    possible to add it in the database
    """

    def __init__(self, name: str, data_type: str, length: int, nullable: bool,
                 unsigned: bool, character_set_name: str):
        self.name = name
        self.nullable = nullable
        self.range: Tuple[int, int] = (0, 0)
        self.length = length
        self.unsigned = unsigned
        self.data_type_name = data_type
        self.data_type: any = None
        self.character_set_name = character_set_name
        if data_type in ["int", "bigint", "smallint", "mediumint", "tinyint", "year"]:
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
            elif data_type == "year":
                self.range = (4, 4)
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
                    if "utf8" in character_set_name:
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
            else:
                raise TypeError('Not found')
        elif data_type in ["uuid"]:
            self.data_type = UUID
        elif data_type in ["date", "datetime", "timestamp"]:
            self.data_type = datetime
        elif data_type in ["time"]:
            self.data_type = timedelta
        elif data_type in ["enum"]:
            # Why i do not a checking
            # https://mariadb.com/kb/en/enum/
            self.data_type = list
        else:
            raise InvalidColumnType(
                f"The column '{name}' has an unsupported validator type -> {data_type}"
            )

    def check(self, value: any) -> bool:
        """
        Check if a value match the type requirements of the column
        :param value:
        :return:
        """
        if value is None and not self.nullable:
            raise ValidatorType("The given value is None, but the accepted"
                                "value can't be None")
        if value is None:
            return True
        if not isinstance(value, self.data_type):
            raise ValidatorType(
                f"The type ({type(value)}) of the given value do "
                f"not match the column type {self.data_type}."
            )
        if self.data_type == str:
            value: str
            if self.data_type_name in [
                "text", "tinytext", "mediumtext", "longtext", "varchar", "char"
            ]:
                length = len(value)
                if length > self.length:
                    raise ValidatorLength(
                        f"The length of the string ({length}) "
                        f"is bigger then the allowed length of {self.length}"
                    )
                return True
            elif self.data_type_name in [
                "blob", "tinyblob", "mediumblob", "longblob"
            ]:
                length = len(value.encode(self.character_set_name))
                if length > self.length:
                    raise ValidatorLength(
                        f"The bytes of the string ({length}) "
                        f"is bigger then the allowed bytes of {self.length}"
                    )
                return True
            elif self.data_type_name in ["inet4", "inet6"]:
                return True
            raise ValidatorUnknown("Oh... there is an internal problem with the type system")
        elif self.data_type == int:
            value: int
            if not self.range[0] <= value <= self.range[1]:
                raise ValidatorRange(
                    f"Your number ({str(value)}) is not in the range of the supported type {str(self.range)}."
                )
            return True
        elif self.data_type == float:
            return True
        elif self.data_type == UUID:
            return True
        elif self.data_type == datetime:
            return True
        elif self.data_type == timedelta:
            return True
        elif self.data_type == Decimal:
            return True
        elif self.data_type == list and self.name == "enum":
            if not all(isinstance(val, str) for val in value):
                raise ValidatorType(
                    "An enum only accept strings"
                )
            return True
        raise ValidatorUnknown("Internal error with the column types, 404 not found")


class Validator:
    """
    This class is for checking the existing of tables, columns and the
    right value types
    """

    def __init__(self, conn):
        self._conn = conn
        tables: List[List[str]] = conn.execute_fetchmany("SHOW tables;")
        tables: List[str] = [table[0] for table in tables]
        self.__structure = {}
        table: str
        table_join = "'" + "', '".join(tables) + "'"
        columns = conn.execute_fetchmany(
            "SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, CHARACTER_SET_NAME, TABLE_NAME " +
            "FROM information_schema.COLUMNS " +
            f"WHERE TABLE_NAME IN ({table_join}) and TABLE_SCHEMA = N'{self._conn.schema}';"
        )
        for column in columns:
            if not column[4] in self.__structure:
                self.__structure[column[4]] = {}
            data_type = column[1].split("(")[0] \
                if "(" in column[1] else column[1].split(" ")[0]
            match = re.search('\((\d+)\)', column[1])
            if match:
                length = int(match.group(1))
            else:
                length = 0
            unsigned = True if "unsigned" in column[1] else False
            self.__structure[column[4]][column[0]] = _Column(
                column[0], data_type, length, column[2], unsigned, column[3]
            )

    def check_table_exists(self, table: str):
        """
        Check if the table exists, if not it raise an error
        :param table:
        :return:
        """
        if table in self.__structure:
            return
        raise ValidatorTableNotFound(
            f"Table {table} not found. Check upper- and lowercase. If you change the database "
            "while the system is running, regenerate the validator"
        )

    def check_column_exists(self, table: str, column: str):
        """
        Check if the table and the column exists,
        if not it raise an error.
        :param table:
        :param column:
        :return:
        """
        self.check_table_exists(table)
        if column in self.__structure[table]:
            return
        raise ValidatorColumnNotFound(
            f"The column {column} in the table {table} not found. "
            f"Check upper- and lowercase. If you change the database "
            "while the system is running, regenerate the validator"
        )

    def check_value_type(self, table: str, colum: str, value: any):
        """
        Check if the given value the correct accepted type of the column,
        its also check if the table and column exists.
        If not it raise an error.
        :param table:
        :param colum:
        :param value:
        :return:
        """
        self.check_column_exists(table, colum)
        return self.__structure[table][colum].check(value)

    @property
    def structure(self):
        """
        Return the dictionary of the current structure.
        Helpful vor debugging
        :return:
        """
        return self.__structure.copy()
