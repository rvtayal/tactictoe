from mcts import State
from game import *
import copy

class Tactictoe_State(State):
	def __init__(self, game):
		super(Tactictoe_State, self).__init__()
		self.state = game

	def get_actions(self):
		return self.state.getValidMoves()

	def make_copy(self):
		return copy.deepcopy(self)

	def do_action(self, action):
		r = self.state.move(action)
		if not r:
			print("invalid move found")
			exit(0)
		
	def simulate(self):
		if self.isterminal:
			self.total_reward += self.total_reward / self.visits
			return self.total_reward / self.visits
		# nn pass on game board
		This is where to do stuff next
