import re
#Some Global Variables
PC = 0x00000000
program_memory_limit = 0x000000FF
data_memory_limit = [0x00010000,0x0001007F]
sp = 0x0000017F
d= {
    "zero": "x0",
    "ra": "x1",
    "sp": "x2",
    "gp": "x3",
    "tp": "x4",
    "t0": "x5",
    "t1": "x6",
    "t2": "x7",
    "s0": "x8",
    "fp": "x8",
    "s1": "x9",
    "a0": "x10",
    "a1": "x11",
    "a2": "x12",
    "a3": "x13",
    "a4": "x14",
    "a5": "x15",
    "a6": "x16",
    "a7": "x17",
    "s2": "x18",
    "s3": "x19",
    "s4": "x20",
    "s5": "x21",
    "s6": "x22",
    "s7": "x23",
    "s8": "x24",
    "s9": "x25",
    "s10": "x26",
    "s11": "x27",
    "t3": "x28",
    "t4": "x29",
    "t5": "x30",
    "t6": "x31"
}
Registers = d
Labels = {}

def halt_valid():
    pass    #returns boolean

#instruction_functions

def RTYPE(instruction):
    inst1=instruction.split()   #split on the basis of space 
    islabel=False
    if(instruction.count(",")!=2):     #check whether no of comma is correct or not
        return False
    tokens = re.split(r"[ ,:]+",instruction)
    if (tokens[0] in Labels.keys()):                    #check whether there is a label or not
        instr=tokens[1]
        rd=tokens[2]
        rs1=tokens[3]
        rs2=tokens[4]
        islabel=True
        splits=instruction.split(":")
        instruction=splits[1]
        instruction=instruction.strip()
    else:
        instr=tokens[0]
        rd=tokens[1]
        rs1=tokens[2]
        rs2=tokens[3]
    if(islabel):                      #if label then the checking valididty of code is different
        if(len(tokens)!=5):
            return False
        if(len(inst1)!=3):
            return False
        comma_check=instruction
        comma_check=comma_check.replace(" ","")
        comma_check=comma_check.replace(",",", ")
        comma_check=comma_check.split()
        for i in comma_check[:-2]:
            if("," not in i):
                return False
    else:
        if(len(tokens)!=4):             #without label checking criteria
            return False
        if(len(inst1)!=2):
            return False
        comma_check=instruction
        comma_check=comma_check.replace(" ","")      #comma postioning check
        comma_check=comma_check.replace(",",", ")
        comma_check=comma_check.split()
        for i in comma_check[:-2]:
            if("," not in i):
                return False
    opcode="0110011"
    result=[]
    isfound=False
    is_register1_valid=False
    is_register2_valid=False
    is_register3_valid=False
    Semantics={                                      #dict of semantics of different instruction func7 and func3 value
        "add":["0000000","000"],
        "sub":["0100000","000"],
        "sll":["0000000","001"],
        "slt":["0000000","010"],
        "sltu":["0000000","011"],
        "xor":["0000000","100"],
        "srl":["0000000","101"],
        "or":["0000000","110"],
        "and":["0000000","111"],
    }
    for reg in Registers.keys():              #find the register values
        if(rs1==reg):
            rs1=Registers[reg]
            is_register1_valid=True       
        if(rs2==reg):
            rs2=Registers[reg]
            is_register2_valid=True
        if(rd==reg):
            rd=Registers[reg]
            is_register3_valid=True
    if rs1[0]=="x":
        rs1=rs1[1:]
        is_register1_valid=True
    if rs2[0]=="x":
        rs2=rs2[1:]
        is_register2_valid=True
    if rd[0]=="x":
        rd=rd[1:]
        is_register3_valid=True
    if (not(is_register1_valid and is_register2_valid and is_register3_valid)):            #if any of the register is not valid then it will throw an error to main func
          return False
    rs1=bin(int(rs1))[2:].zfill(5)
    rs2=bin(int(rs2))[2:].zfill(5)
    rd=bin(int(rd))[2:].zfill(5)
    for intr in Semantics.keys():             #find the appropriate value according to func7 and func3 
        if(instr.lower()==intr.lower()):
            func7=Semantics[intr][0]
            func3=Semantics[intr][1]
            isfound=True
            break
    if(isfound):                           #find the full 32 bit machine code
        result.append(func7)        
        result.append(rs2)
        result.append(rs1)
        result.append(func3)
        result.append(rd)
        result.append(opcode)
        return "".join(result)
    else:
        return False

def ierror(s):
    x=s.split()
    if(len(x)!=2):
        return 1
    if(x[0] in ["addi","sltiu","jalr"]):
        x1=x[1].split(",")
        if(len(x1)!=3):
            return 1
        if((x1[0] not in d.values() and x1[0] not in d) or (x1[1] not in d.values() and x1[1] not in d)):
            return 1
        if((x1[2].lstrip("-")).isdecimal()):
            if(-(2**11)<=int(x1[2])<=(2**11)-1):
                pass
            else:
                return 1
        else:
            return 1
    else:
        if(x[1].count(",")!=1 or x[1].count("(")!=1 or x[1].count(")")!=1):
            return 1
            
        if(x[1].endswith(")")):
            pass
        else:
            return 1
        x1=re.split(",|\(|\)",x[1])
        if(len(x1)!=4):
            return 1
        if((x1[0] not in d.values() and x1[0] not in d) or (x1[2] not in d.values() and x1[2] not in d)):
            return 1
        if((x1[1].lstrip("-")).isdecimal()):
            if(-(2**11)<=int(x1[1])<=(2**11)-1):
                pass
            else:
                return 1
        else:
            return 1
    return 0





