from enum import Enum

# class TIPO_VARIABLE(Enum):
#     INT = 1
#     VOID = 2
#     CHAR = 3
#     DOUBLE=4
#     FLOAT=5
#     IDENTIFICADOR=6

class Expresion:
    '''Clase abstracta'''

class ExpNum(Expresion):
    def __init__(self,id_dot,linea,valor):
        self.id_dot = id_dot
        self.linea = linea
        self.valor = valor