#!/usr/bin/env python3
import sys, re
import argparse

global debug

realprint = print

def dprint(*args):
    if debug:
        realprint(*args)

print = dprint

def main(args):
    global debug
    with open(args.filename, 'r') as fd:
        raw_data = [list(line.strip()) for line in fd.readlines()]
        pass
    dprint(raw_data)
    # active = '#', inactive = '.'
    active_cubes = []
    for y, row in enumerate(raw_data):
        for x, cube in enumerate(row):
            if cube == '#':
                active_cubes.append((x,y,0,0))
    dprint(active_cubes)
    stage = 0
    while stage < 6:
        active_cubes = execute_conway(active_cubes)
        print(stage)
        print(active_cubes)
        stage += 1 
    dprint(len(active_cubes))

def execute_conway(state):
    neighboring_cubes = {}
    next_state = []
    # first, go through all active cubes
    # and add 1 to neigbors for each coord around it
    for cube in state:
        for x in range(cube[0]-1, cube[0]+2):
            for y in range(cube[1]-1, cube[1]+2):
                for z in range(cube[2]-1, cube[2]+2):
                    for w in range(cube[3]-1, cube[3]+2):
                        if (x,y,z,w) == cube: 
                            continue
                        elif (x,y,z,w) in neighboring_cubes.keys():
                            neighboring_cubes[(x,y,z,w)] += 1
                        else:
                            neighboring_cubes[(x,y,z,w)] = 1
    print(neighboring_cubes)
    for coord in neighboring_cubes.keys():
        # check if it's in the current state - that means it's active
        # if not, assume inactive
        if coord in state:
            if neighboring_cubes[coord] == 2 or neighboring_cubes[coord] == 3:
                next_state.append(coord)
        elif neighboring_cubes[coord] == 3:
            # inactive, but will be active now
            next_state.append(coord)
    return next_state


if __name__ == '__main__':
    global debug
    debug = True
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    parser.add_argument("-d", help="Debug. Defaults to False", action='store_true')
    args = parser.parse_args()
    if not args.d:
        debug = False
    print("Debug mode on")
    realprint("This should print regardless of debug")
    main(args)
