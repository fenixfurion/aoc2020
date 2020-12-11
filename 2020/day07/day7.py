#!/usr/bin/env python

import argparse, re, sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", help="Set a non-default rules file.", default="rules.txt")
    args = parser.parse_args()
    bag_rules = build_bag_rules(args.rules)
    count = 0
    # for color in bag_rules.keys():
    #     print("Checking color {}".format(color))
    #     count += (count_colors(bag_rules, color, 'shiny gold') > 0)
    count = count_bags(bag_rules, 'shiny gold')
    print(count)
    

def count_bags(bag_rules, color, depth=0):
    count = 0
    print("{} Checking contents of {} bag".format("#"*depth, color)) 
    for bag_info in bag_rules[color]:
        # add top level bags here
        print(bag_info)
        count += int(bag_info[1])
        count += int(bag_info[1]) * count_bags(bag_rules, bag_info[0])
    return count

def count_colors(bag_rules, color, target_color, depth=0):
    count = 0
    #print("{} {}".format("#"*depth, color))
    for bag_info in bag_rules[color]:
        if bag_info[0] == target_color:
            #print("{} FOUND gold here".format("#"*depth))
            return 1
            #count += int(bag_info[1])
        if count_colors(bag_rules, bag_info[0], target_color, depth+1):
            # immediately return
            return 1
    return count

def build_bag_rules(rules_file):
    print("Building rules from file {}".format(rules_file))
    bag_rules = {}
    with open(rules_file, 'r') as fd:
        for line in fd:
            match = re.match("^(\w+(?:\s+\w+)?)\s+bags contain (.*)\.$",line)
            if not match:
                print("ERROR: line {} does not match regex.".format(line))
                sys.exit(-1)
            else:
                current_color = match.group(1)
                if current_color in bag_rules.keys():
                    print("ERROR: bag color {} already defined!".format(current_color))
                    sys.exit(-1)
                bag_rules[current_color] = []
                # build contents now
                if "no other" in match.group(2):
                    continue
                current_bag_rules = match.group(2).split(',')
                #print(current_bag_rules)
                for rule in current_bag_rules:
                    match = re.match("^(\d+)\s+(\w+\s+\w+) bag", rule.strip())
                    if not match:
                        print("ERROR: rule {} invalid format!".format(rule))
                        sys.exit(-1)
                    count = match.group(1)
                    rule_color = match.group(2)
                    bag_rules[current_color].append((match.group(2), match.group(1)))
        #print(bag_rules)
    return bag_rules

if __name__ == '__main__':
    main()
