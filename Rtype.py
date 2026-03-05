def RTYPE(instr,rd,rs1,rs2):
    opcode="0110011"
    result=[]
    isfound=False
    is_register1_valid=False
    is_register2_valid=False
    is_register3_valid=False
    Semantics={
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
    for reg in Registers.keys():
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
    if (not(is_register1_valid and is_register2_valid and is_register3_valid)):
        print("Not valid registers")
        return
    rs1=bin(int(rs1))[2:].zfill(5)
    rs2=bin(int(rs2))[2:].zfill(5)
    rd=bin(int(rd))[2:].zfill(5)
    for intr in Semantics.keys():
        if(instr.lower()==intr.lower()):
            func7=Semantics[intr][0]
            func3=Semantics[intr][1]
            isfound=True
            break
    if(isfound):
        result.append(func7)
        result.append(rs2)
        result.append(rs1)
        result.append(func3)
        result.append(rd)
        result.append(opcode)
        print("".join(result))
    else:
        print("Instruction Not Found")
RTYPE("xor","x2","t2","zero")


