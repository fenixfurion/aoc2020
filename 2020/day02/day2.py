#!/usr/bin/python
import re

validcount = 0
with open('input.txt') as fd:
    for line in fd:
        match = re.match('(\d+)-(\d+) (.): (.*)', line)
        min_count = int(match.group(1))
        max_count = int(match.group(2))
        target_character = match.group(3)
        password = match.group(4)
        print("looking for {}-{} instances of {} in {}".format(
            min_count, max_count, target_character, password))
        count = password.count(target_character)
        # if count >= min_count and count <= max_count:
        valid = (password[min_count-1] == target_character) ^ (password[max_count-1] == target_character)
        if valid:
            print("+ VALID PASSWORD")
            validcount += 1 
        else:
            print("  INVALID PASSWORD")

print(validcount)
