from mcts import State, MCTS
from game import *
from network import TacticToeNet
import copy

class Tactictoe_State(State):
    def __init__(self, game, network):
        super().__init__()
        self.state = game
        self.network = network

    def get_actions(self):
        return self.state.getValidMoves()

    def make_copy(self):
        g = copy.deepcopy(self.state)
        s = Tactictoe_State(g, self.network)
        return s

    def do_action(self, action):
        r = self.state.move(action)
        return r
        
    def simulate(self):
        # if self.isterminal:
        #     self.total_reward += self.total_reward / self.visits
        #     return self.total_reward / self.visits
        # nn pass on game board
        value, policy = self.network(self.state)
        return value


if __name__ == "__main__":
    game = Game()
    net = TacticToeNet()
    mcts = MCTS(game, Tactictoe_State, net)
    print(mcts.run(20))