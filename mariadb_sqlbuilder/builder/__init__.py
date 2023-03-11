"""
This modul is there for handle table functions
"""
from typing import Union

from .select_builder import SelectBuilder
from .update_builder import UpdateBuilder
from .insert_builder import InsertBuilder
from .upsert_builder import UpsertBuilder
from .delete_builder import DeleteBuilder
from .exists_builder import ExistsBuilder


class TableBuilder:
    """
    TODO: add a description
    This is a dummy docstring.
    """

    def __init__(self, connect, table: str):
        self.connect = connect
        self.table = table

    def select(self, expressions: Union[str, list], *args, **kwargs) -> SelectBuilder:
        """
        Returns a SelectBuilder instance to build a SELECT query.
        :param expressions:
        :param kwargs:
        :return:
        """
        return SelectBuilder(self, expressions, *args, **kwargs)

    def update(self, **kwargs) -> UpdateBuilder:
        """
        Returns an UpdateBuilder instance to build an UPDATE query.
        :param kwargs:
        :return:
        """
        return UpdateBuilder(self, **kwargs)

    def insert(self, **kwargs) -> InsertBuilder:
        """
        Returns an InsertBuilder instance to build an INSERT query.
        :param kwargs:
        :return:
        """
        return InsertBuilder(self, **kwargs)

    def upsert(self, **kwargs) -> UpsertBuilder:
        """
        Returns an UpsertBuilder instance to build an UPSERT query.
        :param kwargs:
        :return:
        """
        return UpsertBuilder(self, **kwargs)

    def delete(self, **kwargs) -> DeleteBuilder:
        """
        Returns a DeleteBuilder instance to build a DELETE query.
        :param kwargs:
        :return:
        """
        return DeleteBuilder(self, **kwargs)

    def exists(self, **kwargs) -> ExistsBuilder:
        """
        Returns an ExistsBuilder instance to check if a record exists in the table.
        :param kwargs:
        :return:
        """
        return ExistsBuilder(self, **kwargs)
