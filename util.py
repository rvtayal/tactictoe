# util file for game

import time
import numpy as np

def waitForInput():
    a = raw_input('Press enter to continue...')

def pause(t):
    time.sleep(t)

#Basically a dictionary that returns 0 if item is not there
class HashMap:
    def __init__(self, hashfn=None):
        self.map_ = {}
        if hashfn is None:
            self.hashfn = self.blankfn
        else:
            self.hashfn = hashfn

    def clear(self):
        self.map_ = {}

    def blankfn(self, val):
        return val

    def __getitem__(self, key):
        if type(key) is type([]):
            l = []
            for k in key:
                l.append(self.getSingleItem(k))
            return np.array(l)
        else:
            return self.getSingleItem(key)

    def __setitem__(self, key, value):
        #print("key",key)
        #print("value", value)
        #self.map_[key] = value
        h = self.hashfn(key)
        self.map_[h] = value

    def size(self):
        return len(self.map_)

    def getSingleItem(self, key):
        if self.hashfn(key) not in self.map_.keys():
            return 0

        return self.map_[self.hashfn(key)]

def exhash(i):
    return i*5

def aiHash(toHash):
    #an item to hash for the ai has the form ((board, move), move)
    a = toHash[0]
    b = toHash[1]
    board = a[0]
    prevMove = a[1]
    curMove = b

    curHash = board.hash()


    print(board)
    print(prevMove)
    print(curMove)

def main():
    d = HashMap()
    d[1] = 'l'
    print(d.map_)
    print(d[1])


if __name__ == "__main__":
    main()