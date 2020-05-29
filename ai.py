from random import random, seed, randint
from datetime import datetime

from boards import *
from game import *
from util import *

r = 1			# reward
a = 0.05		# learning rate
df = .9			# discount factor
epsilon = 0.5	# chance of random turn

class ai:
	def __init__(self):
		self.map_ = HashMap()
		self.game = Game()
		seed((datetime.now()-datetime(1970,1,1)).total_seconds())

	def takeTurnLearn(self):
		state = game.getState()
		validMoves = game.getValidMoves()

		if random() < epsilon:
			#random choice
			move = validMoves[randint(0, len(validMoves)-1)]
		