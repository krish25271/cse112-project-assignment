
Register_main={
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


def B_type(instruction,rs1,rs2,PC_address,label_address):
    B_instructions={
        "beq":  "000",
        "bne":  "001",
        "blt":  "100",
        "bge":  "101",
        "bltu": "110",
        "bgeu": "111"
    }
    registers = {
        f"x{i}": i for i in range(32)
    }


    rs1=Register_main[rs1]
    rs2=Register_main[rs2]
    


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




    

    
    