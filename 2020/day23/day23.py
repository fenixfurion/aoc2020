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
        cups = list([int(elem) for elem in fd.readlines()[0].strip()])
    print(cups)
    if args.part == 2:
        moves = 10000000
        cups += list(range(10,1000001))
        cups_dict = {}
        firstcup = cups[0]
        for index, cup in enumerate(cups):
            next_index = (index+1) % len(cups)
            cups_dict[cup] = cups[next_index]
        #print(cups_dict)
        part2(cups_dict, moves, firstcup)
    else:
        moves = 10
        cups_dict = {}
        firstcup = cups[0]
        for index, cup in enumerate(cups):
            next_index = (index+1) % len(cups)
            cups_dict[cup] = cups[next_index]
        part2(cups_dict, moves, firstcup)

def part2(cups_dict, moves, firstcup):
    move = 1
    currentcup = firstcup
    minval = min(cups_dict.keys())
    maxval = max(cups_dict.keys())
    print(minval, maxval)
    for move in range(1, moves+1):
        if debug: 
            print("Move: {}".format(move))
            print("Current cup: {}".format(currentcup))
            print_cupdict(cups_dict)
        pickup_cups = []
        nextcup = cups_dict[currentcup]
        for i in range(3):
            pickup_cups.append(nextcup)
            nextcup = cups_dict[nextcup]
        if debug:
            print(pickup_cups)
        destination = currentcup-1
        valid_destination = False
        while not valid_destination:
            # print("Trying destination {}".format(destination))
            if destination < minval:
                destination = maxval
            if destination in pickup_cups:
                destination -= 1
                valid_destination = False
                continue
            valid_destination = True
        if debug:
            print("destination: {}".format(destination))
        # get cup after last picked up cup, that's now
        # the current cup's new next
        cups_dict[currentcup] = cups_dict[pickup_cups[-1]]
        # get cup after destination cup, that's now the
        # pickup_cups[-1]'s new destination
        cups_dict[pickup_cups[-1]] = cups_dict[destination]
        # and now next after destination is the first in the
        # picked up cups
        cups_dict[destination] = pickup_cups[0]
        currentcup = cups_dict[currentcup]
        move += 1
    print_cupdict(cups_dict)
    nextval = cups_dict[1]
    secondval = cups_dict[cups_dict[1]]
    realprint("{} * {} = {}".format(nextval, secondval, nextval*secondval))

def print_cupdict(cups_dict):
    cups_list = [1]
    back_at_beginning = False
    currval = 1
    while not back_at_beginning:
        currval = cups_dict[currval]
        if currval == 1:
            back_at_beginning = True
            break
        cups_list.append(currval)
    print(cups_list)

def part1(cups, moves):
    move = 1
    currentcup = 0
    minval = min(cups)
    maxval = max(cups)
    for move in range(1, moves+1):
        currentval = cups[currentcup]
        if debug:
            if args.part == 2:
                if (move % 1000) ==  0:
                    realprint("-- move {} --".format(move))
            else:
                print("-- move {} --".format(move))
        pick_up_indices = [(currentcup+1)%len(cups), (currentcup+2)%len(cups), (currentcup+3)%len(cups)]
        if debug:
            printcups(cups, currentcup, pick_up_indices)
        try_val = cups[currentcup]-1
        destination = pick_up_indices[0]
        while destination in pick_up_indices:
            if try_val < minval:
                try_val = maxval
            destination = cups.index(try_val)
            if destination in pick_up_indices:
                try_val -= 1
        print("destination: {}".format(cups[destination]))
        pick_up_vals = [cups[i] for i in pick_up_indices]
        print("Picking up {}".format(pick_up_vals))
        for elem in pick_up_vals:
            cups.pop(cups.index(elem))
        cups = cups[0:cups.index(try_val)+1] + pick_up_vals + cups[cups.index(try_val)+1:]
        print(cups)
        move += 1
        currentcup = (cups.index(currentval) + 1) % len(cups)
        # while cups.index(nextval) != target_index:
        #     cups = cups[1:] + cups[:1]
        #     currentcup = (cups.index(currentval) + 1) % len(cups)
    if args.part == 2:
        one_index = cups.index(1)
        realprint(cups[one_index:one_index+3])
    else:   
        while cups[0] != 1:
             cups = cups[1:] + cups[:1]
        realprint(''.join([str(a) for a in cups])[1:])

def printcups(cups, currentcup, pick_up_indices):
    outstring = "cups: "
    for index, elem in enumerate(cups):
        if index == currentcup:
            outstring += "(" + str(cups[index]) + ") "
        else:
            outstring += "{} ".format(cups[index])
    print(outstring)
    outstring = "pick up: "
    for elem in pick_up_indices:
        outstring += "{} ".format(cups[elem])
    print(outstring)
    
if __name__ == '__main__':
    global debug
    debug = True
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    parser.add_argument("--part", help="Select a part. Defaults to 1", default=1, type=int)
    parser.add_argument("-d", help="Debug. Defaults to False", action='store_true')
    args = parser.parse_args()
    if not args.d:
        debug = False
    print("Debug mode on")
    realprint("This should print regardless of debug")
    main(args)
