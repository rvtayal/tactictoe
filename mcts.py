import random
import numpy as np
import copy
import math
import time

class MCTS:
	def __init__(self, state, state_class):
		root = state_class(state)
		if not isinstance(root, State):
			print("incorrect state class")
			return

		self.root = root
		self.cp_factor = 1/(2*math.sqrt(2))


	def iteration(self):
		leaf = self.simulate()
		leaf.expand()
		leaf.simulate()
		self.backprop(leaf)


	def selection(self):
		return self.root.find_leaf()


	def backprop(self, node):
		while node != None:
			node.visits += 1
			node.redo_weights(self.cp_factor)
			node = node.parent

	def run(self, time_constraint=10):
		start_time = time.time()
		while (time.time() - start_time) < time_constraint:
			self.iteration()
		return self.root.get_probs()


class State(object):
	def __init__(self):
		self.visits = 0
		self.total_reward = 0
		self.children = []
		self.weights = None
		self.parent = None
		self.isterminal = False

	def find_leaf(self):
		if self.visits == 0:
			return self
		else:
			# select child
			ndx = np.argmax(self.weights)
			return self.children[ndx].find_leaf()

	def expand(self):
		actions = self.state.get_actions()
		self.weights = []
		for a in actions:
			state = self.make_copy()
			state.do_action(a)
			self.children.append(state)
			self.weights.append(math.inf)

	def redo_weights(self, cp):
		weights = []
		for c in self.children:
			if c.visits == 0:
				weights.append(math.inf)
			else:
				w = (self.total_reward/self.visits) + 2*cp*math.sqrt((2*math.log(self.visits, math.e))/c.visits)
				weights.append(w)
		self.weights = weights

	def get_probs(self):
		return [c.visits/self.visits for c in self.children]

	def get_actions(self):
		pass

	def make_copy(self):
		pass

	def do_action(self, action):
		pass

	def simulate(self):
		pass