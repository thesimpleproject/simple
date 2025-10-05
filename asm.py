import io

class AssemblerState:

    def __init__(self):
        self._FILE_TO_READ = 'test.S'
        self._line_no = 0
        self._buffer = io.BytesIO()

    def save_buffer_to(self, fname):
        with open(fname, mode = 'wb') as ftw:
            ftw.write(self._buffer.getvalue())
            ftw.flush()

import definitions as DEF

class Assembler:

    def __init__(self):
        self._state = AssemblerState()
        self._labels = {}
        pass

    def save_file(self, fname):
        self._state.save_buffer_to(fname)
        return fname

    def process_decl(self, line):
        parts = line.split(' ', 1)
        parts[1] = parts[1].strip()

        if parts[0] == '.str':
            parts[1] = self.check_str(parts[1])
            self.emit_str(parts[1])

    def check_str(self, s):
        s = s[1:]
        s = s[:-1]
        return s

    def check_imm(self, imm):
        if imm.startswith('0x'):
            return int(imm[2:], 16)
        elif imm.startswith('@'):
            return self.reflabel(imm[1:])
        else:
            return int(imm, 10)

    def reflabel(self, name):
        if name in self._labels:
            return self._labels[name]

        return 0xDEADBEEF
            

    def process(self):
        with open(self._state._FILE_TO_READ) as ftr:
            for line in ftr:
                self._state._line_no += 1

                line = line.strip()
                
                if line.startswith(';'):
                    continue
                elif line.startswith('.'):
                    self.process_decl(line)
                    continue

                line = line.split(';', 1)
                line = line[0].split()

                if not len(line):
                    continue
                
                ins = line[0]

                if ins in DEF.NO_ARGS:
                    self.emit_no_arg(ins)
                elif ins in DEF.ONE_ARGS:
                    self.emit_one_args(ins, line[1])
                elif ins in DEF.TWO_ARGS:
                    self.emit_two_args(ins, line[1], line[2])
                elif ins in DEF.ONE_IMM_ARGS:
                    self.emit_one_imm_args(ins, self.check_imm(line[1]))

        return self._state._buffer.getvalue()

    def emit_str(self, s):
        self._state._buffer.write(s.encode())

    def emit_no_arg(self, i):
        self._state._buffer.write(DEF.NO_ARGS[i].to_bytes())
        self._state._buffer.write((0x00).to_bytes())

    def emit_one_args(self, i, d):
        self._state._buffer.write(DEF.ONE_ARGS[i].to_bytes())
        self._state._buffer.write((DEF.REGS[d] << 4).to_bytes())

    def emit_two_args(self, i, d, s):
        self._state._buffer.write(DEF.TWO_ARGS[i].to_bytes())
        self._state._buffer.write(((DEF.REGS[d] << 4) | DEF.REGS[s]).to_bytes())

    def emit_one_imm_args(self, i, d):
        self._state._buffer.write(DEF.ONE_IMM_ARGS[i].to_bytes())

        if DEF.IMM_SIZES[i] == 1:
            self._state._buffer.write(int(d).to_bytes())
        elif DEF.IMM_SIZES[i] == 4:
            self._state._buffer.write((0).to_bytes())
            b0 = (d >> 24) & 0xFF
            b1 = (d >> 16) & 0xFF
            b2 = (d >> 8) & 0xFF
            b3 = d & 0xFF
            self._state._buffer.write(b0.to_bytes())
            self._state._buffer.write(b1.to_bytes())
            self._state._buffer.write(b2.to_bytes())
            self._state._buffer.write(b3.to_bytes())
        else:
            raise Exception("Unknown imm size: %s!" % i)


if __name__ == "__main__":
    asm = Assembler()
    print(asm.process())
    asm.save_file("test.bin")
