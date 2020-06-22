class Instruccion:
    '''Clase abstracta'''

class Valor(Instruccion):
    def __init__(self,id_dot,valor):
        self.id_dot = id_dot
        self.valor = valor

class Variable:
    def __init__(self,id_dot,identificador,valor=None):
        self.id_dot = id_dot
        self.identificador = identificador
        self.valor = valor

class Declaracion(Instruccion):
    def __init__(self,id_dot,linea,tipo,variables):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.variables = variables
