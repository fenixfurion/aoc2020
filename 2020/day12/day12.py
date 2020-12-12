#!/usr/bin/env python3

import re

facing = 1
facings = ['N', 'E', 'S', 'W']

position = [0, 0]
with open('input.txt', 'r') as fd:
    for line in [elem.strip() for elem in fd.readlines()]:
        match = re.match('(.)(\d+)', line)
        print("Ship facing: {}, coords: {}".format(facings[facing], position))
        print("instruction: {}".format(line))
        if not match:
            print("Error: unexpected line {}".format(line))
            sys.exit(-1)
        distance = match.group(2)
        if match.group(1) == 'R':
            facing = (facing+int(int(match.group(2))/90))%4
            continue
        elif match.group(1) == 'L':
            facing = (facing-int(int(match.group(2))/90))%4
            continue
        elif match.group(1) == 'F':
            direction = facings[facing]
        else:
            direction = match.group(1)
        if direction == 'N':
            position[1] += int(distance)
        if direction == 'E':
            position[0] += int(distance)
        if direction == 'S': 
            position[1] -= int(distance)
        if direction == 'W': 
            position[0] -= int(distance)

print("Final distance: {}".format(abs(position[0])+abs(position[1])))

