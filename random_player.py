from player import Player
import numpy as np

class RandomPlayer(Player):
    def __init__(self):
        self.name = "random_player"

    def move(self, board):
        whichBoard = np.random.randint(0,8)
        row = np.random.randint(0,2)
        col = np.random.randint(0,2)
        input((whichBoard, (row, col)))
        
        return (whichBoard, (row, col))