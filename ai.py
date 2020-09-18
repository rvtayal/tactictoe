from random import random, seed, randint
from datetime import datetime
import numpy as np

from boards import *
from game import *
from util import *

# data that influences learning
r = 1           # reward
a = 0.05        # learning rate
df = .9         # discount factor
epsilon = 0.5   # chance of random turn



class Ai:
    def __init__(self):
        self.map_ = HashMap(aiHash)
        self.game_ = Game()
        seed((datetime.now()-datetime(1970,1,1)).total_seconds())

    def resetGame(self):
        if self.game_.isWon():
            self.game_ = Game()
            print(self.map_)
            waitForInput()

    def printGame(self):
        self.game_.printBoard()

    def takeTurnLearn(self):
        state = self.game_.getState()
        validMoves = self.game_.getValidMoves()

        if random() < epsilon:
            #random choice
            move = validMoves[randint(0, len(validMoves)-1)]
        else:
            #best choice
            gamestates = []
            for v in validMoves:
                gamestates.append((state, v))
            vals = self.map_[gamestates]
            ndx = np.argmax(vals)
            move = validMoves[ndx]

        self.game_.move(move)

        reward = 0
        if self.game_.isWon():
            reward = r

        nextState = self.game_.getState()
        nextMoves = self.game_.getValidMoves()

        nextGameStates = []
        for nM in nextMoves:
            nextGameStates.append((nextState, nM))

        print(self.map_[(state, move)])
        print(nextGameStates)
        print(np.max(self.map_[nextGameStates]))

        self.map_[(state, move)] = self.map_[(state, move)] + a * (reward + df * np.max(self.map_[nextGameStates]) - self.map_[(state, move)])
        need to deal with situation where a small board is a cats game, but agent is sent there
        no moves makes the agent error out. If cats game, agent can move anywhere?


def main():
    a = Ai()

    while(True):
        a.takeTurnLearn()
        a.printGame()
        a.resetGame()



if __name__ == "__main__":
    main()