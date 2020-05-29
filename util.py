# util file for game

import time

def waitForInput():
    print("Press enter to continue")
    input()

def pause(t):
    time.sleep(t)

#Basically a dictionary that returns 0 if item is not there
class HashMap:
    def __init__(self):
        self.map_ = {}

    def clear(self):
        self.map_ = {}

    def __getitem__(self, key):
        if key not in self.map_.keys():
            return 0

        return self.map_[key]

    def __setitem__(self, key, value):
        self.map_[key] = value

    def size(self):
        return len(self.map_)


def main():
    d = HashMap()
    d[1] = '1'
    print(d[1])
    print(d[2])
    print(len(d.map_))


if __name__ == "__main__":
    main()