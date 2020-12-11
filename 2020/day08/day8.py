#!/usr/bin/env python

import re

class processor:
    visited = []
    program = None
    halted = False
    def __init__(self, program_file):
        self.pc = 0
        self.acc = 0
        with open(program_file) as fd:
            self.program = fd.readlines()
        self.visited = [0]*len(self.program)

    def printstate(self):
        print(32*"#")
        print("CPU STATE")
        print("PC:  {}".format(self.pc))
        print("ACC: {}".format(self.acc))

    def execute(self):
        while self.visited[self.pc] == 0:
            match = re.match('(\w+)\s+([+-]\d+)', self.program[self.pc])
            if not match:
                raise ValueError("Invalid opcode/operand format for {}".format(self.program[self.pc]))
            opcode = match.group(1)
            value = int(match.group(2))
            # nop
            # print("Executing {}".format(self.program[self.pc].strip()))
            self.visited[self.pc] += 1
            if opcode == 'nop':
                self.pc += 1
            if opcode == 'acc':
                self.acc += value
                self.pc += 1
            if opcode == 'jmp':
                self.pc += value
            # self.printstate()
            if self.pc < 0 or self.pc >= len(self.program):
                print("PROGRAM HALTED: PC: {}".format(self.pc))
                self.printstate()
                self.halted = True
                break
        if self.pc < 0 or self.pc >= len(self.program):
            print("PROGRAM HALTED: PC: {}".format(self.pc))
            self.printstate()
            self.halted = True
            return
        if self.visited[self.pc] == 1:
            self.printstate()
            print("Program infinite looped here.")


    def reset(self):
        #print(32*"#")
        #print("RESETTING PC...")
        self.pc = 0
        self.acc = 0
        self.visited = [0]*len(self.program)
        #self.printstate()




def main():
    cpu = processor('input.txt')
    originalprogram = cpu.program[:]
    mod_instr = 0
    #cpu.printstate()
    print("No modified code:")
    cpu.execute()
    while not cpu.halted:
        print(64*"#")
        print("Trying something new... - index {}".format(mod_instr))
        cpu.reset()
        cpu.program = originalprogram[:]
        # replace jmp with nop and nop with jmp
        if 'jmp' in cpu.program[mod_instr]:
            print("Old instr: {}".format(cpu.program[mod_instr]))
            print("Replacing jmp with nop")
            cpu.program[mod_instr] = cpu.program[mod_instr].replace('jmp', 'nop')
        elif 'nop' in cpu.program[mod_instr]:
            print("Old instr: {}".format(cpu.program[mod_instr]))
            print("Replacing nop with jump")
            cpu.program[mod_instr] = cpu.program[mod_instr].replace('nop', 'jmp')
        else:
            # not jmp or nop
            mod_instr += 1 
            continue
        print("New instr: {}".format(cpu.program[mod_instr]))
        cpu.execute()
        mod_instr += 1 

if __name__ == '__main__':
    main()
