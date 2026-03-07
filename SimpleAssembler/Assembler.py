import re
import sys
#Some Global Variables
PC = 0x00000000
Label_validity = {}  #key->Label-address;value->True/False
write_lst = []       #binary-encoding-lst (with errors)
Labels = {}          #key->Label-name;value->Label-address
program_memory_limit = 0x000000FF
data_memory_limit = [0x00010000,0x0001007F]
sp = 0x0000017F
#Registers: key->ABI,value->x{i}
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


def Striper(instruction):
    instruction=instruction.strip()     
    instruction=instruction.replace(", ",",")   #remove the white spaces after comma
    instruction=instruction.replace(" ,",",")   #remove the white spaces before comma
    return instruction

def immediate(imm):
    flag = True
    if ("0x" in imm or "0b" in imm) and (imm[2:].isdigit() or (imm[0]== '-' and imm[3:].isdigit())):
        imm_int = int(imm,0)
    elif imm[0] == "-" and imm[1:].isdigit():
        imm_int = int(imm)
    elif imm.isdigit():
        imm_int = int(imm)
    else:
        flag = False
    if flag == True:
        return (flag,imm_int)
    else:
        return (flag,0)

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


#to check errors in I type instruction (return 1 if error and 0 otherwise)
def ierror(s):
    x=s.split()    #splitting instruction on space
    if(len(x)!=2):      #to check if there is just 1 space
        return 1
    if(x[0] in ["addi","sltiu","jalr"]):   
        x1=x[1].split(",")
        if(len(x1)!=3):               #to check if there are 2 commas
            return 1
        if((x1[0] not in d.values() and x1[0] not in d) or (x1[1] not in d.values() and x1[1] not in d)):    #to check if register names are valid names
            return 1
        if((x1[2].lstrip("-")).isdecimal()):                    
            if(-(2**11)<=int(x1[2])<=(2**11)-1):        #to check if immediate is of 12 bits
                pass
            else:
                return 1
        else:
            return 1
    else:
        if(x[1].count(",")!=1 or x[1].count("(")!=1 or x[1].count(")")!=1):  #to check if there are 1 each of ')','(' and ',' in lw instruction
            return 1
            
        if(x[1].endswith(")")):                                             #to check if the instruction ends with')'
            pass
        else:
            return 1
        x1 = re.split(r"[(),]", x[1])                                         #splitting instruction on '(',')' and ','
        if(len(x1)!=4):                                                     #checking if it splits in 4 parts
            return 1
        if((x1[0] not in d.values() and x1[0] not in d) or (x1[2] not in d.values() and x1[2] not in d)):  #to check if register names are valid names
            return 1
        if((x1[1].lstrip("-")).isdecimal()):
            if(-(2**11)<=int(x1[1])<=(2**11)-1):                      #to check if immediate is of 12 bits
                pass
            else:
                return 1
        else:
            return 1
    return 0

#to check erros in U type instructions (returns 1 if error and 0 otherwise)
def uerror(s):
    x=s.split()       #splitting instruction on space
    if(len(x)!=2):    #to check if there is just 1 space
        return 1
    x1=x[1].split(",")    # splitting instruction on comma
    if(len(x1)!=2):       #to check if there is 1 comma
        return 1
    if(x1[0] not in d.values() and x1[0] not in d):    #to check if register names are valid names
        return 1
    if((x1[1].lstrip("-")).isdecimal()):
        if(-(2**19)<=int(x1[1])<=(2**19)-1):      #to check if immediate is of 20 bits
            pass
        else:
            return 1
    else:
        return 1
    return 0

