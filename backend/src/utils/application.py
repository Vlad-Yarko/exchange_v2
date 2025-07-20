from abc import ABC, abstractmethod


class Application(ABC):
    def __init__(self):
        self.app = None
    
    @abstractmethod
    def create():
        raise NotImplementedError()

    @abstractmethod
    def run():
        raise NotImplementedError()
