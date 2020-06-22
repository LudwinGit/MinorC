import gramaticaC as gramatica
from expresiones import *
from instrucciones import *

class Analizador:
    def __init__(self,entrada):
        self.ast = gramatica.parse(entrada)
        self.procesar_ast()

    def procesar_ast(self):
        for instruccion in self.ast:
            if isinstance(instruccion,Declaracion): self.procesar_declaracion(instruccion)
        return None

    def procesar_declaracion(self,instruccion):
        for var in instruccion.variables:
            print(str(var.identificador))

