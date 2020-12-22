#!/usr/bin/env python3
import sys, re, math
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
        state = 'header'
        current_tile = None
        tiles = {}
        for line in [elem.strip() for elem in fd.readlines()]:
            print("Line: {}, state = {}".format(line, state))
            if state == 'header':
                current_tile = int(re.match('Tile (\d+):', line).group(1))
                tiles[current_tile] = []
                state = 'data'
                continue
            if state == 'break':
                state = 'header'
                continue
            if state == 'data':
                match = re.match('[\.#]+', line)
                if not match:
                    state = 'header'
                    continue
                tiles[current_tile].append(line)
        print(tiles)
    tile_list = []
    for key in tiles.keys():
        tile_list.append(tile_class(key, tiles[key]))
    border_list = []
    for tile in tile_list:
        border_list += tile.borders
        border_list += tile.borders_rev
    border_list.sort()
    unique = list(set(border_list))
    unique.sort()
    low_count_num = []
    for elem in unique:
        print("{}: {}".format(elem, border_list.count(elem)))
        if border_list.count(elem) == 1:
            low_count_num.append(elem)

    print(low_count_num)
    idprod = 1
    start_tile = 0
    tile_dict = {}
    uniq_edges = {}
    for tile in tile_list:
        tile_dict[tile.id] = tile
        edges = set(tile.borders) & set(low_count_num) 
        edgecount = len(edges)
        if edgecount == 2:
            print("Tile id {} has 2 unique edges: {}".format(tile.id, edges))
            uniq_edges = edges
            idprod *= tile.id
            start_tile = tile.id
    realprint(len(tile_list))
    side_length = int(math.sqrt(len(tile_list)))
    realprint(idprod)

    # use one of the corner tiles as 0,0 and oriented where it's top left
    grid = []
    for i in range(side_length):
        grid.append([-1]*side_length)
    print(grid)
    print(tile_dict[start_tile].id)
    print(tile_dict[start_tile].borders)
    # [0N, 1E, 2S, 3W]
    used_tiles = [start_tile]
    curr_tile = tile_dict[start_tile]
    print("Edges: {}, B[0]: {}, B[3]: {}, B_r[0]: {}, B_r[3]: {}".format(uniq_edges, curr_tile.borders[0], curr_tile.borders[3], curr_tile.borders_rev[0], curr_tile.borders_rev[3]))
    while ((curr_tile.borders[0] not in uniq_edges 
        and curr_tile.borders_rev[0] not in uniq_edges)
        or (curr_tile.borders[3] not in uniq_edges 
        and curr_tile.borders_rev[3] not in uniq_edges)):
        curr_tile.rotate()
        print("Edges: {}, B[0]: {}, B[3]: {}, B_r[0]: {}, B_r[3]: {}".format(uniq_edges, curr_tile.borders[0], curr_tile.borders[3], curr_tile.borders_rev[0], curr_tile.borders_rev[3]))
    grid[0][0] = start_tile
    print("done rotating")
    for y in range(len(grid)):
        for x in range(len(grid)):
            print("X: {:02d}, Y: {:02d}. Tile: {}".format(x, y, grid[y][x]))
            # brain off no thoughts
            # if y == 0, get fit from left tile
            if y == 0 and x == 0:
                continue
            if y == 0 or x > 0:
                grid[y][x] = fit_tile(tile_dict, used_tiles, grid[y][x-1], 1)
                used_tiles.append(grid[y][x])
                print(grid)
            # else get fit from tile above
            else:
                grid[y][x] = fit_tile(tile_dict, used_tiles, grid[y-1][x], 2)
                used_tiles.append(grid[y][x])

    # now strip the borders from every tile
    for tile in tile_dict.keys():
        temp_data = []
        for index, elem in enumerate(tile_dict[tile].data):
            if index == (len(tile_dict[tile].data)-1) or index == 0:
                continue
            else:
                temp_data.append(tile_dict[tile].data[index][1:-1])
        tile_dict[tile].data = temp_data

    full_data = []
    for row in range(0, len(tile_dict[grid[0][0]].data)*len(grid)):
        full_data.append('')
    for row in range(0, len(grid)):
        #print("Row: {}".format(row))
        for y in range(0, len(tile_dict[grid[0][0]].data)):
            #print("y: {}".format(y))
            for x in range(0, len(grid)):
                full_data[(row*len(tile_dict[grid[0][0]].data))+y] += tile_dict[grid[row][x]].data[y]
    print(len(full_data))
    print(len(full_data[0]))
    for row in full_data:
        print(row)

    full_image = tile_class(0, full_data)
    # sea monster: 
    ###                   # 
    ### #    ##    ##    ###
    ###  #  #  #  #  #  #   
    sm_row1 = "^..................#." # 1
    sm_row2 = "^#....##....##....###" # 8
    sm_row3 = "^.#..#..#..#..#..#..." # 6
    rotations = 0
    flips = 0
    max_seamonsters = 0
    for flip in range(0, 2):
        for rotation in range(0, 4):
            current_seamonsters = 0
            print("Image {} {}".format(flip, rotation))
            for row in full_image.data:
                print(row)
            for index, row in enumerate(full_image.data):
                for column in range(0, len(full_image.data[0])-20):
                    match = re.match(sm_row1, full_image.data[index][column:])
                    if match:
                        #print("found match1 on line {} col {}, {}".format(index, column, row))
                        #print("Start: {}".format(match.start()))
                        if index > len(full_image.data)-2: 
                            continue
                        match2 = re.match(sm_row2, full_image.data[index+1][column:])
                        if match2:
                            print("found match2 on line {} col {}, {}".format(index+1, column, full_image.data[index+1]))
                            match3 = re.match(sm_row3, full_image.data[index+2][column:])
                            if match3:
                                print("found match3 on line {} col {}, {}".format(index+2, column, full_image.data[index+2]))
                                current_seamonsters += 1
                                if max_seamonsters < current_seamonsters:
                                    max_seamonsters = current_seamonsters
            full_image.rotate()
        full_image.flip()
    total_sea = 0
    for row in full_image.data:
        total_sea += row.count('#')
    realprint("Max seamonsters: {}".format(max_seamonsters))
    realprint("Total sea: {}".format(total_sea))
    realprint("Non seamonster sea: {}".format(total_sea-(max_seamonsters*15)))

