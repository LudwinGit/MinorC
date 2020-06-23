from enum import Enum

# class TIPO_VARIABLE(Enum):
#     INT = 1
#     VOID = 2
#     CHAR = 3
#     DOUBLE=4
#     FLOAT=5
#     IDENTIFICADOR=6

class OPERACION(Enum):
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3
    DIVISION =4
    RESIDUO = 5

class RELACIONAL(Enum):
    COMPARACION = 1
    DIFERENTE =2
    MAYORIGUAL = 3
    MENORIGUAL = 4
    MAYOR = 5
    MENOR = 6

class LOGICO(Enum):
    AND =1
    OR = 2
    XOR = 3
    NEGACION = 4

class Expresion:
    '''Clase abstracta'''

class ExpNum(Expresion):
    def __init__(self,id_dot,linea,valor):
        self.id_dot = id_dot
        self.linea = linea
        self.valor = valor

class ExpIdentificador(Expresion):
    def __init__(self,id_dot,linea,identificador):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador

class ExpArray(Expresion):
    def __init__(self,id_dot,linea,identificador,indices):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.indices = indices

class ExpresionAritmetica(Expresion):
    def __init__(self,id_dot,linea,expresion1,operador,expresion2):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion1 = expresion1
        self.operador = operador
        self.expresion2 = expresion2

class ExpresionAbsoluto(Expresion):
    def __init__(self,id_dot,linea,expresion):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion

class ExpresionNegativo(Expresion):
    def __init__(self,id_dot,linea,expresion):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion

class ExpresionPuntero(Expresion):
    def __init__(self,id_dot,linea,expresion):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion

class ExpresionCadena(Expresion):
    def __init__(self,id_dot,linea,expresion):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion

class ExpresionRelacional(Expresion):
    def __init__(self,id_dot,linea,expresion1,operador,expresion2):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion1 = expresion1
        self.operador = operador
        self.expresion2 = expresion2