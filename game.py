import numpy as np
from boards import *

class Game:
    def __init__(self):
        self.board = LargeBoard()
        self.turn = 'x'
        self.boardToMoveIn = None
        self.validMoves = self.getValidMoves()

    def isOver(self):
        if not (self.board.winner is None):
            return True
        else:
            if len(self.getValidMoves()) == 0:
                return True

    def getWinner(self):
        return self.board.winner

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
        if self.turn == 'x':
            self.turn = 'o'
        else:
            self.turn = 'x'

        self.validMoves = self.getValidMoves()

    def getState(self):
        return (self.board.getState(), self.board.prevMove)

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
        if (self.board.winners[pSquareNum] == 0) and (not self.board.boards[pSquareNum].isCatsGame()):
            # sent to unwon square, move in required square
            self.boardToMoveIn = pSquareNum
            return self.getValidMovesInBoard(pSquareNum)

        #sent to board that has been won, all moves valid
        #or is cats game
        self.boardToMoveIn = None
        valid = []
        for i in range(9):
            if self.board.winners[i] == 0:
                valid.extend(self.getValidMovesInBoard(i))
        return valid

    def getValidMovesInBoard(self, boardnum):
        moves = []
        board = self.board.boards[boardnum]
        for i in range(3):
            for j in range(3):
                if board[i,j] == 0:
                    moves.append((boardnum, (i,j)))
        return moves

    def move(self, move):
        if move not in self.validMoves:
            return False
        ret = self.board.move(self.turn, move[0], move[1])
        print(ret)
        print(self.turn)
        if ret:
            self.incrementTurn()
        print(self.turn)
        return ret

    def invert(self):
        self.board.invert()

def main(): 
    game = Game()
    # game.move((1, (1,1)))
    # game.move((4, (2,2)))
    # game.move((8, (1,1)))
    # game.move((4, (2,1)))
    # game.move((7, (1,1)))
    # game.move((4, (2,0)))
    # game.move((6, (1,1)))
    # game.printBoard()

    # print(game.getValidMoves())

    while not game.isOver():

        #display game state
        game.printBoard()
        print(game.turn + "'s turn:")

        if game.boardToMoveIn is None:
            game.boardToMoveIn = int(input("Which board would you like to play in?\t"))
        else:
            print("moving in board " + str(game.boardToMoveIn))

        boardR = int(input("What row?\t"))
        boardC = int(input("What column?\t"))

        if not game.move((game.boardToMoveIn, (boardR, boardC))):
            print("invalid turn, try again")

if __name__ == "__main__":
    main()
