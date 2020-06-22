class Instruccion:
    '''Clase abstracta'''

class Valor(Instruccion):
    def __init__(self,id_dot,valor):
        self.id_dot = id_dot
        self.valor = valor

class Variable:
    def __init__(self,id_dot,linea,identificador,valor=None):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.valor = valor

class Parametro:
    def __init__(self,id_dot,linea,identificador,tipo=None):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.tipo = tipo

class Struct(Instruccion):
    def __init__(self,id_dot,linea,nombre,atributos):
        self.id_dot = id_dot
        self.linea = linea
        self.nombre = nombre
        self.atributos = atributos

class Declaracion(Instruccion):
    def __init__(self,id_dot,linea,tipo,variables):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.variables = variables

class Funcion(Instruccion):
    def __init__(self,id_dot,linea,tipo,nombre,instrucciones,parametros=None):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.parametros = parametros