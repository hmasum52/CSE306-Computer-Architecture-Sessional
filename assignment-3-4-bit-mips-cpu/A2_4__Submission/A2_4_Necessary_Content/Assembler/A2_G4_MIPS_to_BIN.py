import re
import pprint

serial = {'A': 'add', 'B': 'addi', 'C': 'sub', 'D': 'subi', 'E': 'and', 'F': 'andi', 'G': 'or', 'H': 'ori', 'I': 'sll', 'J': 'srl', 'K': 'nor', 'L': 'lw', 'M': 'sw', 'N': 'beq', 'O': 'bneq', 'P': 'j'}

sequence = 'EIBHGMCDNFPKOLAJ'
instruction = {}

for i in range(len(sequence)):
    instruction[serial[sequence[i]]] = bin(i)[2:].zfill(4)

registers = {'$zero': '0000', '$t0': '0111', '$t1': '0001', '$t2': '0010', '$t3': '0011', '$t4': '0100', '$sp': '0110'}

R_TYPE = ['add', 'sub', 'and', 'or', 'nor']
S_TYPE = ['sll', 'srl']
I_TYPE = ['addi', 'subi', 'andi', 'ori', 'beq', 'bneq', 'lw', 'sw']
J_TYPE = ['j']

ALU_OP = {'add': '000', 'sub': '001', 'and': '010', 'or': '011', 'nor': '100', 'sll': '101', 'srl': '110'}

# reg_dst (0: 4-7 | 1 : 0-3)
REG_DST_4_7 = '0'
REG_DST_0_3 = '1' 
# alu_src (0: $2 | 1 : 0-3)
ALU_SRC_REG = '0'
ALU_SRC_INST = '1'
# mem_to_reg (0: ALU Result | 1 : Memory Result)
MEM_TO_REG_ALU_RESULT = '0'
MEM_TO_REG_MEM_RESULT = '1'
# reg_write (1 : Write to Register)
# mem_read (1 : Read from Memory)
# mem_write (1 : Write to Memory)
# branch (1 : Branch)
# branch_neq (1 : Branch not equal)
# jump (1 : Jump)
# alu_op (0: add | 1: sub | 2: and | 3: or | 4: nor | 5: sll | 6: srl)
def generate_control_rom_row(reg_dst, alu_src, mem_to_reg, reg_write, mem_read, mem_write, branch, branch_neq, jump, alu_op):
    return hex(int(reg_dst + alu_src + mem_to_reg + reg_write + mem_read + mem_write + branch + branch_neq + jump + alu_op, 2))[2:].zfill(3)

label_counter = 0;
def newLabel():
    current_label = label_counter;
    label_counter += 1;
    return "L" + current_label;

def generate_control_rom():
    print('Control ROM:')
    print('\t', end='')
    for i in range(len(sequence)):
        if serial[sequence[i]] in R_TYPE: # Register Only
            print(generate_control_rom_row(REG_DST_0_3, ALU_SRC_REG, MEM_TO_REG_ALU_RESULT, '1', '0', '0', '0', '0', '0', ALU_OP[serial[sequence[i]]]), end=' ')
        elif serial[sequence[i]] in S_TYPE: # Shift
            print(generate_control_rom_row(REG_DST_4_7, ALU_SRC_INST, MEM_TO_REG_ALU_RESULT, '1', '0', '0', '0', '0', '0', ALU_OP[serial[sequence[i]]]), end=' ')
        elif serial[sequence[i]] in I_TYPE[:4]: # immediate
            print(generate_control_rom_row(REG_DST_4_7, ALU_SRC_INST, MEM_TO_REG_ALU_RESULT, '1', '0', '0', '0', '0', '0', ALU_OP[serial[sequence[i]][:-1]]), end=' ')
        elif serial[sequence[i]] in I_TYPE[4:6]: # Branch
            is_beq = ('1', '0') if serial[sequence[i]] == 'beq' else ('0', '1')
            print(generate_control_rom_row(REG_DST_4_7, ALU_SRC_REG, MEM_TO_REG_ALU_RESULT, '0', '0', '0', is_beq[0], is_beq[1], '0', ALU_OP['sub']), end=' ')
        elif serial[sequence[i]] in I_TYPE[6:8]: # Memory
            if serial[sequence[i]] == 'sw':
                print(generate_control_rom_row(REG_DST_4_7, ALU_SRC_INST, MEM_TO_REG_MEM_RESULT, '0', '0', '1', '0', '0', '0', ALU_OP['add']), end=' ')
            else:
                print(generate_control_rom_row(REG_DST_4_7, ALU_SRC_INST, MEM_TO_REG_MEM_RESULT, '1', '1', '0', '0', '0', '0', ALU_OP['add']), end=' ')
        elif serial[sequence[i]] in J_TYPE: # Jump
            print(generate_control_rom_row(REG_DST_4_7, ALU_SRC_REG, MEM_TO_REG_ALU_RESULT, '0', '0', '0', '0', '0', '1', ALU_OP['add']), end=' ')
    print()

