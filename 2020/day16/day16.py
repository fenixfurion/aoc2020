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
    nearby_tickets = []
    raw_rules = {}
    with open(args.filename, 'r') as fd:
        # parse rules
        parse_state = 'rules'
        for line in [elem.strip() for elem in fd.readlines()]:
            if "your ticket" in line:
                # start parsing your ticket
                parse_state = 'your_ticket'
                continue
            if "nearby tickets" in line:
                # parse nearby
                parse_state = 'nearby_tickets'
                continue
            if parse_state == 'rules':
                if ':' in line:
                    rule_name = line.split(':')[0]
                    rule_ranges = [elem.strip() for elem in line.split(':')[1].split(' or ')]
                    print("Rule name: {}, ranges: {}".format(rule_name, rule_ranges))
                    raw_rules[rule_name] = rule_ranges
                else:
                    print("Ignoring line {}".format(line))
            if parse_state == 'your_ticket':
                your_ticket = [int(elem) for elem in line.strip().split(',')]
                print("Added self ticket {}".format(your_ticket))
                parse_state = 'other'
            if parse_state == 'nearby_tickets':
                print("Added other ticket {}".format(line))
                nearby_tickets.append([int(elem) for elem in line.strip().split(',')])
    #print("nearby_tickets: {}".format(nearby_tickets))
    # create an array with all values and valid rules for each number
    print("Raw rules: {}".format(raw_rules))
    rules = {}
    for rule in raw_rules.keys():
        print("Rule: {}".format(rule))
        for elem in raw_rules[rule]:
            rule_min, rule_max = [int(a) for a in elem.split('-')]
            print("Min: {}, Max: {}".format(rule_min, rule_max))
            for value in range(rule_min, rule_max+1):
                if value in rules.keys():
                    rules[value].append(rule)
                else:
                    rules[value] = [rule]
    #print(rules)
    error_rate = 0
    valid_tickets = [your_ticket]
    for ticket in nearby_tickets:
        valid = True
        print("Checking ticket {}".format(ticket))
        for elem in ticket:
            if elem not in rules.keys():
                valid = False
                print("Value {} not in valid rules".format(elem))
                error_rate += elem
        if valid:
            valid_tickets.append(ticket)
    realprint("Error rate: {}".format(error_rate))
    # generate a list of rules based on all valid tickets
    # this duplicates by reference...
    #rule_order = [set(raw_rules.keys())]*len(raw_rules.keys())
    rule_order = []
    for i in range(len(raw_rules.keys())):
        rule_order.append(set(raw_rules.keys()))
    print(rule_order)
    for ticket in valid_tickets:
        print("Ticket {}".format(ticket))
        for index, elem in enumerate(ticket):
            print("Current rules for index {}: {}".format(index, rule_order[index]))
            available_rules = rules[ticket[index]]
            print("Index: {}, value: {}, available rules: {}".format(index, elem, available_rules))
            rule_order[index] &= set(available_rules)
    # now prune rules 
    lengths = [len(elem) for elem in rule_order]
    for i in range(len(lengths)):
        print("index {}: length {}: {}".format(i, lengths[i], rule_order[i]))
    pruned_rules = []
    while any([len(elem) > 1 for elem in rule_order]):
        print("Pruned rules: {}".format(pruned_rules))
        for index, elem in enumerate(rule_order):
            if len(elem) == 1 and elem not in pruned_rules:
                print("Index {} has only one possible rule: {}".format(index, elem))
                for index_mod, elem_mod in enumerate(rule_order):
                    if index_mod != index:
                        rule_order[index_mod] -= elem
                pruned_rules.append(list(elem)[0])
                continue
    print(rule_order)
    final_rule_order = [list(elem)[0] for elem in rule_order]
    realprint(final_rule_order)
    final_mult = 1
    for index, rule in enumerate(final_rule_order):
        if 'departure' in rule:
            final_mult *= your_ticket[index]
    realprint("Final multiplication: {}".format(final_mult))
    


if __name__ == '__main__':
    global debug
    debug = True
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    parser.add_argument("-d", help="Debug. Defaults to False", action='store_true')
    args = parser.parse_args()
    # print(args.d)
    if not args.d:
        debug = False
    main(args)
