import gramaticaC as gramatica
from expresiones import *
from instrucciones import *
import tablasimbolos as TS
from ContenedorError import *
import sys


class Analizador:
    def __init__(self, entrada):
        self.ast = gramatica.parse(entrada)
        self.ts_global = TS.TablaDeSimbolos()
        self.traducciones = {}
        self.structs = {}
        self.traducciones[len(self.traducciones)] = "main:"
        self.indice_temporal = 0
        self.procesar_instrucciones(self.ast, self.ts_global, None)
        self.getTraduccion()

    def generarView(self):
        gramatica.dot.view()

    def getTraduccion(self):
        for traduccion in self.traducciones:
            print(self.traducciones[traduccion])
    
    def procesar_instrucciones(self,instrucciones,ts,ambito,traducir=True):
        for instruccion in instrucciones:
            if isinstance(instruccion, Declaracion):
                self.procesar_declaracion(instruccion, ts, ambito,traducir)
            elif isinstance(instruccion, Struct):
                self.procesar_struct(instruccion)
            elif isinstance(instruccion, Funcion):
                self.procesar_funcion(instruccion)
            elif isinstance(instruccion, Asignacion):
                self.procesar_asignacion(instruccion, ts, ambito)
            elif isinstance(instruccion, Expresion):
                self.resolver_expresion(instruccion, ts, ambito)

    def procesar_declaracion(self, instruccion, ts, ambito,traducir=True):
        if isinstance(instruccion, DeclaracionSimple):
            for variable in instruccion.variables:
                valor = self.resolver_expresion(variable.valor, ts, ambito)

                if valor == None:
                    simbolo = self.agregarSimbolo(TS.Simbolo(
                        variable.identificador, "$t"+str(self.indice_temporal), instruccion.tipo, 0, ambito,TS.TIPO.VARIABLE), ts)
                else:
                    simbolo = self.agregarSimbolo(TS.Simbolo(
                        variable.identificador, "$t"+str(self.indice_temporal), instruccion.tipo, valor, ambito,TS.TIPO.VARIABLE), ts)

                if simbolo == None:
                    error = Error(
                        "SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                else:
                    if traducir:
                        if valor != None:
                            traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                        else:
                            traduccion = str(simbolo.referencia)+";"
                        self.agregarTraduccion(traduccion)
        elif isinstance(instruccion,DeclaracionStruct):
            if instruccion.struct in self.structs:
                struct = self.structs[instruccion.struct]
                for i in struct:
                    valor = struct[i]['valor']
                    if struct[i]['tipo'] == TS.TIPO.VARIABLE:
                        referencia = "$t" + str(self.indice_temporal) + "[\'"+str(i)+"\']"
                        id = str(instruccion.identificador)+str(i)
                        simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                        resultado = self.agregarSimbolo(simbolo, ts)
                        
                        if resultado == None:
                            error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                        else:
                            if traducir:
                                traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                                self.agregarTraduccion(traduccion,False)
                    elif struct[i]['tipo'] == TS.TIPO.ARRAY:
                        ref = i.split(",")
                        referencia = "$t" + str(self.indice_temporal) + "[\'"+str(ref[0])+"\']" + str(ref[1])
                        id = str(instruccion.identificador)+str(i)
                        simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                        resultado = self.agregarSimbolo(simbolo, ts)
                        
                        if resultado == None:
                            error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                        else:
                            if traducir:
                                traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                                self.agregarTraduccion(traduccion,False)
            self.indice_temporal += 1  # Para cambiar de variable al finalizar
        elif isinstance(instruccion,DeclaracionStructArray):
            indices = self.resolver_expresion(instruccion.indices[0],ts,ambito)
            indice = 0
            while indice<indices:
                if instruccion.struct in self.structs:
                    struct = self.structs[instruccion.struct]
                    for i in struct:
                        valor = struct[i]['valor']
                        if struct[i]['tipo'] == TS.TIPO.VARIABLE:
                            referencia = "$t" + str(self.indice_temporal)+"["+str(indice)+"]"+ "[\'"+str(i)+"\']"
                            id = str(instruccion.identificador)+str(indice)+str(i)
                            simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                            resultado = self.agregarSimbolo(simbolo, ts)
                            
                            if resultado == None:
                                error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                            else:
                                if traducir:
                                    traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                                    self.agregarTraduccion(traduccion,False)
                        elif struct[i]['tipo'] == TS.TIPO.ARRAY:
                            ref = i.split(",")
                            referencia = "$t" + str(self.indice_temporal) +"["+str(indice)+"]"+ "[\'"+str(ref[0])+"\']" + str(ref[1])
                            id = str(instruccion.identificador)+str(indice)+str(i)
                            simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                            resultado = self.agregarSimbolo(simbolo, ts)
                            
                            if resultado == None:
                                error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                            else:
                                if traducir:
                                    traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                                    self.agregarTraduccion(traduccion,False)
                indice +=1
            self.indice_temporal += 1  # Para cambiar de variable al finalizar
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
                        instruccion.identificador)+",["+str(indice)+"]", referencia, instruccion.tipo, valor, ambito,TS.TIPO.ARRAY), ts)
                    if simbolo == None:
                        error = Error(
                            "SEMANTICO", "La variable ya ha sido declarada ya ha sido definida", instruccion.linea)
                        return
                    else:
                        if traducir:
                            if simbolo.valor != None:
                                traduccion = str(simbolo.referencia) + \
                                    "="+str(simbolo.valor)+";"
                            else:
                                traduccion = str(simbolo.referencia)+";"
                            self.agregarTraduccion(traduccion, False)
                    indice += 1
                self.indice_temporal += 1  # Para cambiar de variable al finalizar

    def procesar_struct(self, instruccion):
        identificador = instruccion.nombre
        ts_local = TS.TablaDeSimbolos()
        struct = {}
        self.procesar_instrucciones(instruccion.atributos,ts_local,"s-"+str(identificador),False)
        for s in ts_local.simbolos:
            simbolo = ts_local.simbolos[s]
            tipo = simbolo.funcion
            struct.setdefault(s,{'valor':0,'tipo':tipo,'valor':simbolo.valor})
        if identificador in self.structs:
                error = Error("SEMANTICO", "El struct \'"+identificador+"\' ya ha sido declarada ya ha sido definida", instruccion.linea)
        else:self.structs.setdefault(identificador,struct)
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
                self.agregarSimbolo(simbolo, ts,TS.TIPO.VARIABLE)
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
                id = instruccion.identificador+",["+str(indice)+"]"
                simbolo = ts.obtener(id)
                if simbolo == None:
                    referencia = "$t" + \
                        str(self.indice_temporal)+"["+str(indice)+"]"
                    simbolo = TS.Simbolo(id, referencia, None, valor, ambito)
                    self.agregarSimbolo(simbolo, ts,TS.TIPO.ARRAY)
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
        elif isinstance(exp, ExpresionAritmetica):
            return self.resolver_aritmetica(exp,ts,ambito)
        elif isinstance(exp, ExpresionSizeof):
            valor = self.resolver_expresion(exp.valor,ts,ambito)
            return sys.getsizeof(valor)
        elif isinstance(exp, ExpIdentificador):
            simbolo = ts.obtener(exp.identificador)
            if simbolo!=None:
                return simbolo.referencia
            error = Error(
                    "SEMANTICO", "La variable \'"+str(exp.identificador)+"\' no ha sido declarada.", exp.linea)
        elif isinstance(exp, ExpArray):
            identificador = exp.identificador
            for i in exp.indices:
                index = self.resolver_expresion(i,ts,ambito)
                identificador += str(index)
            simbolo = ts.obtener(identificador)
            if simbolo != None:
                return simbolo.valor
            error = Error(
                "SEMANTICO", "La variable \'"+str(exp.identificador)+"\' no ha sido declarada.", exp.linea)
        elif isinstance(exp, ExpresionAbsoluto):
            valor = self.resolver_expresion(exp.expresion,ts,ambito)
            try:
                return abs(valor)
            except:
                error = Error(
                "SEMANTICO", "No se puede realizar abs para \'"+str(valor)+"\' .", exp.linea)
                return 0
        elif isinstance(exp, ExpresionNegativo):
            valor = self.resolver_expresion(exp.expresion,ts,ambito)
            try:
                return -1*valor
            except:
                error = Error(
                "SEMANTICO", "No se puede realizar negativo para \'"+str(valor)+"\' .", exp.linea)
                return 0
        elif isinstance(exp, ExpresionCasteo):
            valor = self.resolver_expresion(exp.valor,ts,ambito)
            if valor != None:
                return "("+str(exp.tipo.valor)+")"+str(valor)
        elif isinstance(exp, ExpresionPuntero):
            simbolo = ts.obtener(exp.identificador)
            if simbolo != None:
                return "&"+str(simbolo.referencia)
            error = Error(
                    "SEMANTICO", "La variable \'"+str(exp.identificador)+"\' no ha sido declarada.", exp.linea)
        elif isinstance(exp,ExpresionTernario):
            condicion = self.resolver_expresion(exp.condicion,ts,ambito)
            if condicion == 0:
                return self.resolver_expresion(exp.expFalsa,ts,ambito)
            return self.resolver_expresion(exp.expVerdadera,ts,ambito)
            # return self.resolver_expresion(exp.expVerdadera,ts,ambito)
        return None

    def resolver_aritmetica(self,exp,ts,ambito):
        valor1 = self.resolver_expresion(exp.expresion1,ts,ambito)
        valor2 = self.resolver_expresion(exp.expresion2,ts,ambito)
        if exp.operador == OPERACION.SUMA:
            try:
                return valor1 + valor2
            except:
                return 0
        elif exp.operador == OPERACION.RESTA:
            try:
                return valor1 - valor2
            except:
                return 0
        elif exp.operador == OPERACION.MULTIPLICACION:
            try:
                return valor1 * valor2
            except:
                return 0
        elif exp.operador == OPERACION.DIVISION:
            try:
                return valor1 / valor2
            except:
                return 0
        elif exp.operador == OPERACION.RESIDUO:
            try:
                return valor1 % valor2
            except:
                return 0
        return 0

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
