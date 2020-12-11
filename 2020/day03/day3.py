#!/usr/bin/python


with open('input.txt','r') as fd:
    route = fd.readlines()

def traverse(x_vel, y_vel):
    trees_hit = 0
    y = 0
    x = 0
    while y<len(route):
        print(route[y].strip())
        length = len(route[y].strip())
        if route[y][x] == '#':
            trees_hit += 1 
        x = (x+x_vel)%length
        y = (y+y_vel)
    return trees_hit

count = traverse(1,1)
count *= traverse(3,1)
count *= traverse(5,1)
count *= traverse(7,1)
count *= traverse(1,2)

print(count)

