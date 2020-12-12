#!/usr/bin/env python3
import re
import time
t0 = time.time()
waypoint_position = [10, 1]
ship_position = [0, 0]
lineformat = re.compile('(.)(\d+)')
with open('input.txt', 'r') as fd:
    for line in [elem.strip() for elem in fd.readlines()]:
        match = lineformat.match(line)
        #print("Ship coords: {} | Waypoint coords: {}".format(ship_position, waypoint_position))
        #print("instruction: {}".format(line))
        if not match:
            print("Error: unexpected line {}".format(line))
            sys.exit(-1)
        distance = match.group(2)
        if match.group(1) == 'R':
            for i in range(int(int(match.group(2))/90)):
                temp_position = waypoint_position[0]
                waypoint_position[0] = waypoint_position[1]
                waypoint_position[1] = temp_position*-1
            continue
        elif match.group(1) == 'L':
            for i in range(int(int(match.group(2))/90)):
                temp_position = waypoint_position[0]
                waypoint_position[0] = waypoint_position[1]*-1
                waypoint_position[1] = temp_position
            continue
        elif match.group(1) == 'F':
            ship_position[0] += int(match.group(2))*waypoint_position[0]
            ship_position[1] += int(match.group(2))*waypoint_position[1]
            continue
        if match.group(1) == 'N':
            waypoint_position[1] += int(distance)
        if match.group(1) == 'E':
            waypoint_position[0] += int(distance)
        if match.group(1) == 'S': 
            waypoint_position[1] -= int(distance)
        if match.group(1) == 'W': 
            waypoint_position[0] -= int(distance)
t_end = time.time()
print("Ship coords: {} | Waypoint coords: {}".format(ship_position, waypoint_position))
print("Final distance: {}".format(abs(ship_position[0])+abs(ship_position[1])))
print("Time taken: {}ms".format((t_end-t0)*1000))

