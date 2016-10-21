class Pessoa(object):
    FEMALE = 0
    MALE = 1

    def __init__(self, nome, sexo):
        self._nome = nome
        self._sexo = sexo

    def __str__(self):
        return str(self._nome)


class Pais(Pessoa):
    def __init__(self, nome, sexo, crianca):
        super(Pais, self).__init__(nome, sexo)
        self._crianca = crianca

    def getCrianca(self, i):
        return self._crianca[i]

    def __str__(self):
        return self._nome


p = Pais('test', 'f', ['1', '2', '3'])
print p.getCrianca(1)
print str(p)