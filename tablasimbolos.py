from enum import Enum
class TIPO(Enum):
    VARIABLE = 1
    ARRAY = 2
    FUNCION = 3
    ETIQUETA = 4

class Simbolo() :
    def __init__(self, id,referencia, tipo,valor,ambito,funcion) :
        self.id = id
        self.referencia = referencia #refencia a la variable de C
        self.tipo = tipo
        self.valor = valor
        self.ambito = ambito
        self.funcion = funcion

class TablaDeSimbolos() :
    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    
    def obtener(self, id) :
        if not id in self.simbolos :
            return None
        return self.simbolos[id]

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo

    def eliminar(self, simbolo):
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            del self.simbolos[simbolo.id]