def itype(s):
    flag=ierror(s)       #to check for errors in I type instructions
    if(flag==1):
        return 0
    x=s.split()                 # splitting on space
    if(x[0] in ["addi","sltiu","jalr"]):
       x1=x[1].split(",")                 #splitting on commas
       imm=f"{int(x1[2]) & 0xFFF:012b}"    #to convert immediate in 12 bits binary
       if(x1[0][0]=='x'):                    #to check if the naming of rd register is ABI naming or not
           rd=x1[0].lstrip("x")
       else:
           rd=d[x1[0]].lstrip("x")
       rd=int(rd)
       rd=f"{rd & 0xFFF:05b}"                 #converting rd to its corresponding binary number representation
       if(x1[1][0]=='x'):                     #to check if the naming of rs register is ABI naming or not
           rs=x1[1].lstrip("x")
       else:
           rs=d[x1[1]].lstrip("x")
       rs=int(rs)
       rs=f"{rs & 0xFFF:05b}"            #converting rs to its corresponding binary number representation
       if(x[0]=="addi"):                 # to find func3 and opcode   
           func3="000"
           opcode="0010011"
       elif(x[0]=="sltiu"):
           func3="011"
           opcode="0010011"
       else:
            func3="000"
            opcode="1100111"
       return imm+rs+func3+rd+opcode
    else:
        x1 = re.split(r"[(),]", x[1])       #splitting on "," ,")","("
        imm=f"{int(x1[1]) & 0xFFF:012b}"    #to convert immediate in 12 bits binary
        if(x1[0][0]=='x'):                   #to check if the naming of rd register is ABI naming or not
            rd=x1[0].lstrip("x") 
        else:
            rd=d[x1[0]].lstrip("x")
        rd=int(rd)                         
        rd=f"{rd & 0xFFF:05b}"                #converting rd to its corresponding binary number representation
        if(x1[2][0]=='x'):                     #to check if the naming of rs register is ABI naming or not
            rs=x1[2].lstrip("x")
        else:
            rs=d[x1[2]].lstrip("x")
        rs=int(rs)
        rs=f"{rs & 0xFFF:05b}"                 #converting rs to its corresponding binary number representation
        return imm+rs+"010"+rd+"0000011"
    
def utype(s):
    flag=uerror(s)        #to check for errors
    if(flag==1):
        return 0
    x=s.split()         #splitting on space
    x1=x[1].split(",")           #splitting on commas
    imm=f"{int(x1[1]) & 0xFFFFF:020b}"     #converting immediate to 20 bits binary
    if(x1[0][0]=='x'):                     #to check if the naming of rd register is ABI naming or not
        rd=x1[0].lstrip("x")
    else:
        rd=d[x1[0]].lstrip("x")
    rd=int(rd)
    rd=f"{rd & 0xFFF:05b}"                #converting rd to its corresponding binary number representation
    if(x[0]=="auipc"):                    # to find opcode
        opcode="0010111"
    else:
        opcode="0110111"
    return imm+rd+opcode

def Jtype(instr):
    opcode = '1101111'      #opcode for j-type instr

    lst = instr.split()     #components of instr
    ra = ''
    register,label = '',''
    imm_int = 0
    imm_valid = False
    #commas, space
    flag = True
    if (len(lst) != 2) or (lst[0] != "jal") or ("," not in lst[1]) or (len(lst[1].split(','))!=2 ):
        flag = False
    else:
        register, label = lst[1].split(",")
        imm_valid, imm_int = immediate(label)
        if label not in Labels and (not imm_valid):
            flag = False
        elif label in Labels:
            label_location = Labels[label]
        if register not in Registers.keys():
            if register not in Registers.values():
                flag = False
            else: pass
        else:
            register = Registers[register]      #ABI convention is changed to x{i}
                    
    if flag == False:       #if any error occurs, flag is False
        return flag
    
    ra = int(register[1:])          #{i} of x{i} changed to binary
    ra = str(bin(ra))[2:]
    while len(ra)<5:                #extend to 5bits
        ra="0"+ra
    if imm_valid == False:                #imm is not directly present
        imm_int = label_location - PC           #Immediate Calc from PC

    if(-(2**19)<=imm_int<=(2**19)-1):      #to check if immediate is of 20 bits
        pass
    else:
        return False
    
    imm_str, imm_str_temp = '',''
    #Sign extension of imm-int into binary of 20 bits
    if imm_int < 0:
        imm_str_temp = str(bin(imm_int))[3:]
        while(len(imm_str_temp)<20):
            imm_str_temp = '1' + imm_str_temp
    else:
        imm_str_temp = str(bin(imm_int))[2:]
        while(len(imm_str_temp)<20):
            imm_str_temp = '0' + imm_str_temp 
    
    #Format of immediate in j-type is imm-str
    imm_str = imm_str_temp[-20]+ imm_str_temp[-10:-1]+ imm_str_temp[-1]+ imm_str_temp[-11] + imm_str_temp[-19:-12] + imm_str_temp[-12]
    
    bin_instr = imm_str + ra + opcode
    return bin_instr

