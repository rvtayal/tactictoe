from player import Player
from boards import *

class UserPlayer(Player):
    def __init__(self):
        self.name = "user_player"

    def move(self, board):
        board.printBoard()

        whichBoard = input("Which board would you like to move in?")
        while not whichBoard.isnumeric() or int(whichBoard) < 0 or int(whichBoard) > 8:
            whichBoard = input("Invalid. Please enter a integer between 0 and 8")
        whichBoard = int(whichBoard)

        row = input("What row?")
        while not row.isnumeric() or int(row) < 0 or int(row) > 2:
            row = input("Invalid. Please enter a integer between 0 and 2")
        row = int(row)

        col = input("What column?")
        while not col.isnumeric() or int(col) < 0 or int(col) > 2:
            col = input("Invalid. Please enter a integer between 0 and 2")
        col = int(col)
        
        return (whichBoard, (row, col))