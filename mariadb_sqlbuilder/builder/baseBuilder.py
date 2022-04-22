from abc import ABC, abstractmethod


class BaseBuilder(ABC):

    def __init__(self, tb):
        self.tb = tb

    @abstractmethod
    def get_sql(self) -> str:
        pass

