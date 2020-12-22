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
    food_list = []
    with open(args.filename, 'r') as fd:
        for line in [line.strip() for line in fd.readlines()]:
            print("###")
            ingredients, allergens = line.strip(')').split(' (contains')
            ingredients = ingredients.strip().split()
            allergens = [elem.strip() for elem in allergens.strip().split(',')]
            print(ingredients)
            print(allergens)
            food_list.append((ingredients, allergens))
    print(food_list)
    # allergen : ingredient is a 1:1 map
    # not all allergens are marked 
    all_ingredients = []
    all_allergens = []
    for elem in food_list:
        all_ingredients += elem[0]
        all_allergens += elem[1]
    all_ingredients = set(all_ingredients)
    all_allergens = set(all_allergens)
    print("Ingredients: {}".format(all_ingredients))
    print("Allergens: {}".format(all_allergens))
    possible_allergens = {}
    mapped_allergens = set()
    mapped_ingredients = set()
    ing_allergen_map = {}
    while mapped_allergens != all_allergens:
        print("ing_allergen_map: {}".format(ing_allergen_map))
        print("mapped_allergens: {}".format(mapped_allergens))
        print("mapped_ingredients: {}".format(mapped_ingredients))
        for allergen in all_allergens:
            ing_list = None
            print(allergen)
            if allergen in mapped_allergens:
                continue
            for food in food_list:
                print(food)
                if allergen not in food[1]:
                    continue
                if not ing_list:
                    ing_list = (set(food[0]) - mapped_ingredients)
                else:
                    ing_list &= set(food[0])
                print("Pruned {} list to {}".format(allergen, ing_list))
                if len(ing_list) == 1:
                    print("Allergen {} is definitely in {}".format(allergen, list(ing_list)[0]))
                    mapped_allergens |= set([allergen])
                    mapped_ingredients |= set([list(ing_list)[0]])
                    ing_allergen_map[str(list(ing_list)[0])] = allergen
                    break
    print("ing_allergen_map: {}".format(ing_allergen_map))
    print("mapped_allergens: {}".format(mapped_allergens))
    print("mapped_ingredients: {}".format(mapped_ingredients))
    non_allergen_food_count = 0
    for food in food_list:
        for ing in food[0]:
            if ing not in mapped_ingredients:
                non_allergen_food_count += 1

    realprint(non_allergen_food_count)
    dangerous_ingredients = list(mapped_ingredients)
    dangerous_ingredients.sort(key = lambda ingredient: ing_allergen_map[ingredient])
    print(','.join(dangerous_ingredients))

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
