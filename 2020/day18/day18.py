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
        data = [elem.strip() for elem in fd.readlines()]
        pass
    print(data)
    total = 0
    for line in data:
        total += weird_eval(line)
    realprint(total)

def weird_eval(line):
    # time to tokenize and traverse the tree aaa
    line = line.replace('(', ' ( ').replace(')', ' ) ')
    line = re.sub('\s+', ' ', line)
    tokens = line.split()
    output = []
    operator_stack = []
    for token in tokens:
        print("###")
        print("Token: {}".format(token))
        print("Operator stack: {}".format(operator_stack))
        print("Output: {}".format(output))
        # high precedence
        if token == '+':
            if len(operator_stack) == 0 or operator_stack[-1] == '(' or operator_stack[-1] == '*':
                operator_stack.append(token)
            else:
                operator = operator_stack.pop()
                print("Popped {}".format(operator))
                while len(operator_stack) != 0 and operator != '(' and operator != '+':
                    output.append(operator)
                    operator = operator_stack.pop()
                    print("Popped {}".format(operator))
                if operator == '(' or operator == '+':
                    operator_stack.append(operator)
                else:
                    output.append(operator)
                operator_stack.append(token)
        elif token == '*':
            if len(operator_stack) == 0 or operator_stack[-1] == '(':
                operator_stack.append(token)
            else:
                operator = operator_stack.pop()
                print("Popped {}".format(operator))
                while len(operator_stack) != 0 and operator != '(':
                    output.append(operator)
                    operator = operator_stack.pop()
                    print("Popped {}".format(operator))
                if operator == '(':
                    operator_stack.append(operator)
                else:
                    output.append(operator)
                operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            leftparen_found = False
            while not leftparen_found:
                # discard '('
                operator = operator_stack.pop()
                print("Popped {}".format(operator))
                if operator != '(':
                    output.append(operator)
                else:
                    leftparen_found = True
        else: # operand
            output.append(int(token))
        # we don't care about precendence
    for i in range(len(operator_stack)):
        output.append(operator_stack.pop())
        
    print(output)
    operand_stack = []
    # evaluate the (now postfix) expression
    print("Evaling postfix {}".format(output))
    for token in output:
        print("Operand stack: {}".format(operand_stack))
        if token == '+' or token == '*':
            r = operand_stack.pop()
            l = operand_stack.pop()
            if token == '+':
                operand_stack.append(r+l)
            else:
                operand_stack.append(r*l)
        else:
            # operand
            operand_stack.append(token)
    print(operand_stack)   
    return operand_stack[0]
    

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
