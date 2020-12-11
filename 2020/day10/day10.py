#!/usr/bin/env python3
import sys

class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

def main():
    global data
    data = [0]
    with open('input.txt', 'r') as fd:
        data += [int(line.strip()) for line in fd.readlines()]
    data.append(max(data)+3)
    data.sort()
    hops = [0,0,0,0]
    for i in range(len(data)-1):
        hop = data[i+1]-data[i]
        #print("Comparing {} and {}: {}".format(data[i], data[i+1], hop))
        hops[hop] += 1
    print("hops[1] * hops[3]: {}".format(hops[1] * hops[3]))
    print("Total valid paths: {}".format(findpaths(0)))

@Memoize
def findpaths(index):
    global data
    valid = 0
    for i in range(index+1, index+4):
        if i >= len(data):
            continue
        if data[i]-data[index] <= 3:
            if data[i] == max(data):
                valid += 1
            else:
                valid += findpaths(i)
    return valid

if __name__ == '__main__':
    main()
