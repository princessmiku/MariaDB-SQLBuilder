from typing import Union

from .select_builder import SelectBuilder
from .update_builder import UpdateBuilder
from .insert_builder import InsertBuilder
from .upsert_builder import UpsertBuilder
from .delete_builder import DeleteBuilder
from .exists_builder import ExistsBuilder


class TableBuilder:

    def __init__(self, connect, table: str):
        self.connect = connect
        self.table = table

    def select(self, column: str, **kwargs) -> SelectBuilder:
        return SelectBuilder(self, column, **kwargs)

    def update(self, **kwargs) -> UpdateBuilder:
        return UpdateBuilder(self, **kwargs)

    def insert(self, **kwargs) -> InsertBuilder:
        return InsertBuilder(self, **kwargs)

    def upsert(self, **kwargs) -> UpsertBuilder:
        return UpsertBuilder(self, **kwargs)

    def delete(self, **kwargs) -> DeleteBuilder:
        return DeleteBuilder(self, **kwargs)

    def exists(self, **kwargs) -> ExistsBuilder:
        return ExistsBuilder(self, **kwargs)
