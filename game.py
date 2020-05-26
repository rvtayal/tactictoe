import numpy as np
from boards import *

class Game:
	def __init__(self):
		self.board = LargeBoard()
		self.turn = 'x'
		self.boardToMoveIn = None

	def isWon(self):
		return not (self.board.winner is None)

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

		#figure out where next person has to move
		prevR, prevC = self.board.prevMove[1]
		num = (prevR*3) + prevC
		if self.board.boards[num].winner is None:
			self.boardToMoveIn = num
		else:
			self.boardToMoveIn = None

	def validateMove(self, boardnum):
		if self.boardToMoveIn is None:
			return True
		else:
			return self.boardToMoveIn == boardnum

	def getState(self):
		return (self.board.boards, self.board.prevMove)

	def getValidMoves(self):
		pBoard, pSquare = self.board.prevMove
		pSquareNum = (pSquare[0] * r) + pSquare[1]
		if self.board.winners[pSquareNum] == 0:
			# sent to unwon square, move in required square
			return self.getValidMovesInBoard(pSquareNum)
		else:
			#sent to board that has been won, all moves valid
			valid = []
			for i in range(9):
				if self.board.winners[i] == 0:
					valid.append(self.getValidMovesInBoard(i))

	def getValidMovesInBoard(boardnum):
		moves = []
		board = self.board.boards[boardnum]
		for i in range(3):
			for j in range(3):
				if board[i,j] == 0:
					moves.append((boardnum, (i,j)))
		return moves

	def getNextMoveString(self):
		if self.boardToMoveIn is None:
			return 'Move anywhere.'
		else:
			return 'Move in board ' + str(self.boardToMoveIn) + '.'

	def move(self, who, boardnum, boardloc):
		if self.validateMove(boardnum):
			if self.board.move(who, boardnum, boardloc):
				return None
			else:
				return "Please play in unoccupied square."
		else:
			return "Please play in correct board."

def main():
	game = Game()
	while not game.isWon():
		moveValid = False
		while not moveValid:
			game.printBoard()

			boardValid = False
			while not boardValid:
				boardnum = int(input(game.turn + "'s turn. " + game.getNextMoveString() + " Which board?\t"))
				boardValid = game.validateMove(boardnum)

			row = int(input("Which row? (0, 1, or 2)\t"))
			col = int(input("Which col? (0, 1, or 2)\t"))
			moveValid = game.board.move(game.turn, boardnum, (row, col))
			if not moveValid:
				print('##############################')
				print('invalid move, please try again')
				print('##############################')

		#move to next turn
		game.incrementTurn()

if __name__ == "__main__":
    main()
