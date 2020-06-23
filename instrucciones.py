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

class DeclaracionArray(Declaracion):
    def __init__(self,id_dot,linea,tipo,identificador,indices,valor=None):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.identificador = identificador
        self.indices = indices
        self.valor = valor

class DeclaracionStruct(Instruccion):
    def __init__(self,id_dot,linea,identificador,struct):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.struct = struct

class DeclaracionStructArray(DeclaracionStruct):
    def __init__(self,id_dot,linea,identificador,struct,indices):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.struct = struct

class Asignacion(Instruccion):
    def __init__(self,id_dot,linea,identificador,simbolo_asignacion,valor):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.simbolo_asignacion = simbolo_asignacion
        self.valor = valor

class AsignacionArray(Asignacion):
    def __init__(self,id_dot,linea,identificador,simbolo_asignacion,indices,valor):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.simbolo_asignacion = simbolo_asignacion
        self.indices = indices
        self.valor = valor

class AsignacionStruct(Asignacion):
    def __init__(self,id_dot,linea,identificador,atributo,simbolo_asignacion,valor):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.atributo = atributo
        self.simbolo_asignacion = simbolo_asignacion
        self.valor = valor

class Funcion(Instruccion):
    def __init__(self,id_dot,linea,tipo,nombre,instrucciones,parametros=None):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.parametros = parametros
    
class If(Instruccion):
    def __init__(self,id_dot,linea,expresion,instrucciones):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion
        self.instrucciones = instrucciones

class Ifelse(Instruccion):
    def __init__(self,id_dot,linea,lista_if):
        self.id_dot = id_dot
        self.linea = linea
        self.lista_if =lista_if
