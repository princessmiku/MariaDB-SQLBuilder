from typing import Union
from .selectBuilder import SelectBuilder
from .updateBuilder import UpdateBuilder
from .insertBuilder import InsertBuilder
from .upsertBuilder import UpsertBuilder
from .deleteBuilder import DeleteBuilder
from .existsBuilder import ExistsBuilder


class TableBuilder:

    def __init__(self, connect, table: str):
        self.connect = connect
        self.table = table

    def select(self, column: str) -> SelectBuilder:
        return SelectBuilder(self, column)

    def update(self) -> UpdateBuilder:
        return UpdateBuilder(self)

    def insert(self) -> InsertBuilder:
        return InsertBuilder(self)

    def upsert(self) -> UpsertBuilder:
        return UpsertBuilder(self)

    def delete(self) -> DeleteBuilder:
        return DeleteBuilder(self)

    def exists(self) -> ExistsBuilder:
        return ExistsBuilder(self)

