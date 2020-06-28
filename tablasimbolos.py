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
        self.simbolos[len(self.simbolos)] = simbolo
    
    def obtener(self, id) :
        for indice in reversed(self.simbolos):
            simbolo = self.simbolos[indice]
            if simbolo.id == id:
                return simbolo
        return None
    
    def obtenerConAmbito(self,id,ambito):
        for indice in reversed(self.simbolos):
            simbolo = self.simbolos[indice]
            if simbolo.id == id and simbolo.ambito == ambito:
                return simbolo
        return None

    def actualizar(self, simbolo) :
        for indice in reversed(self.simbolos):
            s = self.simbolos[indice]
            if s.id == simbolo.id:
                self.simbolos[indice] = simbolo
                return 
        print('Error: variable ', simbolo.id, ' no definida en la tabla de simbolos.')

        # if not simbolo.id in self.simbolos :
        #     print('Error: variable ', simbolo.id, ' no definida.')
        # else :
        #     self.simbolos[simbolo.id] = simbolo

    def eliminar(self, simbolo):
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            del self.simbolos[simbolo.id]