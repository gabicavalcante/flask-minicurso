class Complex(object):
    def __init__(self, real, imag):
        self._real = real
        self._imag = imag

    def getReal(self):
        return self._real

    def setReal(self, valor):
        self._real = valor

    real = property(
        fget=getReal,
        fset=setReal)

    def getImag(self):
        return self._imag

    def setImag(self, valor):
        self._imag = valor

    imag = property(
        fget=getImag,
        fset=setImag)

    @staticmethod
    def main(*argv):
        "Programa para o tesste do Complex"
        c = Complex(0, 0)
        print c
        c.real = 1
        c.real = 2
        print c   
        return 0


c = Complex(1,0)
d = Complex(2,0)
e = Complex(3,0)

print(c._real)
print(d._real)
print(e._real)

c.setReal(2)
print c.getReal()

c.imag = 2
print c.imag

# Complex.setImag(c, 2)
# print Complex.getImag(c)

