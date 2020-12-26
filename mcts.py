import random
import numpy as np
import copy
import math
import time

class MCTS:
    count = 0
    def __init__(self, state, state_class, sim):
        self.root = state_class(state, sim)
        if not isinstance(self.root, state_class):
            print("incorrect state class")
            return

        self.cp_factor = 1/(2*math.sqrt(2))


    def iteration(self):
        leaf = self.selection()
        leaf.expand()
        leaf.simulate()
        self.backprop(leaf)
        MCTS.count += 1

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

        action = self.root.children[np.argmax(self.root.get_probs())].parent_action
        return self.root.get_probs(), action


class State(object):
    def __init__(self):
        self.visits = 0
        self.total_reward = 0
        self.children = []
        self.weights = None
        self.parent = None
        self.isterminal = False
        self.valid = True
        self.parent_action = None

    def find_leaf(self):
        if self.weights is None:
            self.weights = [math.inf for _ in self.get_actions()]
        if self.visits == 0:
            return self

        #terminal, no more states after
        if len(self.weights) == 0:
            return self
        else:
            # select child
            ndx = np.argmax(self.weights)
            return self.children[ndx].find_leaf()

    def expand(self):
        actions = self.get_actions()
        if len(actions) == 0:
            # self.isterminal = True
            return
        self.weights = []
        for a in actions:
            state = self.make_copy()
            v = state.do_action(a)
            state.parent = self
            state.parent_action = a
            if not v:
                state.valid = False
            self.children.append(state)
            self.weights.append(math.inf)

    def redo_weights(self, cp):
        weights = [0 for _ in self.children]
        for i,c in enumerate(self.children):
            if c.visits == 0:
                weights[i] = math.inf
            elif not c.valid:
                weights[i] = -1
            else:
                w = (self.total_reward/self.visits) + 2*cp*math.sqrt((2*math.log(self.visits, math.e))/c.visits)
                weights[i] = w
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