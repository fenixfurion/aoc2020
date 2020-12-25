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
    with open(args.filename, 'r') as fd:
        pub_key_card, pub_key_door = [int(line.strip()) for line in fd.readlines()]
    print("Card Public Key: {}".format(pub_key_card))
    print("Door Public Key: {}".format(pub_key_door))
    
    subject_number = 7
    loop_size_card = find_loop_size(pub_key_card, subject_number)
    print("Card loop size: {}".format(loop_size_card))
    loop_size_door = find_loop_size(pub_key_door, subject_number)
    print("Door loop size: {}".format(loop_size_door))

    encryption_key_1 = get_encryption_key(pub_key_card, loop_size_door)
    encryption_key_2 = get_encryption_key(pub_key_door, loop_size_card)
    print("1: {}, 2: {}".format(encryption_key_1, encryption_key_2))

# this is just diffie-hellman...
def find_loop_size(public_key, subject_number):
    value = 1
    loop_size = 0
    while value != public_key:
        value = (value * subject_number) % 20201227
        loop_size += 1
    return loop_size

def get_encryption_key(subject_number, loop_size):
    key = 1
    for i in range(loop_size):
        key = (key * subject_number) % 20201227
        i += 1
    return key

if __name__ == '__main__':
    global debug
    debug = True
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    parser.add_argument("-d", help="Debug. Defaults to False", action='store_true')
    args = parser.parse_args()
    if not args.d:
        debug = False
    print("Debug mode on")
    realprint("This should print regardless of debug")
    main(args)
