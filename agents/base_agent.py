from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def execute(self, context):
        raise NotImplementedError