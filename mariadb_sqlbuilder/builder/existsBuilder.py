from typing import Union

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder


class DeleteBuilder(BaseBuilder):


    def __init__(self, tb):
        super().__init__(tb)
        self.sureNotUseWhere = False
        self.columnList = []

    def column(self, column: str):
        self.columnList.append(column)

    def columns(self, columns: str):
        self.columnList += columns.replace(", ", ",").split(",")

    def get_sql(self) -> str:
        pass
