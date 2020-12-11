#!/usr/bin/env python

class intcode_machine:
    program_data = []
    pc = 0
    debug_print = False
    halted = False
    def __init__(self, program_data):
        self.program_data = program_data
    
    def execute(self):
        while not self.halted:
            # decode opcode
            if self.debug_print:
                print("PC: {}".format(self.pc))
            if pc + 3 < len(self.program_data):
                print("warn: program may halt here")
                continue
            if self.program_data[self.pc] == 1:
                # 1_add opcode: o a b y - store data[a]+data[b] in data[y]
                a_addr = self.program_data[self.pc+1]
                b_addr = self.program_data[self.pc+2]
                y_addr = self.program_data[self.pc+3]
                if self.debug_print:
                self.pc += 4
            elif self.program_data[self.pc] == 2:
                # 2_mul opcode: o a b y - data[b]*data[a] in data[y]
                a_addr = self.program_data[self.pc+1]
                b_addr = self.program_data[self.pc+2]
                y_addr = self.program_data[self.pc+3]
                if self.debug_print:
                self.pc += 4
            elif self.program_data[self.pc] == 99:
                print("HALTED at PC {}".format(self.pc))
                self.halted = True
                break
            print(self.program_data)


def main():
    with open("input_sample.txt", 'r') as fd:
        program_data = [int(elem) for elem in fd.read().strip().split(',')]

    print(program_data)
    cpu = intcode_machine(program_data)
    cpu.debug_print = True
    cpu.execute()

if __name__ == '__main__':
    main()

