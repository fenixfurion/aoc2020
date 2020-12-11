#!/usr/bin/python

dataset = []
with open('input.txt','r') as fd:
    for line in fd:
        dataset.append(int(line))

print(dataset)
dataset.sort()

for a in dataset:
    for b in dataset[::-1]:
        for c in dataset:
            if a == b or b == c or a == c: 
                continue
            if a+b+c == 2020:
                print('Found a, b, c: {}, {}, {}'.format(a, b, c))
                print("a*b*c = {}".format(a*b*c))
                break
            elif a+b+c > 2020:
                continue
        