def uerror(s):
    x=s.split()
    if(len(x)!=2):
        return 1
    x1=x[1].split(",")
    if(len(x1)!=2):
        return 1
    if(x1[0] not in d.values() and x1[0] not in d):
        return 1
    if((x1[1].lstrip("-")).isdecimal()):
        if(-(2**19)<=int(x1[1])<=(2**19)-1):
            pass
        else:
            return 1
    else:
        return 1
    return 0

def itype(s):
    flag=ierror(s)
    if(flag==1):
        return 0
    x=s.split()
    if(x[0] in ["addi","sltiu","jalr"]):
       x1=x[1].split(",")
       imm=f"{int(x1[2]) & 0xFFF:012b}"
       if(x1[0][0]=='x'):
           rd=x1[0].lstrip("x")
       else:
           rd=d[x1[0]].lstrip("x")
       rd=int(rd)
       rd=f"{rd & 0xFFF:05b}"
       if(x1[1][0]=='x'):
           rs=x1[1].lstrip("x")
       else:
           rs=d[x1[1]].lstrip("x")
       rs=int(rs)
       rs=f"{rs & 0xFFF:05b}"
       if(x[0]=="addi"):
           func3="000"
       else:
           func3="011"
       return imm+rs+func3+rd+"0010011"
    else:
        x1=re.split(",|\(|\)",x[1])
        imm=f"{int(x1[1]) & 0xFFF:012b}"
        if(x1[0][0]=='x'):
            rd=x1[0].lstrip("x")
        else:
            rd=d[x1[0]].lstrip("x")
        rd=int(rd)
        rd=f"{rd & 0xFFF:05b}"
        if(x1[2][0]=='x'):
            rs=x1[2].lstrip("x")
        else:
            rs=d[x1[2]].lstrip("x")
        rs=int(rs)
        rs=f"{rs & 0xFFF:05b}"
        if(x[0]=="lw"):
            func3="010"
            opcode="0000011"
        else:
            func3="000"
            opcode="1100111"
        return imm+rs+func3+rd+opcode
    
def utype(s):
    flag=uerror(s)
    if(flag==1):
        return 0
    x=s.split()
    x1=x[1].split(",")
    imm=f"{int(x1[1]) & 0xFFFFF:020b}"
    if(x1[0][0]=='x'):
        rd=x1[0].lstrip("x")
    else:
        rd=d[x1[0]].lstrip("x")
    rd=int(rd)
    rd=f"{rd & 0xFFF:05b}"
    if(x[0]=="auipc"):
        opcode="0010111"
    else:
        opcode="0110111"
    return imm+rd+opcode

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

    imm_int = label_location - PC
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
    while len(data)<5:
        data="0"+data
    
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
    while len(src)<5:
        src="0"+src

    bin_instr = imm_bin[-12:-5]+data+src+funct3+imm_bin[-5:-1]+imm_bin[-1]+opcode
    return bin_instr

#main body starts

def check_B_type_validity(line):
    mnemonics = {"beq","bne","blt","bge","bltu","bgeu"}
    line=line.replace(","," , ")
    parts = line.split()

    if len(parts) != 6:
        return False

    mnemonic = parts[0]
    rs1 = parts[1]
    rs2 = parts[3]
    labels = parts[5]

    if parts[2]!=',' or parts[4]!=',':
        return False

    if mnemonic not in mnemonics:
        return False

    if rs1 not in d or rs2 not in d:
        return False
    
    if labels not in Labels:
        return False
    return True

def B_type(instructions,PC_address,label_address):
    B_instructions={
        "beq":  "000",
        "bne":  "001",
        "blt":  "100",
        "bge":  "101",
        "bltu": "110",
        "bgeu": "111"
    }
    if check_B_type_validity(instructions)==False:
        return False
    instructions=instructions.replace(',',' , ')
    instruction=instructions.split()[0]
    rs1=instructions.split()[1]
    rs2=instructions.split()[3]

    registers = {
        f"x{i}": i for i in range(32)
    }


    rs1=d[rs1]
    rs2=d[rs2]
    


    B_opcode="1100011"

    def find_Immediate(PC_address,label_address):
        return label_address-PC_address
    
    immediate=find_Immediate(PC_address,label_address)

    
    def decode_B_type(instruction,rs1,rs2,immediate):
        if instruction not in B_instructions:
            return False
        
        if rs1 not in registers or rs2 not in registers:
            return False

        if immediate < -4096 or immediate > 4094:
            return False
        
        immediate=immediate>>1
        rs1_bin=format(registers[rs1],"05b")
        rs2_bin=format(registers[rs2],"05b")
        imm_bin=format(immediate & 0x1FFF,"013b")

        imm_12=imm_bin[0]
        imm_10_5=imm_bin[1:7]
        imm_4_1=imm_bin[7:11]
        imm_11=imm_bin[11]

        func3=B_instructions[instruction]

        bin_inst=imm_12 + imm_10_5 + rs1_bin + rs2_bin + func3 + imm_4_1 + imm_11 + B_opcode
        
        return bin_inst

    Decoded_instruction=decode_B_type(instruction,rs1,rs2,immediate)
    return Decoded_instruction
