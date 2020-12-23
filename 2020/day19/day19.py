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
    rules = {}
    messages = []
    with open(args.filename, 'r') as fd:
        state = "rules"
        for line in [elem.strip() for elem in fd.readlines()]:
            if state == "rules":
                match = re.match("(\d+): (.*)", line)
                if not match:
                    state = "messages"
                    continue
                rules[int(match.group(1))] = match.group(2)
            elif state == "messages":
                messages.append(line)
    # clean up rules first
    for key in rules.keys():
        if '"' in rules[key]:
            rules[key] = rules[key].strip('"')
        else:
            # split by | and then split each rule into characters
            rules[key] = rules[key] #[[int(a) for a in elem.strip().split()] for elem in rules[key].split('|')]
            #if len(rules[key]) == 1:
            #    rules[key] = rules[key][0]
    print(rules)
    print(messages)
    expanded_rules = regexpand_all_rules(rules)
    #expanded_rules = expand_all_rules(rules)
    realprint(expanded_rules)
    #valid_strings = traverse_rule(expanded_rules[0])
    #print(valid_strings)
    #for message in messages:
    #    check_valid(expanded_rules[0], message)
    matches = 0
    for message in messages:
        if re.match('^' + expanded_rules[0] + '$', message):
            print("{} matches rule 0".format(message))
            matches += 1
    realprint(matches)

def regexpand_all_rules(rules):
    rules_to_expand = len(rules.keys())
    expanded_rules = rules.copy()
    total_expansion_needed = len(rules.keys())
    loops = 0
    while total_expansion_needed != 0:
        total_expansion_needed = 0
        for key in [0]:
            print("Going to expand rule {}".format(key))
            needs_expansion, expanded_rules[key] = regexpand_rule(expanded_rules, expanded_rules[key])
            print("New rule: {}".format(expanded_rules[key]))
            total_expansion_needed += needs_expansion
            print("Expansion needed: {}".format(total_expansion_needed))
        loops += 1
        # this is awful but since our input is bounded just break out 
        # if our regex gets too big
        if loops == 20:
            break
    # clean up spaces
    for key in expanded_rules.keys():
        expanded_rules[key] = expanded_rules[key].replace(' ','')
    return expanded_rules

def regexpand_rule(all_rules, rule):
    print("Expanding rule {}".format(rule))
    unexpanded = 0
    expanded_rule = ' ( ' + rule + ' ) '
    expanded_rule = expanded_rule.split()
    for index, elem in enumerate(expanded_rule):
        #print("index: {}, elem: {}".format(index, elem))
        match = re.match('\d+', expanded_rule[index])
        if match:
           # print("finding rule {}".format(expanded_rule[index]))
            if int(expanded_rule[index]) in all_rules.keys():
                #print("Rule {} -> {}".format(expanded_rule[index], all_rules[int(expanded_rule[index])]))
                expanded_rule[index] = ' ( {} ) '.format(str(all_rules[int(expanded_rule[index])]))
    expanded_rule = ''.join(expanded_rule)
    if re.search('[0-9]', expanded_rule):
        unexpanded = 1
    # print("expanded: {}".format(expanded_rule))
    return unexpanded, expanded_rule


def expand_all_rules(rules):
    rules_to_expand = len(rules.keys())
    expanded_rules = rules.copy()
    total_expansion_needed = len(rules.keys())
    while total_expansion_needed != 0:
        total_expansion_needed = 0
        for key in expanded_rules:
            print("Going to expand rule {}".format(key))
            needs_expansion, expanded_rules[key] = expand_rule(expanded_rules, expanded_rules[key])
            print("New rule: {}".format(expanded_rules[key]))
            total_expansion_needed += needs_expansion
            print("Expansion needed: {}".format(total_expansion_needed))
    return expanded_rules

def expand_rule(all_rules, rule):
    print("Expanding rule {}".format(rule))
    unexpanded = 0
    if type(rule) == list:
        expanded_rule = [None]*len(rule)
        # expand each element
        for index, elem in enumerate(rule):
            unexpanded, expanded_rule[index] = expand_rule(all_rules, elem)
    elif type(rule) == int:
        # expand based on current rules
        expanded_rule = all_rules[rule]
        unexpanded += 1
    elif type(rule) == str:
        # don't need to expand, keep the same
        expanded_rule = rule
    return unexpanded, expanded_rule

def check_valid(rule, message):
    print("Checking message {} against rule {}".format(message, rule))


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
