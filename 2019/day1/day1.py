#!/usr/bin/env python

def calc_req(mass):
    fuel_req = max(int(mass/3)-2,0)
    if fuel_req > 0:
        fuel_req += calc_req(fuel_req)
    return fuel_req

print(calc_req(100756))


fuel_req = 0
with open('input.txt', 'r') as fd:
    fuel_req = sum([calc_req(int(mass.strip())) for mass in fd.readlines()])

print(fuel_req)
