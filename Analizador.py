import gramaticaC as gramatica
from expresiones import *
from instrucciones import *
from tablaerrores import *
import tablasimbolos as TS
import tablatraducciones as TT
import sys


class Analizador:
    def __init__(self, entrada):
        self.ast = gramatica.parse(entrada)
        self.ts_global = TS.TablaDeSimbolos()
        self.traducciones = {}
        self.traducciones2 = {}
        self.traducciones_salida = {}
        self.structs = {}
        self.funciones={}
        self.traducciones[len(self.traducciones)] = { "ambito":0,"traduccion":"main:"}
        self.salida_funciones={}
        self.indice_temporal = 0
        self.indice_parametro = 0
        self.indice_etiqueta = 0
        self.indice_ambito = 0
        self.indice_ambito_max =0
        self.indice_ra=0
        self.procesar_instrucciones(self.ast, self.ts_global,"main0")
        self.getTraduccion()
        # self.imprimir_tabla(self.ts_global)

    def generarView(self):
        gramatica.dot.view()

    def getTraduccion(self):
        for traduccion in self.traducciones2:
            self.traducciones_salida[len(self.traducciones_salida)] = self.traducciones2[traduccion]['traduccion']
            
        # self.traducciones_salida[len(self.traducciones_salida)] = "goto main;" Pendiente
        self.traducciones_salida[len(self.traducciones_salida)] = "exit;"
        for traduccion in reversed(self.traducciones):
            self.traducciones_salida[len(self.traducciones_salida)] = self.traducciones[traduccion]['traduccion']
        for index in reversed(self.traducciones_salida):
            print(self.traducciones_salida[index])
    
    def procesar_instrucciones(self,instrucciones,ts,ambito,traducir=True):
        for instruccion in instrucciones:
            if isinstance(instruccion, Declaracion):
                self.procesar_declaracion(instruccion, ts, ambito,traducir)
            elif isinstance(instruccion, Struct):
                self.procesar_struct(instruccion)
            elif isinstance(instruccion, Funcion):
                self.definir_funcion(instruccion,ts)
            elif isinstance(instruccion, Asignacion):
                self.procesar_asignacion(instruccion, ts, ambito)
            elif isinstance(instruccion, Expresion):
                self.resolver_expresion(instruccion, ts, ambito)
            elif isinstance(instruccion, If):
                self.procesar_if(instruccion,ts,ambito)
            elif isinstance(instruccion,For):
                self.procesar_for(instruccion,ts,ambito)
            elif isinstance(instruccion,Print):
                self.procesar_print(instruccion,ts,ambito)
            elif isinstance(instruccion,LlamaFuncion):
                self.procesar_llamada(instruccion,ts,ambito)

    def procesar_llamada(self,instruccion,ts,ambito):
        if instruccion.funcion in self.funciones:
            funcion = self.funciones[instruccion.funcion]
            etiquetaFin = "final"+str(self.indice_etiqueta)
            self.indice_etiqueta+=1
            for i in funcion['parametros']:
                try:
                    parametro = instruccion.parametros.pop(0)
                    valor = self.resolver_expresion(parametro.identificador,ts,ambito)
                    traduccion = str(funcion['parametros'][i])+"="+str(valor)
                except :
                    valor = 0
                    traduccion = str(funcion['parametros'][i])+"="+str(valor)
                    error = Error("SEMANTICO","PARAMETRO NO SUMINISTRADO",instruccion.linea)
                    gramatica.tablaerrores.agregar(error)
                self.agregarTraduccion(traduccion,False)
            traduccion = "$ra="+str(self.indice_ra)+";"
            self.agregarTraduccion(traduccion,False)
            self.indice_ra += 1

            traduccion = "goto "+funcion['etiqueta']+";"
            self.agregarTraduccion(traduccion,False)
            
            traduccion = str(etiquetaFin)+":"
            self.agregarTraduccion(traduccion,False)
        else:
            error = Error("SEMANTICO","la funcion \'"+str(instruccion.funcion)+"\' no existe",instruccion.linea)
            gramatica.tablaerrores.agregar(error)

    def procesar_print(self,instruccion,ts,ambito):
        for index in instruccion.prints:
            valor = self.resolver_expresion(index.valor,ts,ambito)
            traduccion = "print("+str(valor)+");"
            self.agregarTraduccion(traduccion)
            

    def procesar_instruccion(self,instruccion,ts,ambito,traducir=True):
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
        elif isinstance(instruccion,For):
            self.procesar_for(instruccion,ts,ambito)
        elif isinstance(instruccion,Print):
                self.procesar_print(instruccion,ts,ambito)

    def procesar_declaracion(self, instruccion, ts, ambito,traducir=True):
        if isinstance(instruccion, DeclaracionSimple):
            if(instruccion.tipo == TIPO_DATO.IDENTIFICADOR):
                print("Aun no > solo scruct identificador identificador")
                # variable = instruccion.variables[0]
                # valor = self.resolver_expresion(variable.valor, ts, ambito)
                # struct = self.structs[instruccion.tipo]
            else:
                for variable in instruccion.variables:
                    valor = self.resolver_expresion(variable.valor, ts, ambito)
                    valor = 0 if valor == None else valor
                    simbolo = TS.Simbolo(variable.identificador, "$t"+str(self.indice_temporal), instruccion.tipo, valor, ambito,TS.TIPO.VARIABLE)

                    validarSimbolo = self.agregarSimbolo(simbolo,ts,ambito)

                    if validarSimbolo == None:
                        simbolo = ts.obtener(variable.identificador)
                        error = Error(
                            "SEMANTICO", "La variable \'"+str(variable.identificador)+"\' ya ha sido declarada en el mismo ambito", instruccion.linea)
                        gramatica.tablaerrores.agregar(error)
                    if traducir:
                        if valor != None:
                            traduccion = str(simbolo.referencia)+"="+str(valor)+";"
                        else:
                            traduccion = str(simbolo.referencia)+";"
                        self.agregarTraduccion(traduccion)
        elif isinstance(instruccion,DeclaracionStruct):
            if instruccion.struct in self.structs: #validamos si ya ha sido definido
                struct = self.structs[instruccion.struct]
                declarada = ts.obtener(str(instruccion.identificador))
                if declarada == None:
                    traduccion = "$t" + str(self.indice_temporal) + "=" + "array();"
                    self.agregarTraduccion(traduccion, False)

                for i in struct:
                    valor = struct[i]['valor'] #Obtenemos el valor del atributo que tiene el struct
                    if struct[i]['tipo'] == TS.TIPO.VARIABLE:
                        referencia = "$t" + str(self.indice_temporal)
                        id = str(instruccion.identificador)
                        simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                        validarSimbolo = self.agregarSimbolo(simbolo,ts,ambito)

                        if validarSimbolo == None:
                            simbolo = ts.obtener(id)
                            error = Error(
                                "SEMANTICO", "La variable \'"+str(id)+"\' ya ha sido declarada en el mismo ambito", instruccion.linea)
                            gramatica.tablaerrores.agregar(error)
                        if valor != None:
                            traduccion = str(simbolo.referencia)+ "[\'"+str(i)+"\']"+"="+str(valor)+";"
                        else:
                            traduccion = str(simbolo.referencia)+ "[\'"+str(i)+"\']"+";"
                        self.agregarTraduccion(traduccion)
                    elif struct[i]['tipo'] == TS.TIPO.ARRAY:
                        print("Aun no tipo.array dentro de los atributos")
                        #Aun no  arrays en struct
                        # referencia = "$t" + str(self.indice_temporal)
                        # id = str(instruccion.identificador)
                        # simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                        # resultado = self.agregarSimbolo(simbolo, ts,ambito)
                        
                        # if resultado == None:
                        #     simbolo = ts.obtener(id)
                        #     error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                        
                        # if valor!=None:
                        #     traduccion = str(simbolo.referencia)+ "[\'"+str(id)+"\'] ="+str(valor)+";"
                        # else:
                        #     traduccion = str(simbolo.referencia)+ "[\'"+str(id)+"\'];"
                        # self.agregarTraduccion(traduccion,False)
            self.indice_temporal += 1  # Para cambiar de variable al finalizar
        elif isinstance(instruccion,DeclaracionStructArray):
            if traducir:
                struct = self.structs[instruccion.struct]
                declarada = ts.obtener(str(instruccion.identificador))
                if declarada == None:
                    traduccion = "$t" + str(self.indice_temporal) + "=" + "array();"
                    self.agregarTraduccion(traduccion, False)
                    
                    referencia = "$t" + str(self.indice_temporal)
                    id = str(instruccion.identificador)
                    simbolo = TS.Simbolo(id, referencia, instruccion.struct, 0, ambito,TS.TIPO.VARIABLE)
                    validarSimbolo = self.agregarSimbolo(simbolo,ts,ambito)


            indices = self.resolver_expresion(instruccion.indices[0],ts,ambito)
            indice = 0
            while indice<indices:
                if instruccion.struct in self.structs:
                    struct = self.structs[instruccion.struct]
                    for i in struct:
                        valor = struct[i]['valor']
                        if struct[i]['tipo'] == TS.TIPO.VARIABLE:
                            referencia = "$t" + str(self.indice_temporal)+"["+str(indice)+"]"+ "[\'"+str(i)+"\']"
                            # id = str(instruccion.identificador)+str(indice)+str(i)
                            # simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                            # resultado = self.agregarSimbolo(simbolo, ts,ambito)
                            
                            # if resultado == None:
                            #     error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                            # else:
                            if traducir:
                                traduccion = str(referencia)+"="+str(valor)+";"
                                self.agregarTraduccion(traduccion,False)
                        elif struct[i]['tipo'] == TS.TIPO.ARRAY:
                            ref = i.split(",")
                            referencia = "$t" + str(self.indice_temporal) +"["+str(indice)+"]"+ "[\'"+str(ref[0])+"\']" + str(ref[1])
                            # id = str(instruccion.identificador)+str(indice)+str(i)
                            # simbolo = TS.Simbolo(id, referencia, instruccion.struct, valor, ambito,TS.TIPO.VARIABLE)
                            # resultado = self.agregarSimbolo(simbolo, ts)
                            
                            # if resultado == None:
                            #     error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                            # else:
                            if traducir:
                                traduccion = str(referencia)+"="+str(valor)+";"
                                self.agregarTraduccion(traduccion,False)
                indice +=1
            self.indice_temporal += 1  # Para cambiar de variable al finalizar
        elif isinstance(instruccion, DeclaracionArray):
            referencia = "$t" + str(self.indice_temporal)
            id = str(instruccion.identificador)
            simbolo = TS.Simbolo(id,referencia, instruccion.tipo, 0, ambito,TS.TIPO.ARRAY)
            simbolo = self.agregarSimbolo(simbolo,ts,ambito)
            if simbolo == None:
                error = Error("SEMANTICO", "La variable ya ha sido declarada", instruccion.linea)
                gramatica.tablaerrores.agregar(error)
            if traducir:
                traduccion = referencia + "=" + "array();"
                self.agregarTraduccion(traduccion, False)

            if len(instruccion.indices) > 1:
                indice = 0
                indices = self.resolver_expresion(instruccion.indices[0], ts, ambito)
                if(type(instruccion.valores) == list):
                    valor = 0
                else:
                    valor = self.resolver_expresion(instruccion.valores,ts,ambito)
                while indice < indices:
                    subindice = 0
                    subindices = self.resolver_expresion(instruccion.indices[1],ts,ambito)
                    while subindice < subindices:
                        if traducir:
                            traduccion = "$t"+ str(self.indice_temporal)+ "[" + str(indice) +"]"+"["+str(subindice)+"]"+ str("=") +str(valor)+";"
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
                    # simbolo = TS.Simbolo(variable.identificador, "$t"+str(self.indice_temporal), instruccion.tipo, valor, ambito,TS.TIPO.VARIABLE)
                    # validarSimbolo = self.agregarSimbolo(simbolo,ts,ambito)
                    if traducir:
                        traduccion = "$t"+ str(self.indice_temporal)+ "[" + str(indice) +"]"+ str("=") +str(valor)+";"
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
                gramatica.tablaerrores.agregar(error)
        else:self.structs.setdefault(identificador,struct)
        return None

    def procesar_if(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        if isinstance(instruccion,Ifsimple):
            EtiquetaTrue = "if"+str(self.indice_etiqueta)
            self.indice_etiqueta +=1
            EtiquetaSalida = "salidaif"+str(self.indice_etiqueta)
            self.indice_etiqueta +=1
            if instruccion.expresion != None: #No es un else
                condicion = self.resolver_expresion(instruccion.expresion,ts_local,ambito)
                traduccion = "if ("+str(condicion)+") goto "+str(EtiquetaTrue)+";"
                self.agregarTraduccion(traduccion)
                traduccion = EtiquetaSalida+":"
                self.agregarTraduccion(traduccion)
                self.indice_ambito += 1
                traduccion = "\n"+str(EtiquetaTrue)+":"
                self.agregarTraduccion(traduccion)
                self.procesar_instrucciones(instruccion.instrucciones,ts_local,EtiquetaTrue)
                traduccion = "goto "+str(EtiquetaSalida) +";"
                self.agregarTraduccion(traduccion)
                self.reordenar_traducciones(self.indice_ambito)
                self.indice_ambito -= 1
            else: 
                print("Aun no > else")
                # self.procesar_instrucciones(instruccion.instrucciones,ts_local,ambito)
                # self.reordenar_traducciones(self.indice_ambito)
        elif isinstance(instruccion,Ifelse):
            for item in (instruccion.lista_if):
                self.procesar_if(item,ts,ambito)
        else:
            print("If incorrecto....procesar_if")

    def procesar_for(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        
        etiqueta =str("for")+str(self.indice_etiqueta)
        self.indice_etiqueta+=1

        self.procesar_instruccion(instruccion.inicializacion,ts_local,etiqueta)

        etiquetaIngresa =str("ingresafor")+str(self.indice_etiqueta)
        self.indice_etiqueta+=1
        
        etiquetaSalida =str("salidafor")+str(self.indice_etiqueta)
        self.indice_etiqueta+=1
        
        traduccion = "goto "+str(etiqueta)+";"
        self.agregarTraduccion(traduccion)

        traduccion =  etiquetaSalida+":"
        self.agregarTraduccion(traduccion)

        self.indice_ambito += 1

        traduccion = "\n"+str(etiqueta)+":"
        self.agregarTraduccion(traduccion)
        
        condicion = self.resolver_expresion(instruccion.condicion,ts_local,ambito)

        traduccion = "if("+str(condicion)+") goto "+etiquetaIngresa +";"
        self.agregarTraduccion(traduccion)

        traduccion = "goto "+str(etiquetaSalida) +";"
        self.agregarTraduccion(traduccion)

        traduccion = "\n"+str(etiquetaIngresa)+":"
        self.agregarTraduccion(traduccion)
        self.procesar_instrucciones(instruccion.instrucciones,ts,etiqueta)
        self.procesar_instruccion(instruccion.cambio,ts,etiqueta)

        traduccion = "goto "+str(etiqueta)+";"
        self.agregarTraduccion(traduccion)

        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1
        # self.imprimir_tabla_traducciones(self.traducciones)

        

    def reordenar_traducciones(self,ambito):
        temporal = self.traducciones.copy()
        for i in reversed(temporal):
            traduccion = self.traducciones[i]
            if traduccion['ambito'] == ambito:
                self.traducciones2[len(self.traducciones2)] = self.traducciones.pop(i)

    def imprimir_tabla(self,ts):
        for i in ts.simbolos:
            simbolo = ts.simbolos[i]
            print(simbolo.id,simbolo.referencia)

    def imprimir_tabla_traducciones(self,tt):
        for i in tt:
            print(tt[i])

    def definir_funcion(self, instruccion,ts):

        etiqueta = str(instruccion.nombre)+str(self.indice_etiqueta)
        self.indice_etiqueta +=1
        funcion = {"nombre":instruccion.nombre,"tipo":instruccion.tipo.valor,"parametros":{},"etiqueta":etiqueta}
        simbolo = TS.Simbolo(instruccion.nombre,instruccion.nombre,instruccion.tipo.valor,0,etiqueta,TS.TIPO.FUNCION)
        self.agregarSimbolo(simbolo,ts,etiqueta)
        if instruccion.parametros != None:
            for parametro in instruccion.parametros:
                id =parametro.identificador.identificador
                referencia = "$a"+str(self.indice_parametro)
                self.indice_parametro += 1
                simbolo = TS.Simbolo(id,referencia,instruccion.tipo.valor,0,etiqueta,TS.TIPO.PARAMETRO)
                self.agregarSimbolo(simbolo,ts,instruccion.nombre)
                funcion['parametros'][len(funcion['parametros'])] = referencia
        
        self.indice_ambito += 1
        traduccion = "\n"+str(etiqueta)+":"
        self.agregarTraduccion(traduccion)        
        self.procesar_instrucciones(instruccion.instrucciones,ts,etiqueta)
        
        #Agregamos goto para el bloque de salidas
        traduccion = "goto finfuncion;"
        self.agregarTraduccion(traduccion)        
        
        self.funciones[funcion['nombre']] = funcion
        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1

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
            if len(instruccion.indices) > 0:
                indices = ""
                for i in instruccion.indices:
                    indice = self.resolver_expresion(i,ts,ambito)
                    indices += "["+str(indice)+"]"
                id = instruccion.identificador
                simbolo = ts.obtener(id,TS.TIPO.ARRAY)
                if simbolo == None:
                    error = Error("SEMANTICO", "La variable \'"+str(id)+"\' no existe", instruccion.linea)
                    gramatica.tablaerrores.agregar(error)
                else:
                    referencia = str(simbolo.referencia)+str(indices)
                    traduccion = referencia+"="+str(valor)+";"
                    self.agregarTraduccion(traduccion)
        if isinstance(instruccion,AsignacionStruct):
            valor = self.resolver_expresion(instruccion.valor,ts,ambito)
            if instruccion.indices == None:
                identificador = str(instruccion.identificador)
                simbolo = ts.obtener(identificador)
                if simbolo != None:
                    referencia = str(simbolo.referencia)
                    simbolo.referencia = referencia+"[\'"+str(instruccion.atributo)+"\']"
                    self.procesar_simbolo_asignacion(simbolo,instruccion.simbolo_asignacion, valor, ts)
                    simbolo.referencia = referencia
                else:
                    error = Error(
                    "SEMANTICO", "La variable \'"+str(instruccion.identificador)+"\' no esta definida", instruccion.linea)
                    gramatica.tablaerrores.agregar(error)
            else:
                indices = ""
                for i in instruccion.indices:
                    indice = self.resolver_expresion(i,ts,ambito)
                    indices += "["+str(indice)+"]"
                identificador = str(instruccion.identificador)
                simbolo = ts.obtener(identificador)
                if simbolo != None:
                    referencia = str(simbolo.referencia)
                    simbolo.referencia = referencia+str(indices)+"[\'"+str(instruccion.atributo)+"\']"
                    self.procesar_simbolo_asignacion(simbolo,instruccion.simbolo_asignacion, valor, ts)
                    simbolo.referencia = referencia
                else:
                    error = Error(
                    "SEMANTICO", "La variable \'"+str(instruccion.identificador)+"\' no esta definida", instruccion.linea)
                    gramatica.tablaerrores.agregar(error)

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

    def agregarSimbolo(self, simbolo, ts,ambito):
        temporal = ts.obtenerConAmbito(simbolo.id,ambito)
        if (temporal == None):
            ts.agregar(simbolo)
            return simbolo
        return None

    def agregarTraduccion(self, traduccion, incrementar=True):
        t = {'ambito':self.indice_ambito,'traduccion': traduccion}
        self.traducciones[len(self.traducciones)] = t
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
            gramatica.tablaerrores.agregar(error)
        elif isinstance(exp, ExpArray):
            identificador = exp.identificador
            posiciones = ""
            for i in exp.indices:
                index = self.resolver_expresion(i,ts,ambito)
                posiciones += "["+str(index)+"]"
            simbolo = ts.obtener(identificador,TS.TIPO.ARRAY)
            if simbolo != None:
                return str(simbolo.referencia)+str(posiciones)
            error = Error(
                "SEMANTICO", "La variable \'"+str(exp.identificador)+"\' no ha sido declarada.", exp.linea)
            gramatica.tablaerrores.agregar(error)
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
            simbolo = ts.obtener(exp.identificador,TS.TIPO.ARRAY) if simbolo==None else simbolo
            valor = 0 if simbolo == None else str(simbolo.referencia)
            return "&"+str(valor)
        elif isinstance(exp,ExpresionTernario):
            condicion = self.resolver_expresion(exp.condicion,ts,ambito)
            falso = self.resolver_expresion(exp.expFalsa,ts,ambito)
            verdadero = self.resolver_expresion(exp.expVerdadera,ts,ambito)
            if condicion == 0:
                return self.resolver_expresion(exp.expFalsa,ts,ambito)
            return self.resolver_expresion(exp.expVerdadera,ts,ambito)
            # return self.resolver_expresion(exp.expVerdadera,ts,ambito)
        elif isinstance(exp,ExpresionStruct):
            simbolo = ts.obtener(exp.variable)
            atributo = exp.atributo
            if simbolo == None:
                error = Error("SEMANTICO","La variable \'"+str(exp.variable)+"\' de tipo struct no esta definida")
                gramatica.tablaerrores.agregar(error)
            else:
                if exp.indices !=None:
                    indices=""
                    for i in exp.indices:
                        indice = self.resolver_expresion(i,ts,ambito)
                        indices += "["+str(indice)+"]"
                return str(simbolo.referencia)+str(indices)+"[\'"+str(atributo)+"\']"
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