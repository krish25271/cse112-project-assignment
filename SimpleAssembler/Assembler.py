import re
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
    opcode = '1101111'      #opcode for j-type instr

    lst = instr.split()     #components of instr
    ra = ''
    register,label = '',''
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
            register = Registers[register]      #ABI convention is changed to x{i}
                    
    if flag == False:       #if any error occurs, flag is False
        return flag
    
    ra = int(register[1:])          #{i} of x{i} changed to binary
    ra = str(bin(ra))[2:]
    while len(ra)<5:                #extend to 5bits
        ra="0"+ra

    imm_int = label_location - PC           #Immediate Calc
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
    
    imm_bin = int(imm_str)
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