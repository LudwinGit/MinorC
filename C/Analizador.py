import C.gramaticaC as gramatica
from C.expresiones import *
from C.instrucciones import *
from C.tablaerrores import *
import C.tablasimbolos as TS
import C.tablatraducciones as TT
import sys
import re
from graphviz import Graph,Digraph, nohtml

class Analizador:
    def __init__(self):
        self.ast = {}
        self.ts_global = TS.TablaDeSimbolos()
        self.traducciones = {}
        self.traducciones2 = {}
        self.traducciones_salida = {}
        self.pila_control = {} #Para llegar a la profundidad de while,for,switch,etc para usar break,continue
        self.indice_pila_control = 0
        self.structs = {}
        self.funciones={}
        self.funcion_actual = ""
        self.cadena_rep_optimizacion = ""
        self.traducciones[len(self.traducciones)] = { "ambito":0,"traduccion":TT.Traduccion("","main","","",":")}
        self.salida_funciones={}
        self.indice_temporal = 0
        self.indice_retorno = 0
        self.indice_parametro = 0
        self.indice_etiqueta = 0
        self.indice_ambito = 0
        self.indice_ambito_max =0
        self.indice_ra=1
        self.indice_pila = 0
        self.pila_funciones = []
        self.pila_funciones.append(0)
        self.etiqueta_princial = "" #main
        self.traducir_general = False
        self.llenarFunciones(self.ast,self.ts_global,"main")
        self.procesar_instrucciones(self.ast, self.ts_global,"main")
        # self.getTraduccion()
        # self.imprimir_tabla(self.ts_global)

    def run(self,entrada):
        self.ast = gramatica.parse(entrada)
        self.ts_global = TS.TablaDeSimbolos()
        self.traducciones = {}
        self.traducciones2 = {}
        self.traducciones_salida = {}
        self.traducciones_optimizada={}
        self.structs = {}
        self.funciones={}
        self.funcion_actual = ""
        self.traducciones[len(self.traducciones)] = { "ambito":0,"traduccion":TT.Traduccion("","main","","",":")}
        self.salida_funciones={}
        self.indice_temporal = 0
        self.indice_retorno = 0
        self.indice_parametro = 0
        self.indice_etiqueta = 0
        self.indice_ambito = 0
        self.indice_ambito_max =0
        self.indice_ra=1
        self.indice_pila = 0
        self.pila_funciones = []
        self.pila_funciones.append(0)
        self.etiqueta_princial = "" #main
        self.traducir_general = False
        self.llenarFunciones(self.ast,self.ts_global,"main")
        self.procesar_instrucciones(self.ast, self.ts_global,"main")

    def optimizar(self):
        self.regla1()
        self.regla8()
        self.regla9()
        self.regla10()
        self.regla11()
        self.regla12()
        self.regla13()
        self.regla14()
        self.regla15()
        self.regla16()
        self.regla17()
        self.regla18()
        return self.traducciones_optimizada
    
    def regla1(self):
        for index in self.traducciones_salida:
            traduccion = self.traducciones_salida[index]
            if index+1 < len(self.traducciones_salida):
                traduccion2 = self.traducciones_salida[index+1]
                if traduccion.resultado == traduccion2.op1 and traduccion.op1==traduccion2.resultado and str(traduccion.resultado) != str(traduccion.op1):
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+str(traduccion.simbolofinaliza)+\
                                "<BR/>"+str(traduccion2.resultado)+"="+str(traduccion2.op1)+str(traduccion2.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 1")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+str(traduccion2.simbolofinaliza)+"</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    traduccion2.resultado = traduccion.resultado
                    traduccion2.op1 = traduccion.op1
                    continue
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla8(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "+":
                if str(traduccion.resultado) == str(traduccion.op1) and str(traduccion.op2) == "0":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"+0"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 8")+"</TD>"+\
                                "<TD>#SE ELIMINA LA INSTRUCCIÓN</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    continue
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla9(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "-":
                if str(traduccion.resultado) == str(traduccion.op1) and str(traduccion.op2) == "0":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"-0"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 9")+"</TD>"+\
                                "<TD>#SE ELIMINA LA INSTRUCCIÓN</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    continue
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla10(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "*":
                if str(traduccion.resultado) == str(traduccion.op1) and str(traduccion.op2) == "1":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"*1"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 10")+"</TD>"+\
                                "<TD>#SE ELIMINA LA INSTRUCCIÓN</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    continue
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla11(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "/":
                if str(traduccion.resultado) == str(traduccion.op1) and str(traduccion.op2) == "1":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"/1"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 11")+"</TD>"+\
                                "<TD>#SE ELIMINA LA INSTRUCCIÓN</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    continue
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla12(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "+":
                if str(traduccion.resultado) != str(traduccion.op1) and str(traduccion.op2) == "0":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"+0"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 12")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+str(traduccion.simbolofinaliza)+"</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    traduccion.operador = ""
                    traduccion.op2 = ""
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla13(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "-":
                if str(traduccion.resultado) != str(traduccion.op1) and str(traduccion.op2) == "0":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"-0"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 13")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+str(traduccion.simbolofinaliza)+"</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    traduccion.operador = ""
                    traduccion.op2 = ""
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla14(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "*":
                if str(traduccion.resultado) != str(traduccion.op1) and str(traduccion.op2) == "1":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"*1"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 14")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+str(traduccion.simbolofinaliza)+"</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    traduccion.operador = ""
                    traduccion.op2 = ""
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion
    
    def regla15(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "/":
                if str(traduccion.resultado) != str(traduccion.op1) and str(traduccion.op2) == "1":
                    cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"/1"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 15")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+str(traduccion.simbolofinaliza)+"</TD>"+"</TR>"
                    self.cadena_rep_optimizacion += cadena
                    traduccion.operador = ""
                    traduccion.op2 = ""
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla16(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "*" and str(traduccion.op2) == "2":
                cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"*2"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 16")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"+"+str(traduccion.op1)+str(traduccion.simbolofinaliza)+"</TD>"+"</TR>"
                self.cadena_rep_optimizacion += cadena
                traduccion.operador = "+"
                traduccion.op2 = traduccion.op1
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla17(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "*" and str(traduccion.op2) == "0":
                cadena = "<TR><TD>"+str(traduccion.resultado)+"="+str(traduccion.op1)+"*0"+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 17")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"=0"+"</TD>"+"</TR>"
                self.cadena_rep_optimizacion += cadena
                traduccion.op1 = ""
                traduccion.operador = ""
                traduccion.op2 = "0"
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def regla18(self):
        copia = self.traducciones_optimizada.copy()
        self.traducciones_optimizada = {}

        for index in copia:
            traduccion = copia[index]
            if str(traduccion.operador) == "/" and str(traduccion.op1) == "0":
                cadena = "<TR><TD>"+str(traduccion.resultado)+"="+"0/"+str(traduccion.op1)+str(traduccion.simbolofinaliza)+"</TD>"+\
                                "<TD>"+str("REGLA 18")+"</TD>"+\
                                "<TD>"+str(traduccion.resultado)+"=0"+"</TD>"+"</TR>"
                self.cadena_rep_optimizacion += cadena
                traduccion.op1 = ""
                traduccion.operador = ""
                traduccion.op2 = "0"
            self.traducciones_optimizada[len(self.traducciones_optimizada)] = traduccion

    def generarView(self):
        gramatica.dot.view()
    
    def generarRepGramatical(self):
        gramatica.dotgramatica.view()

    def generarRepOptimizacion(self):
        SymbolT = Digraph('g', filename='gram_minor.gv', format='png',node_attr={'shape': 'plaintext', 'height': '.1'})

        SymbolT.node('table','''<<TABLE>
                                <TR>
                                    <TD>CASO</TD>
                                    <TD>REGLA</TD>
                                    <TD>OPTIMIZACION</TD>
                                </TR>'''
                                +self.cadena_rep_optimizacion+
                            '''</TABLE>>''')

        SymbolT.view()

    def generarRepSimbolos(self):
        SymbolT = Digraph('g', filename='btree.gv',
                node_attr={'shape': 'plaintext', 'height': '.1'})        
        cadena=''
        for item in self.ts_global.simbolos:
            # sim=ts.obtener(item,1)
            sim = self.ts_global.simbolos[item]
            cadena+='<TR><TD>'+str(sim.id)+'</TD>'+'<TD>'+str(sim.referencia)+'</TD>'+'<TD>'+str(sim.tipo)+'</TD>'+'<TD>'+str(sim.valor)+'</TD>'+'<TD>'+str(sim.ambito)+'</TD>'+'<TD>'+str(sim.funcion)+'</TD></TR>'

        # for fn in ts.funciones:
        #     fun=ts.obtenerFuncion(fn)
        #     cadena+='<TR><TD>'+str(fun.id)+'</TD>'+'<TD>'+str(fun.tipo)+'</TD>'+'<TD>'+str(fun.parametros)+'</TD>'+'<TD></TD>'+'<TD></TD>'+'<TD>'+str(fun.referencia)+'</TD></TR>'

        SymbolT.node('table','''<<TABLE>
                                <TR>
                                    <TD>ID</TD>
                                    <TD>TRADUCCION</TD>
                                    <TD>TIPO</TD>
                                    <TD>VALOR</TD>
                                    <TD>DECLARADA EN</TD>
                                    <TD>USO</TD>
                                </TR>'''
                                +cadena+
                            '''</TABLE>>''')

        SymbolT.view()

    def generarRepErrores(self):
        SymbolT = Digraph('g', filename='btree.gv',
                node_attr={'shape': 'plaintext', 'height': '.1'})        
        cadena=''
        for item in gramatica.tablaerrores.errores:
            sim = gramatica.tablaerrores.errores[item]
            cadena+='<TR><TD>'+str(sim.tipo)+'</TD>'+'<TD>'+str(sim.descripcion)+'</TD>'+'<TD>'+str(sim.linea)+'</TD></TR>'

        SymbolT.node('table','''<<TABLE>
                                <TR>
                                    <TD>TIPO</TD>
                                    <TD>DESCRIPCION</TD>
                                    <TD>LINEA</TD>
                                </TR>'''
                                +cadena+
                            '''</TABLE>>''')

        SymbolT.view()

    def getTraduccion(self):
        self.indice_ra -= 1
        while self.indice_ra >= 0:
            traduccion = TT.Traduccion("","if ($ra == "+str(self.indice_ra)+")"," goto ","final"+str(self.indice_ra),";")
            self.traducciones_salida[len(self.traducciones_salida)] = traduccion
            self.indice_ra -= 1
        self.traducciones_salida[len(self.traducciones_salida)] = TT.Traduccion("","\nfinfuncion","","",":")

        for traduccion in self.traducciones2:
            self.traducciones_salida[len(self.traducciones_salida)] = self.traducciones2[traduccion]['traduccion']
        
        self.traducciones_salida[len(self.traducciones_salida)] = TT.Traduccion("","exit","","",";")
        self.traducciones_salida[len(self.traducciones_salida)] = TT.Traduccion("","final0","","",":")
        self.traducciones_salida[len(self.traducciones_salida)] =TT.Traduccion("","goto "+str(self.etiqueta_princial),"","",";")
        self.traducciones_salida[len(self.traducciones_salida)] =TT.Traduccion("$ra","0","","",";")
        self.traducciones_salida[len(self.traducciones_salida)] =TT.Traduccion("$s0","array()","","",";")
        for traduccion in reversed(self.traducciones):
            self.traducciones_salida[len(self.traducciones_salida)] = self.traducciones[traduccion]['traduccion']
        # for index in reversed(self.traducciones_salida):
        #     t = self.traducciones_salida[index]
        #     if t.resultado == "":
        #         print(str(t.resultado)+str(t.op1)+str(t.operador)+str(t.op2)+str(t.simbolofinaliza))
        #     else:                
        #         print(str(t.resultado)+"="+str(t.op1)+str(t.operador)+str(t.op2)+str(t.simbolofinaliza))

        return self.traducciones_salida
    
    def llenarFunciones(self,instrucciones,ts,ambito):
        self.traducir_general = False
        for instruccion in instrucciones:
            if isinstance(instruccion, Funcion):self.definir_funcion(instruccion,ts)

    def procesar_instrucciones(self,instrucciones,ts,ambito,traducir=True):
        self.traducir_general = True
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
                self.procesar_ifelse(instruccion,ts,ambito)
            elif isinstance(instruccion,For):
                self.procesar_for(instruccion,ts,ambito)
            elif isinstance(instruccion,Print):
                self.procesar_print(instruccion,ts,ambito)
            elif isinstance(instruccion,LlamaFuncion):
                self.procesar_llamada(instruccion,ts,ambito)
            elif isinstance(instruccion,Return):
                self.procesar_return(instruccion,ts,ambito)
            elif isinstance(instruccion,While):
                self.procesar_while(instruccion,ts,ambito)
            elif isinstance(instruccion,Switch):
                self.procesar_switch(instruccion,ts,ambito)
            elif isinstance(instruccion,DoWhile):
                self.procesar_dowhile(instruccion,ts,ambito)
            elif isinstance(instruccion,Etiqueta):
                etiqueta = "E"+str(instruccion.nombre)
                self.indice_etiqueta +=1
                traduccion = TT.Traduccion("","\n"+str(etiqueta),"","",":")
                self.agregarTraduccion(traduccion)
            elif isinstance(instruccion,Goto):
                etiqueta = "E"+str(instruccion.etiqueta)
                self.indice_etiqueta +=1
                traduccion = TT.Traduccion("","goto "+str(etiqueta),"","",";")
                self.agregarTraduccion(traduccion)
            elif isinstance(instruccion,Break):
                indice = len(self.pila_control)-1
                if indice>=0:
                    traduccion = TT.Traduccion("","goto "+str(self.pila_control[indice]),"","",";")
                    self.agregarTraduccion(traduccion)

    def procesar_dowhile(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        
        etiqueta = "dowhile"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1

        etiquetacond = "docondicion"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1

        etiquetasalida = "dowhilefin"+str(self.indice_etiqueta)
        self.pila_control.setdefault(len(self.pila_control),str(etiquetasalida))
        self.indice_etiqueta +=1

        traduccion = TT.Traduccion("",str(etiqueta),"","",":")
        self.agregarTraduccion(traduccion)
        self.procesar_instrucciones(instruccion.instrucciones,ts_local,etiqueta)
        traduccion = TT.Traduccion("","goto "+str(etiquetacond),"","",";")
        self.agregarTraduccion(traduccion)
        
        traduccion = TT.Traduccion("",str(etiquetasalida),"","",":")
        self.agregarTraduccion(traduccion)

        self.indice_ambito += 1
        traduccion = TT.Traduccion("","\n"+str(etiquetacond),"","",":")
        self.agregarTraduccion(traduccion)
        # self.procesar_instrucciones(instruccion.instrucciones,ts_local,etiqueta)
        condicion = self.resolver_expresion(instruccion.expresion,ts,ambito)
        traduccion = TT.Traduccion("","if("+str(condicion)+")"," goto ",str(etiqueta),";")
        self.agregarTraduccion(traduccion)
        traduccion = TT.Traduccion("","goto "+str(etiquetasalida),"","",";")
        self.agregarTraduccion(traduccion)
        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1
        
        self.pila_control.pop(len(self.pila_control)-1)

    def procesar_return(self,instruccion,ts,ambito):
        simbolo = ts.buscarReturn(self.funcion_actual)
        if simbolo != None:
            valor = self.resolver_expresion(instruccion.expresion,ts,ambito)
            traduccion = TT.Traduccion(str(simbolo.id),str(valor),"","",";")
            self.agregarTraduccion(traduccion)
            traduccion = TT.Traduccion("","goto return"+str(self.funcion_actual),"","",";")
            self.agregarTraduccion(traduccion)

    def procesar_llamada(self,instruccion,ts,ambito):        
        if instruccion.funcion in self.funciones:
            funcion = self.funciones[instruccion.funcion]
            etiquetaFin = "final"+str(self.indice_ra)
            self.indice_etiqueta+=1
            for i in funcion['parametros']:
                try:
                    parametro = instruccion.parametros.pop(0)
                    valor = self.resolver_expresion(parametro.identificador,ts,ambito)
                    traduccion = TT.Traduccion(str(funcion['parametros'][i]),str(valor),"","",";")
                except :
                    valor = 0
                    traduccion = TT.Traduccion(str(funcion['parametros'][i]),str(valor),"","",";")
                    error = Error("SEMANTICO","PARAMETRO NO SUMINISTRADO",instruccion.linea)
                    gramatica.tablaerrores.agregar(error)
                self.agregarTraduccion(traduccion,False)
            traduccion = TT.Traduccion("$ra",str(self.indice_ra),"","",";")
            self.agregarTraduccion(traduccion,False)
            self.indice_ra += 1

            traduccion = TT.Traduccion("","goto "+funcion['etiqueta'],"","",";")
            self.agregarTraduccion(traduccion,False)
            
            traduccion = TT.Traduccion("",str(etiquetaFin),"","",":")
            self.agregarTraduccion(traduccion,False)

            # traduccion = TT.Traduccion("","goto finfuncion","-","",";")
            # self.agregarTraduccion(traduccion,False)
        else:
            error = Error("SEMANTICO","la funcion \'"+str(instruccion.funcion)+"\' no existe",instruccion.linea)
            gramatica.tablaerrores.agregar(error)
            print("funcion no encontrada: ",instruccion.funcion)

    def procesar_print(self,instruccion,ts,ambito):
        for index in instruccion.prints:
            valor = str(self.resolver_expresion(index.valor,ts,ambito))
            valor = valor.replace("%d","")
            valor = valor.replace("%c","")
            valor = valor.replace("%i","")
            valor = valor.replace("%s","")
            valor = valor.replace(str("\\")+str("n")," ")
            valor = valor.replace(str("\\")+str("t"),"  ")
            traduccion = TT.Traduccion("","print("+str(valor)+")","","",";")
            self.agregarTraduccion(traduccion)
        traduccion = TT.Traduccion("","print('\\n')","","",";")
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
            self.procesar_ifelse(instruccion,ts,ambito)
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
                            traduccion = TT.Traduccion(str(simbolo.referencia),str(valor),"","",";")
                        else:
                            traduccion = TT.Traduccion("",str(simbolo.referencia),"","",";")
                        self.agregarTraduccion(traduccion)
        elif isinstance(instruccion,DeclaracionStruct):
            if instruccion.struct in self.structs: #validamos si ya ha sido definido
                struct = self.structs[instruccion.struct]
                declarada = ts.obtener(str(instruccion.identificador))
                if declarada == None:
                    traduccion = TT.Traduccion("$t" + str(self.indice_temporal),"array()","","",";")
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
                            traduccion = TT.Traduccion(str(simbolo.referencia)+ "[\'"+str(i)+"\']",str(valor),"","",";")
                        else:
                            traduccion = TT.Traduccion("",str(simbolo.referencia)+ "[\'"+str(i)+"\']","","",";")
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
                    traduccion = TT.Traduccion("$t" + str(self.indice_temporal),"array()","","",";")
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
                            if traducir:
                                traduccion = TT.Traduccion(str(referencia),str(valor),"","",";")
                                self.agregarTraduccion(traduccion,False)
                        elif struct[i]['tipo'] == TS.TIPO.ARRAY:
                            print("Aun si funcionar array ")
                            # ref = i.split(",")
                            # referencia = "$t" + str(self.indice_temporal) +"["+str(indice)+"]"+ "[\'"+str(ref[0])+"\']" + str(ref[1])
                            # if traducir:
                            #     traduccion = TT.Traduccion(str(referencia),str(valor),"","",";")
                            #     self.agregarTraduccion(traduccion,False)
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
                # traduccion = referencia + "=" + "array();"
                traduccion = TT.Traduccion(str(referencia),"array()","","",";")
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
                            traduccion = TT.Traduccion("$t"+ str(self.indice_temporal)+ "[" + str(indice) +"]"+"["+str(subindice)+"]",str(valor),"","",";")
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
                        traduccion = TT.Traduccion("$t"+ str(self.indice_temporal)+ "[" + str(indice) +"]",str(valor),"","",";")
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

    def procesar_ifelse(self,instruccion,ts,ambito):
        etiquetaSalida = "salidaif"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1
        self.procesar_if(instruccion,ts,ambito,etiquetaSalida)
        for indice in instruccion.elses:
            ifelse = instruccion.elses[indice]
            self.procesar_if(ifelse,ts,ambito,etiquetaSalida)
        
        if instruccion.instrucciones_else != None:
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            etiqueta = "else"+str(self.indice_etiqueta)
            self.indice_etiqueta +=1
            self.procesar_instrucciones(instruccion.instrucciones_else,ts_local,etiqueta)
            self.indice_ambito += 1
            self.reordenar_traducciones(self.indice_ambito)
            self.indice_ambito -= 1
        
        traduccion = TT.Traduccion("",str(etiquetaSalida),"","",":")
        self.agregarTraduccion(traduccion)

    def procesar_if(self,instruccion,ts,ambito,etiquetaSalida):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        EtiquetaTrue = "if"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1

        condicion = self.resolver_expresion(instruccion.expresion,ts_local,ambito)
        traduccion = TT.Traduccion("","if("+str(condicion)+")"," goto ",str(EtiquetaTrue),";")
        self.agregarTraduccion(traduccion)
        self.indice_ambito += 1
        traduccion = TT.Traduccion("","\n"+str(EtiquetaTrue),"","",":")
        self.agregarTraduccion(traduccion)
        self.procesar_instrucciones(instruccion.instrucciones,ts_local,EtiquetaTrue)
        traduccion = TT.Traduccion("","goto "+str(etiquetaSalida),"","",";")
        self.agregarTraduccion(traduccion)
        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1

    def procesar_switch(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        etiqueta = "switch"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1
        etiquetafin = "finswitch"+str(self.indice_etiqueta)
        self.pila_control.setdefault(len(self.pila_control),str(etiquetafin))
        self.indice_etiqueta +=1
        condicion = self.resolver_expresion(instruccion.expresion,ts,etiqueta)

        traduccion = TT.Traduccion("","goto "+str(etiqueta),"","",";")
        self.agregarTraduccion(traduccion)

        traduccion = TT.Traduccion("",str(etiquetafin),"","",":")
        self.agregarTraduccion(traduccion)
        
        self.indice_ambito += 1
        
        traduccion = TT.Traduccion("","\n"+str(etiqueta),"","",":")
        self.agregarTraduccion(traduccion)

        #---------------------Procesamos todos los cases
        for case in instruccion.casos:
            if case.expresion != None:
                caso = str(condicion) +"=="+ str(self.resolver_expresion(case.expresion,ts,etiqueta))
                etiquetacase = "if"+str(self.indice_etiqueta)
                self.indice_etiqueta+=1
                traduccion = TT.Traduccion("","if("+str(caso)+")"," goto ",str(etiquetacase),";")
                self.agregarTraduccion(traduccion)
                self.indice_ambito += 1
                traduccion = TT.Traduccion("","\n"+str(etiquetacase),"","",":")
                self.agregarTraduccion(traduccion)
                self.procesar_instrucciones(case.instrucciones,ts,etiquetacase)
                traduccion = TT.Traduccion("","goto "+str(etiquetafin),"","",";")
                self.agregarTraduccion(traduccion)
                self.reordenar_traducciones(self.indice_ambito)
                self.indice_ambito -= 1
            else:
                self.procesar_instrucciones(case.instrucciones,ts,etiquetacase)
        traduccion = TT.Traduccion("","goto "+str(etiquetafin),"","",";")
        self.agregarTraduccion(traduccion)
        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1
        self.pila_control.pop(len(self.pila_control)-1)
      
    def procesar_while(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        
        etiquetawhile = "while"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1

        etiquetaSalida = "salidawhile"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1

        self.pila_control.setdefault(len(self.pila_control),str(etiquetaSalida))

        traduccion = TT.Traduccion("",etiquetawhile,"","",":")
        self.agregarTraduccion(traduccion)
        condicion = self.resolver_expresion(instruccion.expresion,ts,ambito)
        EtiquetaTrue = "whileprocesa"+str(self.indice_etiqueta)
        self.indice_etiqueta +=1
        traduccion = TT.Traduccion("","if("+str(condicion)+")"," goto ",str(EtiquetaTrue),";")
        self.agregarTraduccion(traduccion)
        self.indice_ambito += 1

        traduccion = TT.Traduccion("","\n"+str(EtiquetaTrue),"","",":")
        self.agregarTraduccion(traduccion)
        self.procesar_instrucciones(instruccion.instrucciones,ts_local,EtiquetaTrue)
        traduccion = TT.Traduccion("","goto "+str(etiquetawhile),"","",";")
        self.agregarTraduccion(traduccion)
        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1

        traduccion = TT.Traduccion("",str(etiquetaSalida),"","",":")
        self.agregarTraduccion(traduccion)
        
        self.pila_control.pop(len(self.pila_control)-1)

    def procesar_for(self,instruccion,ts,ambito):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        
        etiqueta =str("for")+str(self.indice_etiqueta)
        self.indice_etiqueta+=1

        etiquetaIngresa =str("ingresafor")+str(self.indice_etiqueta)
        self.indice_etiqueta+=1
        
        etiquetaSalida =str("salidafor")+str(self.indice_etiqueta)
        self.indice_etiqueta+=1

        self.pila_control.setdefault(len(self.pila_control),str(etiquetaSalida))

        self.procesar_instruccion(instruccion.inicializacion,ts_local,etiqueta)
        
        # traduccion = "goto "+str(etiqueta)+";"
        traduccion = TT.Traduccion("","goto "+str(etiqueta),"","",";")
        self.agregarTraduccion(traduccion)

        # traduccion =  etiquetaSalida+":"
        traduccion = TT.Traduccion("",etiquetaSalida,"","",":")
        self.agregarTraduccion(traduccion)

        self.indice_ambito += 1

        # traduccion = "\n"+str(etiqueta)+":"
        traduccion = TT.Traduccion("","\n"+str(etiqueta),"","",":")
        self.agregarTraduccion(traduccion)
        
        condicion = self.resolver_expresion(instruccion.condicion,ts_local,ambito)

        # traduccion = "if("+str(condicion)+") goto "+etiquetaIngresa +";"
        traduccion = TT.Traduccion("","if("+str(condicion)+")"," goto ",etiquetaIngresa,";")
        self.agregarTraduccion(traduccion)

        # traduccion = "goto "+str(etiquetaSalida) +";"
        traduccion = TT.Traduccion("","goto "+str(etiquetaSalida),"","",";")
        self.agregarTraduccion(traduccion)

        # traduccion = "\n"+str(etiquetaIngresa)+":"
        traduccion = TT.Traduccion("","\n"+str(etiquetaIngresa),"","",":")
        self.agregarTraduccion(traduccion)
        self.procesar_instrucciones(instruccion.instrucciones,ts,etiqueta)
        self.procesar_instruccion(instruccion.cambio,ts,etiqueta)

        # traduccion = "goto "+str(etiqueta)+";"
        traduccion = TT.Traduccion("","goto "+str(etiqueta),"","",";")
        self.agregarTraduccion(traduccion)

        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1
        # self.imprimir_tabla_traducciones(self.traducciones)
        self.pila_control.pop(len(self.pila_control)-1)

    def reordenar_traducciones(self,ambito):
        temporal = self.traducciones.copy()
        for i in reversed(temporal):
            traduccion = self.traducciones[i]
            if traduccion['ambito'] == ambito:
                self.traducciones2[len(self.traducciones2)] = self.traducciones.pop(i)

    def imprimir_tabla(self,ts):
        for i in ts.simbolos:
            simbolo = ts.simbolos[i]
            print(simbolo.id,simbolo.referencia,simbolo.ambito)

    def imprimir_tabla_traducciones(self,tt):
        for i in tt:
            print(tt[i])

    def definir_funcion(self, instruccion,ts):
        # etiqueta = str(instruccion.nombre)+str(self.indice_etiqueta)
        etiqueta = str(instruccion.nombre)
        # self.indice_etiqueta +=1
        if str(instruccion.nombre) == "main": 
            etiqueta = str(instruccion.nombre)+"0"
            self.etiqueta_princial = etiqueta
        funcion = {"nombre":instruccion.nombre,"tipo":instruccion.tipo.valor,"parametros":{},"etiqueta":etiqueta,"retorno":0}
        simbolo = TS.Simbolo(instruccion.nombre,instruccion.nombre,instruccion.tipo.valor,0,etiqueta,TS.TIPO.FUNCION)
        self.agregarSimbolo(simbolo,ts,etiqueta)
        
        if instruccion.parametros != None:
            for parametro in instruccion.parametros:
                id =parametro.identificador.identificador
                referencia = "$a"+str(self.indice_parametro)
                self.indice_parametro += 1
                simbolo = TS.Simbolo(id,referencia,instruccion.tipo.valor,0,etiqueta,TS.TIPO.VARIABLE)
                self.agregarSimbolo(simbolo,ts,instruccion.nombre)
                funcion['parametros'][len(funcion['parametros'])] = referencia
        
        if not self.traducir_general: #Bandera para indicar si estamos llenando la tabla o ejecutando
            funcion['retorno'] = "$v"+str(self.indice_retorno)
            simbolo = TS.Simbolo("$v"+str(self.indice_retorno),"$v"+str(self.indice_retorno),instruccion.tipo.valor,0,etiqueta,TS.TIPO.RETURN)
            self.agregarSimbolo(simbolo,ts,etiqueta)
            self.indice_retorno+=1
            self.funciones[funcion['nombre']] = funcion
            return
        self.funcion_actual = etiqueta
        self.indice_ambito += 1
        # traduccion = "\n"+str(etiqueta)+":"
        traduccion = TT.Traduccion("","\n"+str(etiqueta),"","",":")
        self.agregarTraduccion(traduccion)

        traduccion = TT.Traduccion("$s0["+str(self.indice_pila)+"]","$ra","","",";")
        self.agregarTraduccion(traduccion)
        
        self.indice_pila +=1

        self.procesar_instrucciones(instruccion.instrucciones,ts,etiqueta)
        
        self.funcion_actual = etiqueta
        # self.indice_pila -=1
        # if str(etiqueta)=="main":
            # traduccion = TT.Traduccion("$sp","$sp","-","1",";")
            # self.agregarTraduccion(traduccion)

        traduccion = TT.Traduccion("","return"+str(etiqueta),"","",":")
        self.agregarTraduccion(traduccion)
        traduccion = TT.Traduccion("$ra","$s0["+str(self.indice_pila-1)+"]","","",";")
        self.agregarTraduccion(traduccion)
        #Agregamos goto para el bloque de salidas
        # traduccion = "goto finfuncion;"
        traduccion = TT.Traduccion("","goto finfuncion","","",";")
        self.agregarTraduccion(traduccion)        
        
        self.reordenar_traducciones(self.indice_ambito)
        self.indice_ambito -= 1

    def procesar_asignacion(self, instruccion, ts, ambito):
        if isinstance(instruccion, AsignacionSimple):
            valor = self.resolver_expresion(instruccion.valor, ts, ambito)
            simbolo = ts.obtener(instruccion.identificador)
            if simbolo == None:
                simbolo = TS.Simbolo(instruccion.identificador, "$t"+str(self.indice_temporal), None, 0, ambito,TS.TIPO.VARIABLE)
                self.agregarSimbolo(simbolo, ts,ambito)
                # traduccion = str(simbolo.referencia)+"=0;"
                traduccion = TT.Traduccion(str(simbolo.referencia),"0","","",";")
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
                    # traduccion = referencia+"="+str(valor)+";"
                    traduccion = TT.Traduccion(str(referencia),str(valor),"","",";")
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
            # traduccion = str(simbolo.referencia)+"="+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(valor),"","",";")
        elif simbolo_asignacion == "+=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"+"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"+",str(valor),";")
        elif simbolo_asignacion == "-=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"-"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"-",str(valor),";")
        elif simbolo_asignacion == "*=":
            # simbolo.valor *= valor
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"*"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"*",str(valor),";")
        elif simbolo_asignacion == "<<=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"<<"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"<<",str(valor),";")
        elif simbolo_asignacion == ">>=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+">>"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),">>",str(valor),";")
        elif simbolo_asignacion == "&=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"&"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"&",str(valor),";")
        elif simbolo_asignacion == "^=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"^"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"^",str(valor),";")
        elif simbolo_asignacion == "|=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"|"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"|",str(valor),";")
        elif simbolo_asignacion == "/=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"/"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"/",str(valor),";")
        elif simbolo_asignacion == "%=":
            # traduccion = str(simbolo.referencia)+"=" + str(simbolo.referencia)+"%"+str(valor)+";"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"&",str(valor),";")
        self.agregarTraduccion(traduccion, False)

    def agregarSimbolo(self, simbolo, ts,ambito):
        temporal = ts.obtenerConAmbito(simbolo.id,ambito,simbolo.funcion)
        if (temporal == None):
            ts.agregar(simbolo)
            return simbolo
        return None

    def agregarTraduccion(self, traduccion, incrementar=True):
        if not self.traducir_general:
            return
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
            # traduccion = simbolo.referencia+"="+str(simbolo.referencia)+"+1;"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"+","1",";")
            self.agregarTraduccion(traduccion)
            return simbolo.referencia
        elif isinstance(exp, ExpresionDecremento):
            identificador = exp.variable
            simbolo = ts.obtener(identificador)
            # traduccion = simbolo.referencia+"="+str(simbolo.referencia)+"-1;"
            traduccion = TT.Traduccion(str(simbolo.referencia),str(simbolo.referencia),"-","1",";")
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
            referencia = "$t"+str(self.indice_temporal)
            traduccion = TT.Traduccion(str(referencia),"","-",str(valor),";")
            self.agregarTraduccion(traduccion)
            return str(referencia)
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
        elif isinstance(exp,ExpFuncion):
            self.procesar_llamada(exp,ts,ambito)
            if exp.funcion in self.funciones:
                funcion = self.funciones[exp.funcion]
                return funcion['retorno']
        elif isinstance(exp,ExpresionScanf):
                return "read()"
        return 0

    def resolver_aritmetica(self,exp,ts,ambito):
        valor1 = self.resolver_expresion(exp.expresion1,ts,ambito)
        valor2 = self.resolver_expresion(exp.expresion2,ts,ambito)
        if exp.operador == OPERACION.SUMA:
            referencia = "$t"+str(self.indice_temporal)
            # traduccion = referencia+"="+str(valor1)+"+"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"+",str(valor2),";")
        elif exp.operador == OPERACION.RESTA:
            referencia = "$t"+str(self.indice_temporal)
            # traduccion = referencia+"="+str(valor1)+"-"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"-",str(valor2),";")
        elif exp.operador == OPERACION.MULTIPLICACION:
            referencia = "$t"+str(self.indice_temporal)
            # traduccion = referencia+"="+str(valor1)+"*"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"*",str(valor2),";")
        elif exp.operador == OPERACION.DIVISION:
            referencia = "$t"+str(self.indice_temporal)
            # traduccion = referencia+"="+str(valor1)+"/"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"/",str(valor2),";")
        elif exp.operador == OPERACION.RESIDUO:
            referencia = "$t"+str(self.indice_temporal)
            # traduccion = referencia+"="+str(valor1)+"%"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"%",str(valor2),";")

        self.agregarTraduccion(traduccion)
        return str(referencia)
        
    def resolver_bit(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1,ts,ambito)
        valor2 = self.resolver_expresion(exp.expresion2,ts,ambito)

        referencia = "$t"+str(self.indice_temporal)
        if exp.operador == BIT.SHIFTIZQUIERDA:
            # traduccion = referencia+"="+str(valor1)+" << "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"<<",str(valor2),";")
        elif exp.operador == BIT.SHIFTDERECHA:
            # traduccion = referencia+"="+str(valor1)+" >> "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),">>",str(valor2),";")
        elif exp.operador == BIT.AND:
            # traduccion = referencia+"="+str(valor1)+" & "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"&",str(valor2),";")
        elif exp.operador == BIT.XOR:
            # traduccion = referencia+"="+str(valor1)+" ^ "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"^",str(valor2),";")
        elif exp.operador == BIT.OR:
            # traduccion = referencia+"="+str(valor1)+" | "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"|",str(valor2),";")
        elif exp.operador == BIT.NOT:
            # traduccion = referencia+"="+"~"+str(valor1)+";"
            traduccion = TT.Traduccion(str(referencia),"~"+str(valor1),"","",";")

        self.agregarTraduccion(traduccion)
        return str(referencia)

    def resolver_logica(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1, ts, ambito)
        valor2 = self.resolver_expresion(exp.expresion2, ts, ambito)

        referencia = "$t"+str(self.indice_temporal)
        if exp.operador == LOGICO.AND:
            # traduccion = referencia+"="+str(valor1)+" && "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"&&",str(valor2),";")
        elif exp.operador == LOGICO.OR:
            # traduccion = referencia+"="+str(valor1)+" || "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"||",str(valor2),";")
        elif exp.operador == LOGICO.XOR:
            # traduccion = referencia+"="+str(valor1)+" xor "+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"xor",str(valor2),";")
        elif exp.operador == LOGICO.NEGACION:
            # traduccion = referencia+"= !"+str(valor1)+";"
            traduccion = TT.Traduccion(str(referencia),"!"+str(valor1),"","",";")
        
        self.agregarTraduccion(traduccion)
        return str(referencia)

    def resolver_relacional(self, exp, ts, ambito):
        valor1 = self.resolver_expresion(exp.expresion1, ts, ambito)
        valor2 = self.resolver_expresion(exp.expresion2, ts, ambito)

        referencia = "$t"+str(self.indice_temporal)
        if exp.operador == RELACIONAL.COMPARACION:
            # traduccion = referencia+"="+str(valor1)+"=="+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"==",str(valor2),";")
        elif exp.operador == RELACIONAL.DIFERENTE:
            # traduccion = referencia+"="+str(valor1)+"!="+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"!=",str(valor2),";")
        elif exp.operador == RELACIONAL.MAYORIGUAL:
            # traduccion = referencia+"="+str(valor1)+">="+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),">=",str(valor2),";")
        elif exp.operador == RELACIONAL.MENORIGUAL:
            # traduccion = referencia+"="+str(valor1)+"<="+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"<=",str(valor2),";")
        elif exp.operador == RELACIONAL.MAYOR:
            # traduccion = referencia+"="+str(valor1)+">"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),">",str(valor2),";")
        elif exp.operador == RELACIONAL.MENOR:
            # traduccion = referencia+"="+str(valor1)+"<"+str(valor2)+";"
            traduccion = TT.Traduccion(str(referencia),str(valor1),"<",str(valor2),";")

        self.agregarTraduccion(traduccion)
        return str(referencia)