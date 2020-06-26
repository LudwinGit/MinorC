class Error():
    def __init__(self,tipo,descripcion,linea,columna=0):
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna

class ContenedorError():
    def __init__(self,errores ={}):
        self.errores = errores
        self.id = 1

    def agregar(self, error) :
        self.errores[self.id] = error
        self.id += 1