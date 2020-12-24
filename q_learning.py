from random import random, seed, randint
from datetime import datetime
import numpy as np

from boards import *
from game import *
from util import *

# data that influences learning
r = 1           # reward
a = 0.1        # learning rate
df = .95         # discount factor
epsilon = 0.1   # chance of random turn
n = 1000000      # learning iterations



class Ai:
    def __init__(self):
        self.map_ = HashMap(aiHash)
        self.game_ = Game()
        seed((datetime.now()-datetime(1970,1,1)).total_seconds())

    def resetGame(self):
        if self.game_.isOver():
            self.game_ = Game()


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
        if self.game_.getWinner() == 'x':
            reward = r

        nextState = self.game_.getState()
        nextMoves = self.game_.getValidMoves()

        nextGameStates = []
        for nM in nextMoves:
            nextGameStates.append((nextState, nM))

        if len(nextMoves) > 0:
            maxTerm = np.max(self.map_[nextGameStates])
        else:
            maxTerm = 0

        self.map_[(state, move)] = self.map_[(state, move)] + a * (reward + df * maxTerm - self.map_[(state, move)])


def main():
    a = Ai()

    i = 0

    while(i < n):
        print("iteration {}".format(i))
        a.takeTurnLearn()
        #a.printGame()
        a.resetGame()
        i = i + 1

    print(a.map_)



if __name__ == "__main__":
    main()