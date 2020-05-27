import numpy as np
from boards import *

class Game:
    def __init__(self):
        self.board = LargeBoard()
        self.turn = 'x'
        self.boardToMoveIn = None
        self.validMoves = self.getValidMoves()

    def isWon(self):
        return not (self.board.winner is None)

    def getWinner(self):
        return self.board,winner

    def printBoard(self):
        disp = self.board.getDisplay()
        r, c = disp.shape
        for i in range(r):
            row = ''
            for j in range(c):
                row += disp[i,j] + ' '
            print(row)

    def incrementTurn(self):
        #set turn
        if self.turn is 'x':
            self.turn = 'o'
        else:
            self.turn = 'x'

        self.validMoves = self.getValidMoves()

    def getState(self):
        return (self.board.boards, self.board.prevMove)

    def getValidMoves(self):
        if self.board.prevMove is None:
            #handles start state
            self.boardToMoveIn = None
            valid = []
            for i in range(9):
                valid.extend(self.getValidMovesInBoard(i))
            return valid

        pBoard, pSquare = self.board.prevMove
        pSquareNum = (pSquare[0] * 3) + pSquare[1]
        if self.board.winners[pSquareNum] == 0:
            # sent to unwon square, move in required square
            self.boardToMoveIn = pSquareNum
            return self.getValidMovesInBoard(pSquareNum)
        else:
            #sent to board that has been won, all moves valid
            self.boardToMoveIn = None
            valid = []
            for i in range(9):
                if self.board.winners[i] == 0:
                    valid.extend(self.getValidMovesInBoard(i))

    def getValidMovesInBoard(self, boardnum):
        moves = []
        board = self.board.boards[boardnum]
        for i in range(3):
            for j in range(3):
                if board[i,j] == 0:
                    moves.append((boardnum, (i,j)))
        return moves

    def move(self, boardloc):
        if (self.boardToMoveIn, boardloc) in self.validMoves:
            return self.board.move(self.turn, self.boardToMoveIn, boardloc)

def main(): 
    game = Game()
    while not game.isWon():

        #display game state
        game.printBoard()
        print(game.turn + "'s turn:")

        if game.boardToMoveIn is None:
            game.boardToMoveIn = int(input("Which board would you like to play in?\t"))
        else:
            print("moving in board " + str(game.boardToMoveIn))

        boardR = int(input("What row?\t"))
        boardC = int(input("What column?\t"))

        if game.move((boardR, boardC)):
            #move to next turn
            game.incrementTurn()
        else:
            print("invalid turn, try again")

if __name__ == "__main__":
    main()
