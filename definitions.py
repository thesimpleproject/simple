OPC_NOP = 0b00000000
OPC_ADD = 0b00000001
OPC_SUB = 0b00000010
OPC_INC = 0b00000110
OPC_DEC = 0b00000111

OPC_LDCA8 = 0b11101000
OPC_LDCB8 = 0b11101001

OPC_DMAPORT = 0b10000000
OPC_DMAADDR = 0b10000001
OPC_DMALEN = 0b10000010
OPC_DMAWRITESYNC = 0b10000011
OPC_JMP32 = 0b11111011

REG_A = 0x00
REG_B = 0x01
REG_C = 0x02

REGS = {
    "ra": REG_A,
    "rb": REG_B,
    "rc": REG_C,
}

NO_ARGS = {
        "nop": OPC_NOP,
        "dma.write.sync": OPC_DMAWRITESYNC
}

ONE_ARGS = {
    "inc": OPC_INC,
    "dec": OPC_DEC,
    "dma.port": OPC_DMAPORT,
    "dma.addr": OPC_DMAADDR,
    "dma.len": OPC_DMALEN,
}

ONE_IMM_ARGS = {
    "ldc.a.8": OPC_LDCA8,
    "ldc.b.8": OPC_LDCB8,
    "jmp.32": OPC_JMP32
}

IMM_SIZES = {
    "ldc.a.8": 1,
    "ldc.b.8": 1,
    "jmp.32": 4,
}

TWO_ARGS = {
    "add": OPC_ADD,
    "sub": OPC_SUB,
}
