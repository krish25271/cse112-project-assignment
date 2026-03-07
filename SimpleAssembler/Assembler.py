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
