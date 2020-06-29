class Error():
    def __init__(self,tipo,descripcion,linea):
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea

class TablaDeErrores():
    def __init__(self,errores={}):
        self.errores = errores

    def agregar(self,error):
        self.errores[len(self.errores)] = error
    
    def clear(self):
        self.errores.clear()