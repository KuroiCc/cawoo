from abc import ABC, abstractmethod


class IParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, src):
        pass
