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
        self.indice_etiqueta = 0
        self.procesar_instrucciones(self.ast, self.ts_global,0)
        self.getTraduccion()
        # self.imprimir_tabla(self.ts_global)

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
            elif isinstance(instruccion, If):
                self.procesar_if(instruccion,ts,ambito)

    def procesar_declaracion(self, instruccion, ts, ambito,traducir=True):
        if isinstance(instruccion, DeclaracionSimple):
            if(instruccion.tipo == TIPO_DATO.IDENTIFICADOR):
                print("Aun no")
                # variable = instruccion.variables[0]
                # valor = self.resolver_expresion(variable.valor, ts, ambito)
                # struct = self.structs[instruccion.tipo]
            else:
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
            if traducir:
                traduccion = "$t" + str(self.indice_temporal) + "=" + "array();"
                self.agregarTraduccion(traduccion, False)
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
            if traducir:
                traduccion = "$t" + str(self.indice_temporal) + "=" + "array();"
                self.agregarTraduccion(traduccion, False)
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
            if traducir:
                traduccion = "$t" + str(self.indice_temporal) + "=" + "array();"
                self.agregarTraduccion(traduccion, False)
            if len(instruccion.indices) > 1:
                #solo se permite 2 indices
                indice = 0
                indices = self.resolver_expresion(instruccion.indices[0],ts,ambito)
                if(type(instruccion.valores) == list):
                    valor = 0
                else:
                    valor = self.resolver_expresion(instruccion.valores,ts,ambito)
                while indice < indices:
                    subindice = 0
                    subindices = self.resolver_expresion(instruccion.indices[1],ts,ambito)
                    while subindice < subindices:
                        referencia = "$t" + str(self.indice_temporal)+"["+str(indice)+"]"+"["+str(subindice)+"]"
                        id = str(instruccion.identificador)+",["+str(indice)+"]"+"["+str(subindice)+"]"
                        simbolo = TS.Simbolo(id,referencia, instruccion.tipo, valor, ambito,TS.TIPO.ARRAY)
                        simbolo = self.agregarSimbolo(simbolo,ts)
                        if simbolo == None:
                            error = Error(
                                "SEMANTICO", "La variable \'"+instruccion.identificador+"\' ya ha sido declarada ya ha sido definida", instruccion.linea)
                        if traducir:
                            if simbolo.valor != None:
                                traduccion = str(simbolo.referencia) + \
                                    "="+str(simbolo.valor)+";"
                            else:
                                traduccion = str(simbolo.referencia)+";"
                        self.agregarTraduccion(traduccion, False)
                        subindice +=1
                    indice += 1
            else:
                indice = 0
                indices = self.resolver_expresion(instruccion.indices.pop(0), ts, ambito)
                while indice < indices:
                    if instruccion.valores != None:
                        if type(instruccion.valores) == list:
                            try:
                                valor = self.resolver_expresion(instruccion.valores[indice],ts,ambito)
                            except:
                                valor = 0
                        else:
                            valor = self.resolver_expresion(instruccion.valores,ts,ambito)
                            if instruccion.tipo == TIPO_DATO.CHAR and valor != None:
                                valor = valor[1:-1]
                                try:
                                    valor = "\'"+str(valor[indice])+"\'"
                                except:
                                    valor = 0
                    else:
                        valor = 0

                    referencia = "$t" + str(self.indice_temporal)+"["+str(indice)+"]"
                    simbolo = self.agregarSimbolo(TS.Simbolo(str(
                        instruccion.identificador)+",["+str(indice)+"]", referencia, instruccion.tipo, valor, ambito,TS.TIPO.ARRAY), ts)
                    if simbolo == None:
                        error = Error(
                            "SEMANTICO", "La variable \'"+instruccion.identificador+"\' ya ha sido declarada ya ha sido definida", instruccion.linea)
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
            struct.setdefault(simbolo.id,{'valor':0,'tipo':tipo,'valor':simbolo.valor})
        if identificador in self.structs:
                error = Error("SEMANTICO", "El struct \'"+identificador+"\' ya ha sido declarada ya ha sido definida", instruccion.linea)
        else:self.structs.setdefault(identificador,struct)
        return None

    def procesar_if(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        ambito += 1
        if isinstance(instruccion,If):
            condicion = self.resolver_expresion(instruccion.expresion,ts_local,ambito)
            traduccion = "if ("+condicion+") goto"+" if"+str(self.indice_etiqueta)+";"
            self.agregarTraduccion(traduccion)
            traduccion = "\nif"+str(self.indice_etiqueta)+":"
            self.indice_etiqueta +=1
            self.agregarTraduccion(traduccion)
            self.procesar_instrucciones(instruccion.instrucciones,ts_local,ambito)

    def imprimir_tabla(self,ts):
        for i in ts.simbolos:
            simbolo = ts.simbolos[i]
            print(simbolo.id,simbolo.referencia)

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
                simbolo = TS.Simbolo(instruccion.identificador, "$t"+str(self.indice_temporal), None, 0, ambito,TS.TIPO.VARIABLE)
                self.agregarSimbolo(simbolo, ts)
                traduccion = str(simbolo.referencia)+"=0;"
                self.agregarTraduccion(traduccion)
            self.procesar_simbolo_asignacion(simbolo, instruccion.simbolo_asignacion, valor, ts)
        elif isinstance(instruccion, AsignacionArray):
            valor = self.resolver_expresion(instruccion.valor, ts, ambito)
            if len(instruccion.indices) > 1:
                indices = ""
                for i in instruccion.indices:
                    indice = self.resolver_expresion(i,ts,ambito)
                    indices += "["+str(indice)+"]"
                id = instruccion.identificador+","+indices
                simbolo = ts.obtener(id)
                if simbolo == None:
                    referencia = "$t" + \
                        str(self.indice_temporal)+indices
                    simbolo = TS.Simbolo(id, referencia, None, valor, ambito,TS.TIPO.ARRAY)
                    self.agregarSimbolo(simbolo, ts)
                else:
                    simbolo.valor = valor
                    ts.actualizar(simbolo)
                referencia = str(simbolo.referencia)
                traduccion = referencia+"="+str(valor)+";"
                self.agregarTraduccion(traduccion)
            else:
                indice = self.resolver_expresion(
                    instruccion.indices.pop(0), ts, ambito)
                id = instruccion.identificador+",["+str(indice)+"]"
                simbolo = ts.obtener(id)
                if simbolo == None:
                    referencia = "$t" + \
                        str(self.indice_temporal)+"["+str(indice)+"]"
                    simbolo = TS.Simbolo(id, referencia, None, valor, ambito,TS.TIPO.ARRAY)
                    self.agregarSimbolo(simbolo, ts)
                else:
                    simbolo.valor = valor
                    ts.actualizar(simbolo)
                referencia = str(simbolo.referencia)
                traduccion = referencia+"="+str(valor)+";"
                self.agregarTraduccion(traduccion)
        if isinstance(instruccion,AsignacionStruct):
            valor = self.resolver_expresion(instruccion.valor,ts,ambito)
            if instruccion.indices == None:
                identificador = str(instruccion.identificador)+str(instruccion.atributo)
                simbolo = ts.obtener(identificador)
                if simbolo != None:
                    self.procesar_simbolo_asignacion(simbolo,instruccion.simbolo_asignacion, valor, ts)
                else:
                    error = Error(
                    "SEMANTICO", "La variable \'"+str(instruccion.identificador)+"\' no esta definida", instruccion.linea)
            else:
                indices = ""
                for i in instruccion.indices:
                    indice = self.resolver_expresion(i,ts,ambito)
                    indices +=str(indice)
                identificador = str(instruccion.identificador)+str(indices)+str(instruccion.atributo)
                simbolo = ts.obtener(identificador)
                if simbolo != None:
                    self.procesar_simbolo_asignacion(simbolo,instruccion.simbolo_asignacion, valor, ts)
                else:
                    error = Error(
                    "SEMANTICO", "La variable \'"+str(instruccion.identificador)+"\' no esta definida", instruccion.linea)

    def procesar_simbolo_asignacion(self, simbolo, simbolo_asignacion, valor, ts):
        if simbolo_asignacion == "=":
            traduccion = str(simbolo.referencia)+"="+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "+=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"+"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "-=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"-"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "*=":
            simbolo.valor *= valor
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"*"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "<<=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"<<"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == ">>=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+">>"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "&=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"&"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "^=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"^"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "|=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"|"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "/=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"/"+str(valor)+";"
            self.agregarTraduccion(traduccion, False)
        elif simbolo_asignacion == "%=":
            traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"%"+str(valor)+";"
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
            return simbolo.referencia
        elif isinstance(exp, ExpresionDecremento):
            identificador = exp.variable
            simbolo = ts.obtener(identificador)
            traduccion = simbolo.referencia+"="+str(simbolo.referencia)+"-1;"
            self.agregarTraduccion(traduccion)
            return simbolo.referencia
        elif isinstance(exp, ExpresionRelacional):
            return self.resolver_relacional(exp, ts, ambito)
        elif isinstance(exp, ExpresionLogica):
            return self.resolver_logica(exp, ts, ambito)
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
            posiciones = ""
            for i in exp.indices:
                index = self.resolver_expresion(i,ts,ambito)
                posiciones += "["+str(index)+"]"
            identificador += ","+posiciones
            simbolo = ts.obtener(identificador)
            if simbolo != None:
                return simbolo.referencia
            error = Error(
                "SEMANTICO", "La variable \'"+str(exp.identificador)+"\' no ha sido declarada.", exp.linea)
        elif isinstance(exp, ExpresionAbsoluto):
            valor = self.resolver_expresion(exp.expresion,ts,ambito)
            return "abs("+str(valor)+")"
        elif isinstance(exp, ExpresionNegativo):
            valor = self.resolver_expresion(exp.expresion,ts,ambito)
            return "-"+str(valor)
        elif isinstance(exp, ExpresionCasteo):
            valor = self.resolver_expresion(exp.valor,ts,ambito)
            return "("+str(exp.tipo.valor)+")"+str(valor)
        elif isinstance(exp, ExpresionPuntero):
            simbolo = ts.obtener(exp.identificador)
            valor = 0 if simbolo == None else str(simbolo.referencia)
            return "&"+str(valor)
        elif isinstance(exp,ExpresionTernario):
            condicion = self.resolver_expresion(exp.condicion,ts,ambito)
            falso = self.resolver_expresion(exp.expFalsa,ts,ambito)
            verdadero = self.resolver_expresion(exp.expVerdadera,ts,ambito)
            print(condicion,"----")
            if condicion == 0:
                return self.resolver_expresion(exp.expFalsa,ts,ambito)
            return self.resolver_expresion(exp.expVerdadera,ts,ambito)
            # return self.resolver_expresion(exp.expVerdadera,ts,ambito)
        return 0

    def resolver_aritmetica(self,exp,ts,ambito):
        valor1 = self.resolver_expresion(exp.expresion1,ts,ambito)
        valor2 = self.resolver_expresion(exp.expresion2,ts,ambito)
        if exp.operador == OPERACION.SUMA:
            referencia = "$t"+str(self.indice_temporal)
            traduccion = referencia+"="+str(valor1)+"+"+str(valor2)+";"
        elif exp.operador == OPERACION.RESTA:
            referencia = "$t"+str(self.indice_temporal)
            traduccion = referencia+"="+str(valor1)+"-"+str(valor2)+";"
        elif exp.operador == OPERACION.MULTIPLICACION:
            referencia = "$t"+str(self.indice_temporal)
            traduccion = referencia+"="+str(valor1)+"*"+str(valor2)+";"
        elif exp.operador == OPERACION.DIVISION:
            referencia = "$t"+str(self.indice_temporal)
            traduccion = referencia+"="+str(valor1)+"/"+str(valor2)+";"
        elif exp.operador == OPERACION.RESIDUO:
            referencia = "$t"+str(self.indice_temporal)
            traduccion = referencia+"="+str(valor1)+"%"+str(valor2)+";"

        self.agregarTraduccion(traduccion)
        return str(referencia)
        
    def resolver_bit(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1,ts,ambito)
        valor2 = self.resolver_expresion(exp.expresion2,ts,ambito)

        referencia = "$t"+str(self.indice_temporal)
        if exp.operador == BIT.SHIFTIZQUIERDA:
            traduccion = referencia+"="+str(valor1)+" << "+str(valor2)+";"
        elif exp.operador == BIT.SHIFTDERECHA:
            traduccion = referencia+"="+str(valor1)+" >> "+str(valor2)+";"
        elif exp.operador == BIT.AND:
            traduccion = referencia+"="+str(valor1)+" & "+str(valor2)+";"
        elif exp.operador == BIT.XOR:
            traduccion = referencia+"="+str(valor1)+" ^ "+str(valor2)+";"
        elif exp.operador == BIT.OR:
            traduccion = referencia+"="+str(valor1)+" | "+str(valor2)+";"
        elif exp.operador == BIT.NOT:
            traduccion = referencia+"="+"~"+str(valor1)+";"

        self.agregarTraduccion(traduccion)
        return str(referencia)

    def resolver_logica(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1, ts, ambito)
        valor2 = self.resolver_expresion(exp.expresion2, ts, ambito)

        referencia = "$t"+str(self.indice_temporal)
        if exp.operador == LOGICO.AND:
            traduccion = referencia+"="+str(valor1)+" && "+str(valor2)+";"
        elif exp.operador == LOGICO.OR:
            traduccion = referencia+"="+str(valor1)+" || "+str(valor2)+";"
        elif exp.operador == LOGICO.XOR:
            traduccion = referencia+"="+str(valor1)+" xor "+str(valor2)+";"
        elif exp.operador == LOGICO.NEGACION:
            traduccion = referencia+"= !"+str(valor1)+";"
        
        self.agregarTraduccion(traduccion)
        return str(referencia)

    def resolver_relacional(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1, ts, ambito)
        valor2 = self.resolver_expresion(exp.expresion2, ts, ambito)

        referencia = "$t"+str(self.indice_temporal)
        if exp.operador == RELACIONAL.COMPARACION:
            traduccion = referencia+"="+str(valor1)+"=="+str(valor2)+";"
        elif exp.operador == RELACIONAL.DIFERENTE:
            traduccion = referencia+"="+str(valor1)+"!="+str(valor2)+";"
        elif exp.operador == RELACIONAL.MAYORIGUAL:
            traduccion = referencia+"="+str(valor1)+">="+str(valor2)+";"
        elif exp.operador == RELACIONAL.MENORIGUAL:
            traduccion = referencia+"="+str(valor1)+"<="+str(valor2)+";"
        elif exp.operador == RELACIONAL.MAYOR:
            traduccion = referencia+"="+str(valor1)+">"+str(valor2)+";"
        elif exp.operador == RELACIONAL.MENOR:
            traduccion = referencia+"="+str(valor1)+"<"+str(valor2)+";"

        self.agregarTraduccion(traduccion)
        return str(referencia)