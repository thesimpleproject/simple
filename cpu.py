import definitions as DEF

class TaskContext:

    def __init__(self):
        self._registers = [0]*16
        self._ip = 1024
        

class CPU:

    def __init__(self):
        self._contexts = []
        self._memory = [0]*(2**24)
        self._current_task = None
        
        self._dma_port = 0
        self._dma_addr = 0
        self._dma_len = 0

        for i in range(16):
            self._contexts.append(TaskContext())

        self.I26_MAX = (2**26)-1

        self._current_task = self._contexts[0]

        self._imap = {
            DEF.OPC_NOP : self.i_nop,
            DEF.OPC_ADD : self.i_add,
            DEF.OPC_SUB : self.i_sub,
            DEF.OPC_LDCA8: self.i_ldca8,
            DEF.OPC_LDCB8: self.i_ldcb8,
            DEF.OPC_DMAPORT: self.i_dmaport,
            DEF.OPC_INC : self.i_inc,
            DEF.OPC_DEC : self.i_dec,
        }

        print("cpu::__init__")

    def i_nop(self, d, s): pass

    def i_dmaport(self, d, s):
        self._dma_port = self._current_task.registers[d]

    def i_dmaaddr(self, d, s):
        self._dma_addr = self._current_task.registers[d]

    def i_dmalen(self, d, s):
        self._dma_len = self._current_task.registers[d]

    def i_dmawritesync(self, d, s):
        print("dma.write.sync")

    def i_add(self, d, s):
        self._current_task._registers[d] += self._current_task.registers[s]
        if(self._current_task.registers[d] > self.I26_MAX):
            self.err_interrupt(self.EINT_OVERFLOW)

    def i_sub(self, d, s):
        self._current_task._registers[d] -= self._current_task.registers[s]
        if(self._current_task.registers[d] < 0):
            self.err_interrupt(self.EINT_UNDERFLOW)

    def i_inc(self, d, s):
        self._current_task._registers[d] += 1
        if(self._current_task._registers[d] > self.I26_MAX):
            self.err_interrupt(self.EINT_OVERFLOW)

    def i_dec(self, d, s):
        self._current_task._registers[d] -= 1
        if(self._current_task._registers[d] < 0):
            self.err_interrupt(self.EINT_UNDERFLOW)

    def i_ldca8(self,d, s):
        self._current_task._registers[DEF.REG_A] = (d << 4) | s

    def i_ldcb8(self,d, s):
        self._current_task._registers[DEF.REG_B] = (d << 4) | s

    def run(self):
        while self._current_task._ip < len(self._memory):
            b0 = self._memory[self._current_task._ip]
            b1 = self._memory[self._current_task._ip+1]

            opc = b0
            dst = (b1 >> 4)
            src = (b1 & 0xF)

            self._imap[opc](dst, src)

            self._current_task._ip += 2
            
            continue


if __name__ == "__main__":
    cpu = CPU()
    cpu._memory[1024] = DEF.OPC_LDCA8
    cpu._memory[1025] = 0x20
    cpu._memory[1026] = DEF.OPC_LDCB8
    cpu._memory[1027] = 0x77
    cpu.run()
    print(cpu._current_task._registers)
