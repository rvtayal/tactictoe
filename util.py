# util file for game

import time
import numpy as np

def waitForInput():
    a = raw_input('Press enter to continue...')

def pause(t):
    time.sleep(t)

#Basically a dictionary that returns 0 if item is not there
class HashMap:
    def __init__(self):
        self.map_ = {}

    def clear(self):
        self.map_ = {}

    def __getitem__(self, key):
        if type(key) is type([]):
            l = []
            for k in key:
                l.append(self.getSingleItem(k))
            return np.array(l)
        else:
            return self.getSingleItem(key)

    def __setitem__(self, key, value):
        self.map_[key] = value

    def size(self):
        return len(self.map_)

    def getSingleItem(self, key):
        if key not in self.map_.keys():
            return 0

        return self.map_[key]


def main():
    d = HashMap()
    d.map_ = {'1': 1, '2': 2, '3': 3}
    print(d['1'])
    print(d[['1', '2']])


if __name__ == "__main__":
    main()