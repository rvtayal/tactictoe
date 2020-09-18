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

    def __str__(self):
        s = ''
        for i in self.map_.keys():
            s = s + str(i) + '\t' + str(self.map_[i]) + '\n'
        return s

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

def base3toBase10(string):
    base10 = 0
    while(len(string) > 0):
        base10 = base10*3
        cur = string[0]
        string = string[1:]
        base10 = base10 + int(cur)
    return base10

def hashMove(move):
    if move is None:
        return 0
    board, loc = move
    locStr = str(loc[0]) + str(loc[1])
    locInt = base3toBase10(locStr)
    return board*10 + locInt + 1


def aiHash(toHash):
    #an item to hash for the ai has the form ((board, move), move)
    a = toHash[0]
    b = toHash[1]
    board = a[0]
    prevMove = a[1]
    curMove = b

    return (hash(board)*100*100) + (hashMove(prevMove)*100) + (hashMove(curMove))

def main():
    h = HashMap()
    h[1] = '1'
    h[2] = '2'
    print(h)

if __name__ == "__main__":
    main()