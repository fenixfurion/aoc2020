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
        # need to parse each line separately, character by character
        data = []
        for line in [line.strip() for line in fd.readlines()]:
            current_line = []
            print(line)
            state = 'new'
            currdata = ''
            for char in line:
                if state == 'new':
                    if char == 's' or char == 'n':
                        state = 'diagonal'
                        currdata = char
                        continue
                    else:
                        current_line.append(char)
                        continue
                if state == 'diagonal':
                    current_line.append(currdata + char)
                    currdata = ''
                    state = 'new'
                    continue

            print(current_line)
            data.append(current_line)
        print(len(current_line))
        directions = {
            'e':  [1,-1,0],
            'se': [0,-1,1],
            'sw': [-1,0,1],
            'w':  [-1,1,0],
            'nw': [0,1,-1],
            'ne': [1,0,-1],
        }
        tiles = {}
        for line in data:
            #print("Checking line {}".format(line))
            coord = [0,0,0]
            for direction in line:
                coord[0] += directions[direction][0]
                coord[1] += directions[direction][1]
                coord[2] += directions[direction][2]
            #print(coord)
            coord = tuple(coord)
            if coord not in tiles.keys():
               # new tile, flip to black
               tiles[coord] = 'black'
            else:
                if tiles[coord] == 'black':
                    tiles[coord] = 'white'
                else:
                    tiles[coord] = 'black'
        bcount = 0
        for key in tiles.keys():
            if tiles[key] == 'black':
                bcount += 1
        realprint("Found {} black tiles".format(bcount))
        # part 2
        days = 100
        for day in range(0,days + 1):
            bcount = 0
            for key in tiles.keys():
                if tiles[key] == 'black':
                    bcount += 1
            realprint("Day {}: {}".format(day, bcount))
            tiles = execute_day(tiles)
            


def execute_day(tiles):
    directions = {
        'e':  [1,-1,0],
        'se': [0,-1,1],
        'sw': [-1,0,1],
        'w':  [-1,1,0],
        'nw': [0,1,-1],
        'ne': [1,0,-1],
    }
    next_tiles = {}
    neighboring_tiles = {}
    for key in tiles:
        if tiles[key] == 'white':
            continue
        # assume the current tile is black, so 
        # all neighbors get +1 black
        tile = tiles[key]
        #neighbor_list = []
        for direction in directions:
            neighbor = list(key)
            # temporarily convert so we can change the value
            # this is bad
            neighbor = list(neighbor)
            neighbor[0] += directions[direction][0]
            neighbor[1] += directions[direction][1]
            neighbor[2] += directions[direction][2]
            neighbor = tuple(neighbor)
            #neighbor_list.append(neighbor)
            if neighbor in neighboring_tiles: # check if black or white
                neighboring_tiles[neighbor] += 1
            else:
                neighboring_tiles[neighbor] = 1
        # print("coord: {}, NL: {}".format(key, neighbor_list))
    # print("NT: {}".format(neighboring_tiles))
    next_tiles = {}
    for tile_coord in list(set(neighboring_tiles) | set(tiles)):
        if tile_coord in neighboring_tiles:
            neighbor_count = neighboring_tiles[tile_coord]
        else:
            neighbor_count = -1
        if tile_coord in tiles:
            tile_color = tiles[tile_coord]
        else:
            tile_color = 'assumed white'
        # print("Coord: {}: color: {} neighbors: {}".format(tile_coord, tile_color, neighbor_count))
        if tile_coord in tiles and tiles[tile_coord] == 'black':
            # 0 or >  2 -> white
            if tile_coord in neighboring_tiles and neighboring_tiles[tile_coord] <= 2:
                next_tiles[tile_coord] = 'black'
            else:
                next_tiles[tile_coord] = 'white'
                # print("## Tile {} flips to white".format(tile_coord))
        else: # white
            if tile_coord in neighboring_tiles and neighboring_tiles[tile_coord] == 2:
                next_tiles[tile_coord] = 'black'
                # print("# Tile {} flips to black".format(tile_coord))
            # else don't even worry about it, it's white
    print(len(next_tiles))
    return next_tiles
                
                

if __name__ == '__main__':
    global debug
    debug = True
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    parser.add_argument("-d", help="Debug. Defaults to False", action='store_true')
    args = parser.parse_args()
    if not args.d:
        debug = False
    print("Debug mode on")
    realprint("This should print regardless of debug")
    main(args)
