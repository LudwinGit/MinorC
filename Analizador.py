import gramaticaC as gramatica
from expresiones import *
from instrucciones import *

class Analizador:
    def __init__(self,entrada):
        self.ast = gramatica.parse(entrada)
        gramatica.dot.view()
        self.procesar_ast()

    def procesar_ast(self):
        for instruccion in self.ast:
            if isinstance(instruccion,Declaracion): self.procesar_declaracion(instruccion)
            if isinstance(instruccion,Struct):      self.procesar_struct(instruccion)
            if isinstance(instruccion,Funcion):     self.procesar_funcion(instruccion)
            if isinstance(instruccion,Declaracion): self.procesar_asignacion(instruccion)
        return None

    def procesar_declaracion(self,instruccion):
        return None
        if isinstance(instruccion,DeclaracionArray):
            print(1)
        if isinstance(instruccion,DeclaracionStruct):
            print(1)
        if isinstance(instruccion,DeclaracionStructArray):
            print(1)
        if isinstance(instruccion,DeclaracionArray):
            print(1)
        # for var in instruccion.variables:
        #     print(str(var.identificador))

    def procesar_struct(self,instruccion):
        # for atributo in instruccion.atributos:
        #     print(atributo)
        return None

    def procesar_funcion(self,instruccion):
        if instruccion.parametros != None:
            print(".....")
            # for parametro in instruccion.parametros:
            #     print(parametro.identificador)

    def procesar_asignacion(self,instruccion):
        if isinstance(instruccion,AsignacionArray):
            print(1)
        if isinstance(instruccion,AsignacionStruct):
            print(2)