def fit_tile(tile_dict, used_tiles, anchor, anchor_side):
    # print(locals())
    print("Anchor: {}, sides: {}, side: {}".format(anchor,tile_dict[anchor].borders, tile_dict[anchor].borders[anchor_side]))
    match_tile = None
    for tile in tile_dict.keys():
        curr_tile = tile_dict[tile]
        if tile in used_tiles:
            continue
        if (tile_dict[anchor].borders[anchor_side] in curr_tile.borders or 
           tile_dict[anchor].borders[anchor_side] in curr_tile.borders_rev):
            print("Found tile {} with matching sides {} {}".format(curr_tile.id, curr_tile.borders, curr_tile.borders_rev))
            match_tile = curr_tile.id
            break
    if not match_tile:
        print("Something went really wrong here")
        sys.exit(-1)
    print("Anchor: {}, side: {}, match_tile: {}".format(anchor, anchor_side, match_tile))
    target_side = -1
    if anchor_side == 1:
        target_side = 3 # west
    elif anchor_side == 2:
        target_side = 0 # north
    i = 0
    # note that since i'm doing this as a > V < ^ style, we need to match
    # the reverse border with the regular border
    if tile_dict[anchor].borders[anchor_side] in curr_tile.borders:
        curr_tile.flip()
    rotations = 0
    while curr_tile.borders_rev[target_side] != tile_dict[anchor].borders[anchor_side]:
        if rotations > 4:
            print("Something went really wrong here")
            sys.exit(-1)
        curr_tile.rotate()
        rotations += 1
            
    print("Finished rotating tile.")
    return match_tile
        


class tile_class():
    def tile_to_int(self, value):
        tile_data = int(value.replace('.','0').replace('#','1'),2)
        #print("Original value: {}, tile num: {}".format(value, tile_data))
        return tile_data

    def __init__(self, tile_id, data):
        self.id = tile_id
        print("Generating tile id {}".format(self.id))
        self.data = data
        print("Tile data {}".format(self.data))
        # express tiles as a list of [NESW] sides?
        self.generate_borders()
    
    def generate_borders(self):
        self.borders = []
        self.borders.append(self.tile_to_int(self.data[0]))
        self.borders.append(self.tile_to_int(''.join([elem[-1] for elem in self.data])))
        self.borders.append(self.tile_to_int(self.data[-1][::-1]))
        self.borders.append(self.tile_to_int(''.join([elem[0] for elem in self.data[::-1]])))
        # print(self.borders)
        self.borders_rev = []
        self.borders_rev.append(self.tile_to_int(self.data[0][::-1]))
        self.borders_rev.append(self.tile_to_int(''.join([elem[-1] for elem in self.data[::-1]])))
        self.borders_rev.append(self.tile_to_int(self.data[-1]))
        self.borders_rev.append(self.tile_to_int(''.join([elem[0] for elem in self.data])))
        # print(self.borders_rev)


    def rotate(self):
        print("Rotating tile {} clockwise.".format(self.id))
        # for elem in self.data:
        #     print(elem)
        # print("Rotating data.")
        self.data = list(zip(*self.data[::-1]))
        for index, elem in enumerate(self.data):
            self.data[index] = ''.join(list(elem))
        #    print(self.data[index])
        print(self.borders)
        self.generate_borders()
        print(self.borders)

    def flip(self):
        print("Flipping tile {} vertically.".format(self.id))
        # for elem in self.data:
        #     print(elem)
        self.data = self.data[::-1]
        #print("Flipping data.")
        # for elem in self.data:
        #     print(elem)
        print(self.borders)
        self.generate_borders()
        print(self.borders)
            


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
