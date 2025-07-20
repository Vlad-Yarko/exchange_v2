from abc import ABC, abstractmethod


class DatabaseManager(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