line_no = 1
labels = {}

def generate_label_location(lines):
    changed_lines = []
    for line in lines:
        parts = [part.strip() for part in line.split(':')]

        if len(parts) == 2:                         # case label
            labels[parts[0]] = len(changed_lines)
            if parts[1] != '':                      # code without label
                changed_lines.append(parts[1])
        else:                                       # not a label
            changed_lines.append(line)
    return changed_lines

def change(line_no, opcode, *args):
    bin_instruction = instruction[opcode]
    
    # add $t0, $t1, $t2 : Opcode SrcReg1($t1) SrcReg2($t2) DstReg($t0)
    if opcode in R_TYPE: # R-Type
        bin_instruction += registers[args[1]] # source 1
        bin_instruction += registers[args[2]] # source 2
        bin_instruction += registers[args[0]] # destination register
    
    # sll $t0, $t1, 1 : Opcode SrcReg1($t1) DstReg($t0) unsigned-int
    elif opcode in S_TYPE: # S-Type
        bin_instruction += registers[args[1]] # source register
        bin_instruction += registers[args[0]] # destination register
        bin_instruction += bin(int(args[2]))[2:].zfill(4) # shift amount
    
    # addi $t0, $t1, 1 : Opcode SrcReg1($t1) DstReg($t0) signed-int
    # beq $t0, $t1, 1 : Opcode SrcReg1($t1) SrcReg2($t0) signed-int     | if ($t1 - $t0 == 0) then goto 1
    # sw $t0, 1($t1) : Opcode SrcReg1($t1) SrcReg2($t0) signed-int      | $t0 = $t1 + 1
    # lw $t0, 1($t1) : Opcode SrcReg1($t1) DstReg($t0) signed-int       | *($t1+1) = $t0
    elif opcode in I_TYPE: # I-Type
        # addi $t0, $t1, 1          | immediate position @ 3
        if opcode in I_TYPE[:6]:
            bin_instruction += registers[args[1]] # source register
            if opcode in I_TYPE[:4]: # Immediate Operations
                immediate = int(args[2])
            else: # Branch Operations
                immediate = labels[args[2]] - ( line_no + 1 ) # PC auto-increments
        # sw $t0, 1($t1)            | immediate position @ 2
        else:
            bin_instruction += registers[args[2]]
            immediate = int(args[1])
            
        bin_instruction += registers[args[0]] # destination register
        
        if immediate < 0:   # negative immediate : signed int case handle
            immediate = 2**4 + immediate
        bin_instruction += bin(immediate)[2:].zfill(4) # immediate value / address
    
    # j 1 : Opcode address (unsigned-int)
    elif opcode in J_TYPE: # J-Type
        label_line = labels[args[0]]
        bin_instruction += bin(label_line)[2:].zfill(8) # target jump address
        bin_instruction += '0000'
    
    return bin_instruction


split_pattern = r'[ \t,\(\)]+'

def split(line):
    return re.split(split_pattern, line)

STACK_POINTER_ENABLED = True

if __name__ == '__main__':
    print('Instructions OPCODE:')
    pprint.pprint(instruction)
    print()

    generate_control_rom()
    print()

    with open('input.asm', 'r') as file:
        lines = [line.split(r'//')[0].strip() for line in file]                 # Trim Whitespaces
        lines = list(filter(lambda line : line != '', lines))   # Without Empty Lines
    
    if STACK_POINTER_ENABLED:
        push_pop_re = r'(push|pop)[ ]+(\$t[0-4])'
        original_lines = lines
        lines = ['addi $sp, $zero, 15']                         # SP initalization
        for line in original_lines:
            matched = re.search(push_pop_re, line)
            if matched is None:
                lines.append(line)
            else:
                if matched.group(1) == 'push':
                    lines.append(f'sw {matched.group(2)}, 0($sp)')        # store data in the stack top
                    lines.append('subi $sp, $sp, 1')              # allocate one variable to stack pointer
                else:
                    lines.append('addi $sp, $sp, 1')              # deallocate one variable from stack pointer
                    lines.append(f'lw {matched.group(2)}, 0($sp)')        # load data from the stack top
    
    lines = generate_label_location(lines)                      # Label Location Generated

    print('ASM Lines:')
    pprint.pprint(lines)
    
    bin_lines = []
    hex_lines = []

    for i in range(len(lines)):
        bin_line = change(i, *split(lines[i]))
        bin_lines.append(bin_line)
        hex_lines.append(hex(int(bin_line, 2))[2:].zfill(4)+'\n')

    with open('output.bin', 'w') as bin_file:
        for i in range(len(lines)):
            bin_file.write(' '.join([bin_lines[i][j:j+4] for j in range(0, len(bin_lines[i]), 4)]) + ' : ' + lines[i] + '\n')
    
    with open('output.hex', 'w') as hex_file:
        hex_file.writelines(hex_lines)