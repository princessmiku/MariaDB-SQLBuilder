from mariadb_sqlbuilder import TableBuilder


class Connect:

    def __init__(self, info_print: bool = True):
        if info_print:
            print("\n\033[36mMariaDB_SQLBuilder connect class is an dummy class.\n"
                  "\033[1;31mExecute and fetching function raise errors!\n"
                  "\033[93mMany functions of connect are not available.\n"
                  "get_sql() is still usable, read the wiki for more information." + "\033[0;0m\n")

    def table(self, name: str) -> TableBuilder:
        return TableBuilder(self, name)


