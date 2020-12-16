#!/usr/bin/env python3

import sys, re
import argparse
import BitVector

def main(args):
    mask = None
    mem = {}
    with open(args.filename, 'r') as fd:
        data = [[a.strip() for a in elem.split('=')] for elem in fd.readlines()]
        pass
    #print(data)
    for elem in data:
        if elem[0] == 'mask':
            current_mask = elem[1]
            print("New mask: {}".format(current_mask))
        else:
            # assign memory with mask
            addr = int(re.match("mem\[(\d+)\]", elem[0]).group(1))
            value = int(elem[1])
            print("Addr: {}, value: {}".format(addr, value))
            addrlist = get_addresses(addr, current_mask)
            # print("Generated {} Valid addresses".format(len(addrlist)))
            print("Applying values")
            for elem in addrlist:
                addrtowrite = int(elem,2)
                #print(addrtowrite)
                mem[addrtowrite] = value
            
    sum = 0
    print("summing")
    for key in mem.keys():
        #print("{:036b}: {}".format(key, mem[key]))
        sum += mem[key]
    print(sum)

def get_addresses(addr, mask):
    addr_list = []
    x_bits = []
    masked_addr = "{:036b}".format(addr)
    for index, elem in enumerate(mask):
        if elem == 'X':
            x_bits.append(index)
        if elem == '1':
            masked_addr = list(masked_addr)
            masked_addr[index] = '1'
            masked_addr = ''.join(masked_addr)
    #print(x_bits)
    #print(1<<len(x_bits))
    for i in range(0, 1<<len(x_bits)):
        temp_addr = masked_addr
        bitstring = "{:0{width}b}".format(i, width=len(x_bits))
        #print(i, bitstring)
        for idx in range(0, len(bitstring)):
            temp_addr = list(temp_addr)
            temp_addr[x_bits[idx]] = bitstring[idx]
            temp_addr = ''.join(temp_addr)
        #print(temp_addr)
        addr_list.append(temp_addr)
    return addr_list

def apply_mask(value, mask):
    all_ones = int(36*'1',2)
    for index, bitval in enumerate(mask[::-1]):
        if bitval == 'X':
            continue
        if bitval == '0':
            value &= (all_ones ^ (1<<index))
        if bitval == '1':
            value |= (1 << index)
    return value

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    args = parser.parse_args()
    main(args)
