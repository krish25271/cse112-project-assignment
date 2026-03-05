PC = 0x00000000
program_memory_limit = 0x000000FF
data_memory_limit = [0x00010000,0x0001007F]
sp = 0x0000017F
Labels = {}
Registers={
        "zero":"x0",
        "ra":"x1",
        "sp":"x2",
        "gp":"x3",
        "tp":"x4",
        "t0":"x5",
        "t1":"x6",
        "t2":"x7",
        "s0":"x8",
        "fp":"x8",
        "s1":"x9",
        "a0":"x10",
        "a1":"x11",
        "a2":"x12",
        "a3":"x13",
        "a4":"x14",
        "a5":"x15",
        "a6":"x16",
        "a7":"x17",
        "s2":"x18",
        "s3":"x19",
        "s4":"x20",
        "s5":"x21",
        "s6":"x22",
        "s7":"x23",
        "s8":"x24",
        "s9":"x25",
        "s10":"x26",
        "s11":"x27",
        "t3":"x28",
        "t4":"x29",
        "t5":"x30",
        "t6":"x31",
    }


def halt_valid():
    pass    #returns boolean

#instruction_functions

def Jtype(instr):
    opcode = '1101111'

    lst = instr.split()
    ra = ''
    
    #commas, space
    flag = True
    if (len(lst) != 2) or (lst[0] != "jal") or ("," not in lst[1]) or (len(lst[1].split(','))!=2 ):
        flag = False
    else:
        register, label = lst[1].split(",")
        if label not in Labels:
            flag = False
        else:
            label_location = Labels[label]
        if register not in Registers.keys():
            if register not in Registers.values():
                flag = False
            else: pass
        else:
            register = Registers[register]
                    
    if flag == False:
        return flag
    
    ra = int(register[1:])
    ra = str(bin(ra))[2:]
    while len(ra)<5:
        ra="0"+ra

    imm_int = label_location - PC;
    imm_str, imm_str_temp = '',''
    if imm_int < 0:
        imm_str_temp = str(bin(imm_int))[3:]
        while(len(imm_str_temp)<20):
            imm_str_temp = '1' + imm_str_temp
    else:
        imm_str_temp = str(bin(imm_int))[2:]
        while(len(imm_str_temp)<20):
            imm_str_temp = '0' + imm_str_temp
    
    imm_str = imm_str_temp[-20]+ imm_str_temp[-10:-1]+ imm_str_temp[-1]+ imm_str_temp[-11] + imm_str_temp[-19:-12] + imm_str_temp[-12]
    
    bin_instr = imm_str + ra +opcode
    return bin_instr

def Stype(instr):
    opcode = '0100011'
    funct3 = '010'

    lst = instr.split()
    data = ''
    src =''
    register, rest = '',''
    imm_str, imm_bin = '',''
    #commas, space
    flag = True
    if (len(lst) != 2) or (lst[0]!='sw') or ("," not in lst[1]) or (len(lst[1].split(','))!=2):
        flag = False
    else:  
        register, rest = lst[1].split(',')
        #Register_validity
        if register not in Registers.keys():
            if register not in Registers.values():
                flag = False
            else:
                register = Registers[register]

        #imm(src) validity
        if '(' not in rest or ')' not in rest:
            flag = False
        else:
            open, close = 0,0
            for a in range(len(rest)):
                if rest[a] == '(':
                    if a == 0:
                        flag = False
                    open = a
                if rest[a] == ')':
                    close = a
            if open>close:
                flag = False
            else:
                imm_str = rest[0:open]
                src = rest[open+1:close]
                if src not in Registers.keys():
                    if src not in Registers.values():
                        flag = False
                else:
                    src = Registers[src]

    if flag == False:
        return flag
    
    data = int(register[1:])
    data = str(bin(data))[2:]
    imm_bin = int(imm_str)
    if imm_bin < 0:
        imm_bin = str(bin(imm_bin))[3:]
        while(len(imm_bin)<12):
            imm_bin = '1' + imm_bin
    else:
        imm_bin = str(bin(imm_bin))[2:]
        while(len(imm_bin)<12):
            imm_bin = '0' + imm_bin
    
    src = int(src[1:])
    src = str(bin(src))[2:]

    bin_instr = imm_bin[-12:-5]+data+src+funct3+imm_bin[-5:-1]+imm_bin[-1]+opcode
    return bin_instr
#main body starts