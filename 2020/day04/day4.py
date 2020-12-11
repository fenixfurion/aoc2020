#!/usr/bin/env python

import re

with open('input.txt') as fd:
    data = fd.read()

#print(data)
data = data.replace('\n\n',';')
data = data.replace('\n', ' ')
data = data.replace(' ', ', ')
data = data.replace(';', '\n')
data = data.split('\n')
#print(data)

valid_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])

passports = []
for elem in data:
    passport = {}
    fieldlist = [a.strip() for a in elem.strip(' ,').split(',')]
    for field in fieldlist:
        fieldname, value = field.split(':')
        passport[fieldname] = value
    passports.append(passport)

#print(passports)

validcount = 0

for passport in passports:
    fields = set(passport.keys())
    print("{}".format(len(passport.keys())))
    #print(valid_fields-fields)
    if fields == valid_fields or valid_fields-fields == set(['cid']):
        print("Found valid passport fields: {}".format(passport))
        # birth year parsing
        if len(passport['byr']) == 4 and int(passport['byr']) >= 1920 and int(passport['byr']) <= 2002:
            pass
        else:
            print("Invalid byr {}".format(passport['byr']))
            continue
        # issue year parsing
        if len(passport['iyr']) == 4 and int(passport['iyr']) >= 2010 and int(passport['iyr']) <= 2020:
            pass
        else:
            print("Invalid iyr {}".format(passport['iyr']))
            continue
        # expiration year parsing
        if len(passport['eyr']) == 4 and int(passport['eyr']) >= 2020 and int(passport['eyr']) <= 2030:
            pass
        else:
            print("Invalid eyr {}".format(passport['eyr']))
            continue
        # height parsing
        match = re.match('^(\d+)(cm|in)$', passport['hgt'])
        if match:
            if match.group(2) == 'cm':
                min_height = 150
                max_height = 193
            else: #in
                min_height = 59
                max_height = 76
            if int(match.group(1)) >= min_height and int(match.group(1)) <= max_height:
                pass
            else:
                print("Invalid height {} {}".format(match.group(1), match.group(2)))
                continue
        else:
            print("Invalid height format {}".format(passport['hgt']))
            continue
        # hair color parsing
        match = re.match('^#[0-9a-f]{6}$', passport['hcl'])
        if match:
            pass
        else:
            print("Invalid hair color {}".format(passport['hcl']))
            continue
        # eye color parsing
        valid_eyes = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        if passport['ecl'] not in valid_eyes:
            print("Invalid eye color {}".format(passport['ecl']))
            continue
        # passport ID parsing
        match = re.match('^[0-9]{9}$', passport['pid'])
        if match:
            pass
        else:
            print("Invalid passport ID {}".format(passport['pid']))
            continue
        validcount += 1
    else:
        print("invalid passport fields: {}".format(passport))
        continue

print("Total passports: {}".format(len(passports)))
print(validcount)
