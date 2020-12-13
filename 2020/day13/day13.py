#!/usr/bin/env python3

import sys, re
import argparse
    
# day13 boilerplate code for being one of the first people done

def main(args):
    with open(args.filename, 'r') as fd:
        earliest_time = int(fd.readline().strip())
        buses = fd.readline().strip().split(',')
    print(earliest_time)
    print(buses)
    id_offset = []
    for offset, bus in enumerate(buses):
        if bus == 'x':
            continue
        else:
            id_offset.append([int(bus), offset])
            earliest_multiple = int(earliest_time/int(bus))+1
            time = earliest_multiple*int(bus)
            time_delta = time - earliest_time
            print("bus: {}, closest multiple: {}, time = {}, depart-earliest = {}".format(
                bus, earliest_multiple, earliest_multiple*int(bus), time_delta))
    print(id_offset)
    found = False
    id_offset.sort(key=lambda x: -1*x[0])
    print(id_offset)
    t = 0-id_offset[0][1]
    loopindex = 1
    step = id_offset[0][0]
    lastspace = 0
    startpos = 1
    sadcount = 0
    while not found:
        if not (loopindex % 100000):
            print("Checking time {}".format(t))
        bad = False
        for index in range(startpos, len(id_offset)):
            #print("{} % {} needs to be 0".format(t+id_offset[index][1], id_offset[index][0]))
            if ((t+id_offset[index][1]) < id_offset[index][0]) or ((t+id_offset[index][1]) % id_offset[index][0]) != 0:
                t += step 
                loopindex += 1
                bad = True
                break
            else:
                print("Found LCM of {} and {} with offset at time {}".format(id_offset[0][0], id_offset[index][0],t))
                if lastspace == 0:
                    lastspace = t
                    print("Skipping first instance..., setting initial collision to {}".format(t))
                else:
                    step = t-lastspace
                    print("Found periodicity between these two at period {}".format(step))
                    startpos += 1
                    lastspace = 0
                    if sadcount > 10:
                        sys.exit()
                    sadcount += 1
        if not bad:
            found = True
    print("Found time t satisfying constraints: {}".format(t))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    args = parser.parse_args()
    main(args)
