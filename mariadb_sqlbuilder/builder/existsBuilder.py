from typing import Union

from ..execution import executeFunctions
from .baseBuilder import BaseBuilder


class DeleteBuilder(BaseBuilder):


    def __init__(self, tb):
        super().__init__(tb)
        self.__where_conditions = []
        self.sureNotUseWhere = False
        self.columnList = []

    def column(self, column: str):
        self.columnList.append(column)

    def columns(self, columns: str):
        self.columnList += columns.replace(", ", ",").split(",")

    def where(self):
        pass

    def get_sql(self) -> str:
        pass
