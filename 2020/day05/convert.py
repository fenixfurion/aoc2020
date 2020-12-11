#!/usr/bin/env python

seatlist = []

with open('raw_input.txt', 'r') as fd:
    for line in fd:
        update_line = line.replace('F','0').replace('B','1').replace('L','0').replace('R','1')
        seatlist.append(int(update_line,2))

    print(seatlist)

max_seat = max(seatlist)
print('Max seat: {}'.format(max_seat))

all_seats = set(range(min(seatlist),max(seatlist)))
missing_seats = all_seats - set(seatlist)
print(missing_seats)

