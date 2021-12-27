from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self):
        self.name = "player"

    @abstractmethod
    def move(self, board):
        pass