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
    'Clase abstracta para declaracion'

class DeclaracionSimple(Declaracion):
    def __init__(self,id_dot,linea,tipo,variables):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.variables = variables

class DeclaracionArray(Declaracion):
    def __init__(self,id_dot,linea,tipo,identificador,indices,valores=None):
        self.id_dot = id_dot
        self.linea = linea
        self.tipo = tipo
        self.identificador = identificador
        self.indices = indices
        self.valores = valores

class DeclaracionStruct(Declaracion):
    def __init__(self,id_dot,linea,identificador,struct):
        self.id_dot = id_dot
        self.linea = linea
        self.identificador = identificador
        self.struct = struct

class DeclaracionStructArray(Declaracion):
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
    def __init__(self,id_dot,linea,identificador,atributo,simbolo_asignacion,valor,indices=None):
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

class Etiqueta(Instruccion):
    def __init__(self,id_dot,linea,nombre):
        self.id_dot = id_dot
        self.linea = linea
        self.nombre =nombre

class Switch(Instruccion):
    def __init__(self,id_dot,linea,expresion,casos):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion
        self.casos = casos    

class Case(Instruccion):
    def __init__(self,id_dot,linea,expresion,instrucciones):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion
        self.instrucciones = instrucciones    

class Break(Instruccion):
    def __init__(self,id_dot,linea):
        self.id_dot  = id_dot
        self.linea = linea

class Print(Instruccion):
    def __init__(self,id_dot,linea,prints):
        self.id_dot = id_dot
        self.linea = linea
        self.prints = prints

class Return(Instruccion):
    def __init__(self,id_dot,linea,expresion):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion

class While(Instruccion):
    def __init__(self,id_dot,linea,expresion,instrucciones):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion
        self.instrucciones = instrucciones

class DoWhile(Instruccion):
    def __init__(self,id_dot,linea,expresion,instrucciones):
        self.id_dot = id_dot
        self.linea = linea
        self.expresion = expresion
        self.instrucciones = instrucciones

class For(Instruccion):
    def __init__(self,id_dot,linea,inicializacion,condicion,cambio,instrucciones):
        self.id_dot = id_dot
        self.linea = linea
        self.inicializacion=inicializacion
        self.condicion = condicion
        self.cambio = cambio
        self.instrucciones = instrucciones

class Goto(Instruccion):
    def __init__(self,id_dot,linea,etiqueta):
        self.id_dot = id_dot
        self.linea = linea
        self.etiqueta = etiqueta

class Continue(Instruccion):
    def __init__(self,id_dot,linea):
        self.id_dot  = id_dot
        self.linea = linea