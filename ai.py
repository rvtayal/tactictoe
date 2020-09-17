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

        #print("map", self.map_.map_)
        #print(state)
        #print(move)
        #print("map[(state, move)]",self.map_[(state, move)])
        #print("max val", np.max(self.map_[nextGameStates]))
        self.map_[(state, move)] = self.map_[(state, move)] + a * (reward + df * np.max(self.map_[nextGameStates]) - self.map_[(state, move)])
        ToDo:
        make hash function for large boards
        make a move object? with hash function?
        or make a seperate hashMove function
        combine move and board hash in the function in util.py




def main():
    a = Ai()

    while(True):
        a.takeTurnLearn()
        a.printGame()
        a.resetGame()
        waitForInput()



if __name__ == "__main__":
    main()