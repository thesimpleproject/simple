class CharStream:

    def __init__(self, s):
        self._s = s
        self._i = 0
        self._next = None
        self._line_no = 1
        self._fname = "<str>"

    def read(self):
        if self._next != None:
            c = self._next
            self._next = None
            return c

        if self._i >= len(self._s):
            return None

        c = self._s[self._i]
        self._i += 1

        if c == '\n':
            self._lino_no += 1

        return c

    def read_until_whitespace(self):
        s = ""
        while True:
            c = self.read()
            if c == None:
                if s == "":
                    return None
                else:
                    return s

            if c == ' ' or c == '\n' or c == '\r' or c == '\t':
                return s
            print(s,"+=",c)
            s += c

    def putback(self, c):
        if self._next != None:
            raise Exception("Can't putback now!")

        self._next = c

    def lookahead(self):
        if self._next != None:
            return self._next

        if self._i >= len(self._s):
            return None

        return self._s[self._i]

class Parser:

    def __init__(self, cs):
        self._cs = cs

    def parse_expression(self):
        c = self._cs.read()
        l = self._cs.lookahead()
        self._cs.putback(c)

        if c in "+-/*":
            if c == '-':
                if l in '0123456789':
                    return self.parse_number()
            return self.parse_binop()
        elif c in "0123456789":
            return self.parse_number()

    def parse_binop(self):
        s = self._cs.read_until_whitespace()

        if s in "+-/*":
            left = self.parse_expression()
            right = self.parse_expression()
            return ('binop', s, (left, right), self._cs._line_no, self._cs._fname)
        else:
            raise Exception("Parser: Not a valid binop: %s!" % s)

    def parse_number(self):
        s = self._cs.read_until_whitespace()

        for c in s:
            if c < '0' or c > '9':
                if c != '.' and c != '-':
                    raise Exception("Parser: Not a valid number: %s!" % s)


        return ('int', int(s), self._cs._line_no, self._cs._fname)
