#!/usr/bin/env python

def check_valid(previous_list, check_value):
    for i in range(0,len(previous_list)):
        # print("i: {}".format(i))
        search_value = abs(check_value-previous_list[i])
        if search_value in previous_list[0:i] or search_value in previous_list[i:]:
            print("Found values {} and {} in valid list {}".format(search_value, previous_list[i], valid_list))
            return True
    print("Did not find a pair in list {} to sum to {}.".format(previous_list, check_value))
    return False

with open('input.txt', 'r') as fd:
    data = [int(elem.strip()) for elem in fd.readlines()]

preamble_length = 25

valid_list = data[0:preamble_length]
print(valid_list)

for elem in data[preamble_length:len(data)]:
    print("checking {}".format(elem))
    if not check_valid(valid_list, elem):
        print("{} is the first invalid value".format(elem))
        invalid_num = elem
        break
    else:
        print("Dropping {} from valid_list and appending {}".format(valid_list[0], elem))
        valid_list.append(elem)
        valid_list.pop(0)
        # print("Valid list: {}".format(valid_list))
    
# part 2
found_range = False
for i in range(0,len(data)):
    for j in range(i+1,len(data)):
        data_range = data[i:j]
        #print("i = {}, j = {}; list = {}".format(i, j, data_range))
        #print("i = {}, j = {}".format(i, j))
        if sum(data_range) == invalid_num:
            print("Found range {} to {} with sum {}".format(i, j, invalid_num))
            minval = min(data_range)
            maxval = max(data_range)
            print("Min: {}, Max: {}, min+max: {}".format(minval, maxval, minval+maxval))
            found_range = True
            break
        if sum(data_range) > invalid_num:
            # if sum(data[i:j]) > invalid num, continue i and reset j
            break
    if found_range:
        break