def Stype(instr):
    opcode = '0100011'      #opcode and funct3 values for s-type instr
    funct3 = '010'
    imm_valid = False
    imm_int = 0
    lst = instr.split()     #components of instr
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
            register = Registers[register]      #ABI changed to x{i}

        #imm(src) validity
        if '(' not in rest or ')' not in rest:      #Parenthesis must be closed
            flag = False
        else:
            open, close = 0,0       #open is index("("), close is index(")")
            for a in range(len(rest)):
                if rest[a] == '(':
                    if a == 0:
                        flag = False        #if open = 0, imm is not provided
                    open = a
                if rest[a] == ')':
                    close = a
            if open>close:          #invalid parenthesis
                flag = False
            else:
                imm_str = rest[0:open]
                imm_valid, imm_int = immediate(imm_str)
                if not imm_valid:
                    flag = False
                src = rest[open+1:close]
                if src not in Registers.keys():
                    if src not in Registers.values():
                        flag = False
                else:
                    src = Registers[src]        #ABI changed to x{i}

    if flag == False:
        return flag
    
    data = int(register[1:])
    data = str(bin(data))[2:]
    while len(data)<5:      #Bit extension to 5
        data="0"+data
    
    imm_bin = imm_int
    if(-(2**11)<=imm_bin<=(2**11)-1):      #to check if immediate is of 12 bits
        pass
    else:
        return False
    if imm_bin < 0:     #Sign extension of imm-bin to 12 bits
        imm_bin = str(bin(imm_bin))[3:]
        while(len(imm_bin)<12):
            imm_bin = '1' + imm_bin
    else:
        imm_bin = str(bin(imm_bin))[2:]
        while(len(imm_bin)<12):
            imm_bin = '0' + imm_bin
    
    src = int(src[1:])
    src = str(bin(src))[2:]
    while len(src)<5:       #Bit extension to 5
        src="0"+src

    #Instruction encoding
    bin_instr = imm_bin[-12:-5]+data+src+funct3+imm_bin[-5:-1]+imm_bin[-1]+opcode
    return bin_instr

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

    if parts[2]!=',' or parts[4]!=',':# comma position check
        return False

    if mnemonic not in mnemonics:# Valid instruction type check
        return False

    if rs1 not in d or rs2 not in d:# Valid register type check
        return False
    
    if (labels.isdigit()==False and labels not in Labels) and (labels[0]=='-' and labels[1:].isdigit()==False):# Valid Label check
        return False
    return True

def B_type(instructions,PC_address):
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
    instructions=instructions.replace(',',' , ')#instructions=[instruction,rs1,',',rs2,',',label]
    instruction=instructions.split()[0]
    rs1=instructions.split()[1]
    Label=instructions.split()[5]
    rs2=instructions.split()[3]

    registers = {
        f"x{i}": i for i in range(32)
    }


    rs1=d[rs1]
    rs2=d[rs2]
    


    B_opcode="1100011"

    def find_Immediate(PC_address,label_address):
        return label_address-PC_address
    if (Label[0]=='-' and Label[1:].isdigit()) or Label.isdigit():
        immediate=int(Label)
    else:
        label_address=Labels[Label]
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
        imm_bin=format(immediate & 0x1FFF,"013b")#sign extension of immediate

        imm_12=imm_bin[0]
        imm_10_5=imm_bin[2:8]
        imm_4_1=imm_bin[8:12]
        imm_11=imm_bin[1]

        func3=B_instructions[instruction]

        bin_inst=imm_12 + imm_10_5 + rs2_bin + rs1_bin + func3 + imm_4_1 + imm_11 + B_opcode# final instruction in binary
        
        return bin_inst

    Decoded_instruction=decode_B_type(instruction,rs1,rs2,immediate)
    return Decoded_instruction

