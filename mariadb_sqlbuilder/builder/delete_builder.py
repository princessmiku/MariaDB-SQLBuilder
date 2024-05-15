"""
This modul is there for build a sql delete query for
delete stuff in your database
"""
from .base_builder import ConditionsBuilder


class DeleteBuilder(ConditionsBuilder):
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, tb, **kwargs):
        super().__init__(tb, **kwargs)
        self.sure_not_use_conditions = False

    def im_sure_im_not_use_conditions(self, im_sure: bool = True):
        """
        Sets the sure_not_use_conditions attribute to the provided boolean value.
        :param im_sure:
        :return:
        """
        self.sure_not_use_conditions = im_sure
        return self

    def execute(self):
        """
        Executes the DELETE SQL statement built by the builder.
        :return:
        """
        if not self.is_conditions() and not self.sure_not_use_conditions:
            raise PermissionError('Delete Builder: You are not sure enough not to use where')
        cursor = self.tb.connector.get_available_cursor()
        cursor.execute(
            self.get_sql(),
            self.values_for_execute
        )
        cursor.connection.commit()
        self.tb.connector.release_cursor(cursor)

    def get_sql(self) -> str:
        """
        Returns the DELETE SQL statement built by the builder as a string.
        :return:
        """
        return f"DELETE FROM {self.tb.table} " \
            f"{self._get_where_sql()};"

    def __str__(self):
        return self.get_sql()
