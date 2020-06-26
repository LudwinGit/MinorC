import gramaticaC as gramatica
from expresiones import *
from instrucciones import *
import tablasimbolos as TS
from ContenedorError import *


class Analizador:
    def __init__(self, entrada):
        self.ast = gramatica.parse(entrada)
        self.ts_global = TS.TablaDeSimbolos()
        self.traducciones = {}
        self.traducciones[len(self.traducciones)] = "main:"
        self.indice_temporal = 0
        self.procesar_ast(self.ast, self.ts_global, None)
        self.getTraduccion()

    def generarView(self):
        gramatica.dot.view()

    def getTraduccion(self):
        for traduccion in self.traducciones:
            print(self.traducciones[traduccion])

    def procesar_ast(self, instrucciones, ts, ambito):
        for instruccion in instrucciones:
            if isinstance(instruccion, Declaracion):
                self.procesar_declaracion(instruccion, ts, ambito)
            if isinstance(instruccion, Struct):
                self.procesar_struct(instruccion)
            if isinstance(instruccion, Funcion):
                self.procesar_funcion(instruccion)
            if isinstance(instruccion, Asignacion):
                self.procesar_asignacion(instruccion, ts, ambito)
            if isinstance(instruccion, Expresion):
                self.resolver_expresion(instruccion, ts, ambito)
        return None

    def procesar_declaracion(self, instruccion, ts, ambito):
        if isinstance(instruccion, DeclaracionSimple):
            for variable in instruccion.variables:
                valor = self.resolver_expresion(variable.valor, ts, ambito)

                if valor == None:
                    simbolo = self.agregarSimbolo(TS.Simbolo(
                        variable.identificador, "$t"+str(self.indice_temporal), instruccion.tipo, 0, ambito), ts)
                else:
                    simbolo = self.agregarSimbolo(TS.Simbolo(
                        variable.identificador, "$t"+str(self.indice_temporal), instruccion.tipo, valor, ambito), ts)

                if simbolo == None:
                    error = Error(
                        "SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                else:
                    if valor != None:
                        traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                    else:
                        traduccion = str(simbolo.referencia)+";"
                    self.agregarTraduccion(traduccion)
        # if isinstance(instruccion,DeclaracionStruct):
        #     print(1)
        # if isinstance(instruccion,DeclaracionStructArray):
        #     print(1)
        elif isinstance(instruccion, DeclaracionArray):
            if len(instruccion.indices) > 1:
                print("Aun no, indices > 1")
                # for index in instruccion.indices:
                # i = self.resolver_expresion(index)
                # if instruccion.valores != None:
                #     if type(instruccion.valores) == list:
                #         valor = self.resolver_expresion(instruccion.valores.pop(0))
                #     else:
                #         valor = self.resolver_expresion(instruccion.valores)
                # else:
                #     valor = 0
                # simbolo = self.agregarSimbolo(TS.Simbolo(str(instruccion.identificador)+str(i),"$t"+str(self.indice_temporal),instruccion.tipo,valor,self.ambito),ts)
            else:
                indice = 0
                indices = self.resolver_expresion(
                    instruccion.indices.pop(0), ts, ambito)
                while indice < indices:
                    if instruccion.valores != None:
                        if type(instruccion.valores) == list:
                            try:
                                valor = self.resolver_expresion(
                                    instruccion.valores.pop(0))
                            except:
                                valor = 0
                        else:
                            valor = self.resolver_expresion(
                                instruccion.valores)
                            valor = valor[1:-1]
                            if instruccion.tipo == TIPO_DATO.CHAR and valor != None:
                                try:
                                    valor = "\'"+str(valor[indice])+"\'"
                                except expression as identifier:
                                    valor = 0
                    else:
                        valor = 0

                    referencia = "$t" + \
                        str(self.indice_temporal)+"["+str(indice)+"]"
                    simbolo = self.agregarSimbolo(TS.Simbolo(str(
                        instruccion.identificador)+str(indice), referencia, instruccion.tipo, valor, ambito), ts)
                    if simbolo == None:
                        error = Error(
                            "SEMANTICO", "La variable ya ha sido declarada ya ha sido definida", instruccion.linea)
                        print(error.descripcion)
                        return
                    else:
                        if simbolo.valor != None:
                            traduccion = str(simbolo.referencia) + \
                                "="+str(simbolo.valor)+";"
                        else:
                            traduccion = str(simbolo.referencia)+";"
                        self.agregarTraduccion(traduccion, False)
                    indice += 1
                self.indice_temporal += 1  # Para cambiar de variable al finalizar

    def procesar_struct(self, instruccion):
        # for atributo in instruccion.atributos:
        #     print(atributo)
        return None

    def procesar_funcion(self, instruccion):
        if instruccion.parametros != None:
            print(".....")
            # for parametro in instruccion.parametros:
            #     print(parametro.identificador)

    def procesar_asignacion(self, instruccion, ts, ambito):
        if isinstance(instruccion, AsignacionSimple):
            valor = self.resolver_expresion(instruccion.valor, ts, ambito)
            simbolo = ts.obtener(instruccion.identificador)
            if simbolo == None:
                simbolo = TS.Simbolo(
                    instruccion.identificador, "$t"+str(self.indice_temporal), None, 0, ambito)
                self.agregarSimbolo(simbolo, ts)
                traduccion = str(simbolo.referencia)+"=0;"
                self.agregarTraduccion(traduccion)
            self.procesar_simbolo_asignacion(
                instruccion, simbolo, instruccion.simbolo_asignacion, valor, ts)
        elif isinstance(instruccion, AsignacionArray):
            valor = self.resolver_expresion(instruccion.valor, ts, ambito)
            if len(instruccion.indices) > 1:
                print("Aun no, indices > 1")
            else:
                indice = self.resolver_expresion(
                    instruccion.indices.pop(0), ts, ambito)
                id = instruccion.identificador+str(indice)
                simbolo = ts.obtener(id)
                if simbolo == None:
                    referencia = "$t" + \
                        str(self.indice_temporal)+"["+str(indice)+"]"
                    simbolo = TS.Simbolo(
                        instruccion.identificador+str(indice), referencia, None, valor, ambito)
                    self.agregarSimbolo(simbolo, ts)
                else:
                    simbolo.valor = valor
                    ts.actualizar(simbolo)
                referencia = str(simbolo.referencia)
                traduccion = referencia+"="+str(valor)+";"
                self.agregarTraduccion(traduccion)
        # if isinstance(instruccion,AsignacionStruct):
        #     print("Asignacion struct")

    def procesar_simbolo_asignacion(self, instruccion, simbolo, simbolo_asignacion, valor, ts):
        if simbolo_asignacion == "=":
            simbolo.valor = valor
            traduccion = str(simbolo.referencia)+"="+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "+=":
            simbolo.valor += valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"+"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "-=":
            simbolo.valor -= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"-"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "*=":
            simbolo.valor *= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"*"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "<<=":
            if type(simbolo.valor) != int or type(valor) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion << en tipos diferentes a int", instruccion.linea)
            else:
                simbolo.valor <<= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"<<"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == ">>=":
            if type(simbolo.valor) != int or type(valor) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion >> en tipos diferentes a int", instruccion.linea)
            else:
                simbolo.valor >>= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+">>"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "&=":
            if type(simbolo.valor) != int or type(valor) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion & en tipos diferentes a int", instruccion.linea)
            else:
                simbolo.valor &= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"&"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "^=":
            if type(simbolo.valor) != int or type(valor) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion ^ en tipos diferentes a int", instruccion.linea)
            else:
                simbolo.valor ^= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"^"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "|=":
            if type(simbolo.valor) != int or type(valor) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion | en tipos diferentes a int", instruccion.linea)
            else:
                simbolo.valor |= valor
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"|"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "/=":
            if valor != 0:
                simbolo.valor /= valor
            else:
                error = Error(
                    "SEMANTICO", "No se puede dividir entre 0", instruccion.linea)
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"/"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "%=":
            if valor != 0:
                simbolo.valor /= valor
            else:
                error = Error(
                    "SEMANTICO", "No se puede dividir entre 0", instruccion.linea)
            traduccion = str(simbolo.referencia)+"=" + \
                str(simbolo.referencia)+"%"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        ts.actualizar(simbolo)

    def agregarSimbolo(self, simbolo, ts):
        temporal = ts.obtener(simbolo.id)
        if (temporal == None):
            ts.agregar(simbolo)
            return simbolo
        return None

    def agregarTraduccion(self, traduccion, incrementar=True):
        self.traducciones[len(self.traducciones)] = traduccion
        if incrementar:
            self.indice_temporal += 1

    def resolver_expresion(self, exp, ts, ambito):
        # if isinstance(exp,ExpIdentificador):
        if isinstance(exp, ExpNum):
            return exp.valor
        elif isinstance(exp, ExpresionCadena):
            return str(exp.valor)
        elif isinstance(exp, ExpresionIncremento):
            identificador = exp.variable
            simbolo = ts.obtener(identificador)
            traduccion = simbolo.referencia+"="+str(simbolo.referencia)+"+1;"
            self.agregarTraduccion(traduccion)
            return (simbolo.valor+1)
        elif isinstance(exp, ExpresionDecremento):
            identificador = exp.variable
            simbolo = ts.obtener(identificador)
            traduccion = simbolo.referencia+"="+str(simbolo.referencia)+"-1;"
            self.agregarTraduccion(traduccion)
            return (simbolo.valor-1)
        elif isinstance(exp, ExpresionRelacional):
            resultado = 1 if self.resolver_relacional(exp, ts, ambito) else 0
            return resultado
        elif isinstance(exp, ExpresionLogica):
            resultado = 1 if self.resolver_logica(exp, ts, ambito) else 0
            return resultado
        elif isinstance(exp, ExpresionBit):
            return self.resolver_bit(exp, ts, ambito)
        return None

    def resolver_bit(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1,ts,ambito)
        valor2 = self.resolver_expresion(exp.expresion2,ts,ambito)
        if exp.operador == BIT.SHIFTIZQUIERDA:
            if type(valor1) != int or type(valor2) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion << en tipos diferentes a int", exp.linea)
            else:
                return valor1 << valor2
        elif exp.operador == BIT.SHIFTDERECHA:
            if type(valor1) != int or type(valor2) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion >> en tipos diferentes a int", exp.linea)
            else:
                return valor1 >> valor2
        elif exp.operador == BIT.AND:
            if type(valor1) != int or type(valor2) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion & en tipos diferentes a int", exp.linea)
            else:
                return valor1 & valor2
        elif exp.operador == BIT.XOR:
            if type(valor1) != int or type(valor2) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion ^ en tipos diferentes a int", exp.linea)
            else:
                return valor1 ^ valor2
        elif exp.operador == BIT.OR:
            if type(valor1) != int or type(valor2) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion | en tipos diferentes a int", exp.linea)
            else:
                return valor1 | valor2
        elif exp.operador == BIT.NOT:
            if type(valor1) != int:
                error = Error(
                    "SEMANTICO", "No se puede realizar la operacion ~ en tipos diferentes a int", exp.linea)
            else:
                return ~valor1
        return 0

    def resolver_logica(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1, ts, ambito)
        valor2 = self.resolver_expresion(exp.expresion2, ts, ambito)

        if exp.operador == LOGICO.AND:
            resultado = valor1 and valor2
            if resultado == True:
                return True
            return False
        elif exp.operador == LOGICO.OR:
            resultado = valor1 or valor2
            if resultado == True:
                return True
            return False
        elif exp.operador == LOGICO.XOR:
            return valor1 != valor2
        elif exp.operador == LOGICO.NEGACION:
            return not valor1

    def resolver_relacional(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1, ts, ambito)
        valor2 = self.resolver_expresion(exp.expresion2, ts, ambito)

        if exp.operador == RELACIONAL.COMPARACION:
            return valor1 == valor2
        elif exp.operador == RELACIONAL.DIFERENTE:
            return valor1 != valor2
        elif exp.operador == RELACIONAL.MAYORIGUAL:
            try:
                return valor1 >= valor2
            except:
                return False
        elif exp.operador == RELACIONAL.MENORIGUAL:
            try:
                return valor1 <= valor2
            except:
                return False
        elif exp.operador == RELACIONAL.MAYOR:
            try:
                return valor1 > valor2
            except:
                return False
        elif exp.operador == RELACIONAL.MENOR:
            try:
                return valor1 < valor2
            except:
                return False