def find_label():
    global lines
    temp1=PC
    for i in range(len(lines)):
        if ':' in lines[i]:
            temp = re.split(r"[:]+",lines[i])
            Labels[temp[0]] = temp1      #Label saved

            for j in range(len(lines[i])):      #j is index(':')
                if lines[i][j] == ":":
                    break
                
            if temp[0][0].isalpha() and lines[i][j-1] != ' ':   #if first letter is not alphabet or if there is " " bw label and ":",# label invalid
                Label_validity[temp1] = True
            else:
                Label_validity[temp1] = False
            lines[i] = lines[i][j+2:]       #instruction without labels
            lines[i] = lines[i].strip()     #remove white spaces
        temp1+=4


def identify_instruction(instruction):
    instruct=re.split(r"[ ,:]+",instruction)
    if (instruct[0] in Labels.keys()):
        instructs=instruct[1]                  #Find if instruction is label or not and choose appropriate instruction to check
    else:
        instructs=instruct[0]              #if it not label it directly take the starting index
    Instruction_types={"R":["add","sub","sll","slt","sltu","xor","srl","or","and"],
                       "I":["lw","addi","sltiu","jalr"],
                       "S":["sw"],                                              #dictionary of instruction
                       "B":["beq","bne","blt","bge","bltu","bgeu"],
                       "U":["lui","auipc"],
                       "J":["jal"]
                       }
    for i in Instruction_types:
        if instructs in Instruction_types[i]:                           #finding the appropriate function type
            return i
        
    return False

def MAIN():
    global PC
    assembly_file=sys.argv[1]
    machine_code_file=sys.argv[2]
    with open(assembly_file,"r") as f:
        global lines
        lines=f.readlines()
    find_label()
    f=open(machine_code_file,"w")
    num=0
    write_lst=[]
    #Virtual-Halt Error Checking and Program Memory Limit
    if len(lines)<=64:
        halt = B_type(Striper(lines[-1]))
        if halt == "00000000000000000000000001100011":
            pass
        else:
            print(f"Line->{len(lines)} SyntaxError PC->{PC+(4*len(lines))}")
            return
    else:
        print(f"Line->65 SyntaxError PC->{program_memory_limit}")
        return
    
    for instr in lines:
        if(instr==""):
            continue
        lines[num]=Striper(lines[num])     #remove extra spaces and new line characters
        type_of_inst=identify_instruction(lines[num])
        instr=instr.rstrip("\n")
        num=num+1
        if PC in Label_validity and Label_validity[PC] == False:        #Invalid label, break
            print(f"Line->{num} SyntaxError PC->{PC}")
            return
        if(type_of_inst)==False:
            print(f"Line->{num} SyntaxError PC->{PC}")
            return
        if(type_of_inst)=="R":
            binary=RTYPE(instr)
            if(binary)==False:
                print(f"Line->{num} SyntaxError PC->{PC}")
                return
            else:
                write_lst.append(f"{binary}\n")
        elif(type_of_inst)=="B":
            binary=B_type(instr,PC)
            if(binary)==False:
                print(f"Line->{num} SyntaxError PC->{PC}")
                return
            else:
                write_lst.append(f"{binary}\n")
        elif(type_of_inst)=="J":
            binary=Jtype(instr)
            if(binary)==False:
                print(f"Line->{num} SyntaxError PC->{PC}")
                return
            else:
                write_lst.append(f"{binary}\n")
        elif(type_of_inst)=="S":
            binary=Stype(instr)
            if(binary)==False:
                print(f"Line->{num} SyntaxError PC->{PC}")
                return
            else:
                write_lst.append(f"{binary}\n")
        elif(type_of_inst)=="I":
            binary=itype(instr)
            if(binary)==False:
                print(f"Line-> {num} SyntaxError PC->{PC}")
                return
            else:
                write_lst.append(f"{binary}\n")
        elif(type_of_inst)=="U":
            binary=utype(instr)
            if(binary)==False:
                print(f"Line->{num} SyntaxError PC->{PC}")
                return
            else:
                write_lst.append(f"{binary}\n")
        PC=PC+4
    f.writelines(write_lst)
    
MAIN()