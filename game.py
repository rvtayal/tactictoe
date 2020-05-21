import numpy as np
from boards import *

class Game:
	def __init__(self):
		self.board = LargeBoard()
		self.turn = 'x'
		self.boardToMoveIn = None

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

	def getNextMoveString(self):
		if self.boardToMoveIn is None:
			return 'Move anywhere.'
		else:
			return 'Move in board ' + str(self.boardToMoveIn + 1) + '.'

def main():
	game = Game()
	while game.board.winner is None:
		moveValid = False
		while not moveValid:
			game.printBoard()

			boardValid = False
			while not boardValid:
				boardnum = int(input(game.turn + "'s turn. " + game.getNextMoveString() + " Which board?\t"))-1
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
