class Traduccion():
    def __init__(self,resultado,op1,operador,op2):
        self.resultado = resultado
        self.op1 = op1
        self.operador = operador
        self.op2 = op2

class TablaDeTraducciones():
    def __init__(self,traducciones = {}):
        self.traducciones = traducciones

    def agregar(self,traduccion):
        self.traducciones[len(self.traducciones)] = traduccion