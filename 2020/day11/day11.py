#!/usr/bin/env python3

import sys
import copy
import argparse

class cabin:
    debugprint = False
    state = None 
    next_state = None
    equilibrium = False
    def __init__(self, data, debugprint=False):
        self.debugprint = debugprint
        self.state = data
        # make a deep copy of the state
        for i in range(len(self.state)):
           self.next_state = [['.']*len(row) for row in self.state]
        if self.debugprint:
            print("Original state:")
            self.planeprint(self.state)

    def compare(self):
        for index in range(len(self.state)):
            if self.state[index] != self.next_state[index]:
                return False
        return True
        
    def check_direction(self, x, y, x_vec, y_vec, max_distance=None):
        # valid_x = lambda x : x >= 0 and x < len(self.state[0])
        # valid_y = lambda y : y >= 0 and y < len(self.state)
        distance = 1
        while True:
            target_x = x + (x_vec*distance)
            target_y = y + (y_vec*distance)
            #if not valid_x(target_x) or not valid_y(target_y):
            #    break
            if not (target_x >= 0 and target_x < len(self.state[0])) or not (target_y >= 0 and target_y < len(self.state)):
                break
            if self.state[target_y][target_x] == 'L':
                return 0
            elif self.state[target_y][target_x] == '#':
                return 1
            distance += 1 
            if max_distance and distance > max_distance:
                return 0
        return 0

    def calc_nextstate_part2(self, part=2):
        if part==2:
            surround_care = 5
            max_distance = None
        else:
            surround_care = 4
            max_distance = 1
        for y in range(len(self.state)):
            for x in range(len(self.state[0])):
                surrounding = 0
                #print("x: {} y: {} state: {}".format(x,y,self.state[y][x]))
                for x_vec in range(-1, 2):
                    for y_vec in range(-1, 2):
                        if x_vec == 0 and y_vec == 0:
                            continue
                        surrounding += self.check_direction(x, y, x_vec, y_vec, max_distance=max_distance)
                #print("Surrounding: {}".format(surrounding))
                if self.state[y][x] == '#' and surrounding >= surround_care:
                    #print("Should be assigning L to # at {}, {}".format(x,y))
                    self.next_state[y][x] = 'L'
                elif self.state[y][x] == 'L' and surrounding == 0:
                    #print("Should be assigning # to L at {}, {}".format(x,y))
                    self.next_state[y][x] = '#'
                else:
                    self.next_state[y][x] = self.state[y][x]
                                

    def planeprint(self, data):
        for index, row in enumerate(data):
            print("{:03d} {}".format(index, ''.join(row)))

    def execute(self, part=1):
        self.calc_nextstate_part2(part=part)
        if self.debugprint:
            print("Next state:")
            self.planeprint(self.next_state)
        if self.compare():
            print("Plane is at equilibrium")
            self.equilibrium = True
        self.state = [row[:] for row in self.next_state]

    def countseats(self):
        count = 0
        for y in range(len(self.state)):
            for x in range(len(self.state[0])):
                if self.state[y][x] == '#':
                    count += 1
        return count



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", help="Part to check. defaults to 1", default=1, type=int)
    parser.add_argument("--debugprint", help="Debug print. Defaults to False", default=False, type=bool)
    parser.add_argument("--input", help="Input file path. Defaults to input.txt", default="input.txt", type=str)
    args = parser.parse_args()
    with open(args.input, 'r') as fd:
        floor_data = [[char for char in elem.strip()] for elem in fd.readlines()]
        plane = cabin(floor_data, debugprint=args.debugprint)
        while not plane.equilibrium:
            plane.execute(part=args.part)
        #plane.execute()
        #plane.execute()
        print(plane.countseats())

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main()')
    main()
