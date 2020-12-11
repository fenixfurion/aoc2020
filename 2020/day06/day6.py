#!/usr/bin/env python

with open('input.txt','r') as fd:
    data = fd.read()
    data = data.strip()
    data = data.replace('\n\n',';')
    data = data.replace('\n', ',')
    parsed = [elem.split(',') for elem in data.split(';')]

print(parsed)
intersections = 0
for elem in parsed:
    print(elem)
    print(set.intersection(*[set(response) for response in elem]))
    intersections += len(set.intersection(*[set(response) for response in elem]))

print(intersections)
