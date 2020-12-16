#!/usr/bin/env python3

import sys, re
import argparse

def main(args):
    with open(args.filename, 'r') as fd:
        start_nums = [int(elem) for elem in fd.readlines()[0].strip().split(',')]
    
    turn = 1
    number_tracker = {}
    first_time = True
    while turn <= 30000000:
        # starting numbers
        if turn % 1000000 == 0:
            print("Turn {}".format(turn))
        if turn < len(start_nums)+1:
            print(" Adding start number {}".format(start_nums[turn-1]))
            number_tracker[start_nums[turn-1]] = [turn]
            last_num = start_nums[turn-1]
            turn += 1
            print(number_tracker)
            continue
        if len(number_tracker[last_num]) > 1:
            # already exists, now speak the difference between last time and most recent time
            next_num = number_tracker[last_num][-1]-number_tracker[last_num][-2]
            # print(" Number {} already has been spoken: {}, {}".format(last_num, number_tracker[last_num], next_num))
            number_tracker[last_num].pop(0)
            last_num = next_num
        else:
            # number has NOT showed up, last_num is now 0
            # print(" Number {} has not been spoken, next is 0.".format(last_num))
            last_num = 0
        if last_num not in number_tracker.keys():
            number_tracker[last_num] = []
        number_tracker[last_num].append(turn)
        # print(number_tracker)
        turn += 1
    print("Turn: {}, number: {}".format(turn-1, next_num))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    args = parser.parse_args()
    main(args)
