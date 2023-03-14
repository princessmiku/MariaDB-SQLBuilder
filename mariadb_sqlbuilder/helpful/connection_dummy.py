"""
This modul is there for fake a connection to a database,
if you only want to use the sql query builder
"""
from mariadb_sqlbuilder.helpful.validator_dummy import ValidatorDummy
from mariadb_sqlbuilder.builder import TableBuilder


class Connector:
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, info_print: bool = True):
        if info_print:
            print("\n\033[36mMariaDB_SQLBuilder connect class is an dummy class.\n"
                  "\033[1;31mExecute and fetching function raise errors!\n"
                  "\033[93mMany functions of connect are not available.\n"
                  "get_sql() is still usable, read the wiki for more information." + "\033[0;0m\n")
        self.__validator = ValidatorDummy()

    def table(self, name: str) -> TableBuilder:
        """
        Get the functions for building the sql in the selected table
        :param name:
        :return:
        """
        return TableBuilder(self, name)

    def get_available_cursor(self):
        """
        This is a "dead end" for the execution functions. This will raise a NotImplementedError,
        which is helpful for a better assignment of the error.
        :return:
        """
        raise NotImplementedError("This function is only available with a active connection")

    @property
    def schema(self) -> str:
        """
        It's only a dummy function,
        its return's the schema name "MariaDBSQLBuilder"
        :return:
        """
        return "MariaDBSQLBuilder"

    @property
    def validator(self) -> ValidatorDummy:
        """
        Returns the current used validator
        :return:
        """
        return self.__validator
