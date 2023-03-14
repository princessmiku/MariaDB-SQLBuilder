"""
Dummy Class for the Validator,
if you won't use it
"""


class ValidatorDummy:
    """
    This class is for checking the existing of tables, columns and the
    right value types
    """

    def __init__(self, conn):
        self._conn = conn
        self.__structure = {}

    def check_table_exists(self, table: str):
        """
        It's only a dummy function
        :param table:
        :return:
        """

    def check_column_exists(self, table: str, column: str):
        """
        It's only a dummy function
        :param table:
        :param column:
        :return:
        """

    def check_value_type(self, table: str, colum: str, value: any):
        """
        It's only a dummy function
        :param table:
        :param colum:
        :param value:
        :return:
        """

    @property
    def structure(self):
        """
        It's only a dummy function
        :return:
        """
        return self.__structure.copy()
