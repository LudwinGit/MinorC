from graphviz import Graph
#
#LUDWIN ROMARIO BURRIÓN IMUCHAC
#201314001
#

i=0
def inc():
    global i
    i += 1
    return i

reservadas = {
    'auto'  :   'AUTO',
    'abs'   :   'ABS',
    'break' :   'BREAK',
    'case'  :   'CASE',
    'char'  :   'CHAR',
    'const' :   'CONST',
    'continue': 'CONTINUE',
    'default'   :   'DEFAULT',
    'do'        :   'DO',
    'double'    :   'DOUBLE',
    'else'      :   'ELSE',
    'enum'      :   'ENUM',
    'extern'    :   'EXTERN',
    'float'     :   'FLOAT',
    'for'       :   'FOR',
    'goto'      :   'GOTO',
    'if'        :   'IF',
    'int'       :   'INT',
    'register'  :   'REGISTER',
    'return'    :   'RETURN',
    'sizeof'    :   'SIZEOF',
    'struct'    :   'STRUCT',
    'switch'    :   'SWITCH',
    'void'      :   'VOID',
    'while'     :   'WHILE',
    'printf'    :   'PRINTF',
    'scanf'     :   'SCANF',
    'true'      :   'TRUE',
    'false'     :   'FALSE'
}

tokens = [
    'ENTERO','DECIMAL','CADENA',

    'IDENTIFICADOR',

    #asignaciones compuestas
    'IGUAL', 'INCREMENTO', 'DECREMENTO','MULTIPLYAND','DIVIDEAND','MODULUSAND','LEFTSHIFTAND','RIGHTSHIFTAND',
    'BITWISEAND','BITWISEEXCLUSIVE','BITWISEINCLUSIVE',

    'DOSPUNTOS','PUNTOCOMA','ABREPARENTESIS','CIERRAPARENTESIS','ABRELLAVE','CIERRALLAVE','MENOS',
    'MAS','MUL','DIV','AMPERSAN','RESIDUO','NOT','AND','OR','XOR','COMPARACION',
    'DIFERENTE','MAYORIGUAL','MENORIGUAL','MAYOR','MENOR','ABRECORCHETE','CIERRACORCHETE','COMA','PUNTO','TERNARIO',

    #bit
    'NOTBIT','ORBIT','XORBIT','SHIFTIZQ','SHIFTDER'
]+ list(reservadas.values())

t_DOSPUNTOS=            r'\:'
t_PUNTOCOMA=            r'\;'
t_IGUAL=                r'\='
t_ABREPARENTESIS =      r'\('
t_CIERRAPARENTESIS =    r'\)'
t_ABRELLAVE =           r'\{'
t_CIERRALLAVE =         r'\}'
t_MENOS =               r'\-'
t_MAS =                 r'\+'
t_MUL =                 r'\*'
t_DIV =                 r'\/'
t_RESIDUO =             r'\%'
t_AND =                 r'&&'
t_AMPERSAN =            r'&'
t_NOT =                 r'\!'
t_OR =                  r'\|\|'
t_XOR =                 r'xor'
t_COMPARACION=          r'\=\='
t_DIFERENTE=            r'\!\='
t_MAYORIGUAL=           r'\>\='
t_MENORIGUAL=           r'\<\='
t_MAYOR=                r'\>'
t_MENOR=                r'\<'
t_ABRECORCHETE=         r'\['
t_CIERRACORCHETE=       r'\]'
t_COMA=                 r'\,'
t_PUNTO=                r'\.'
t_INCREMENTO=           r'\+\='
t_DECREMENTO=           r'\-\='
t_MULTIPLYAND=          r'\*\='
t_DIVIDEAND=            r'\/\='
t_MODULUSAND=           r'\%\='
t_LEFTSHIFTAND=         r'\<\<\='
t_RIGHTSHIFTAND=        r'\>\>\='
t_BITWISEAND=           r'\&\='
t_BITWISEEXCLUSIVE=     r'\^\='
t_BITWISEINCLUSIVE=     r'\|\='
t_NOTBIT=               r'\~'
t_ORBIT=                r'\|'
t_XORBIT=               r'\^'
t_SHIFTIZQ=             r'\<\<'
t_SHIFTDER=             r'\>\>'
t_TERNARIO=             r'\?'
# Caracteres ignorados
t_ignore = " \t"

def t_CADENA(t):
    r'\'.*?\'|\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_IDENTIFICADOR(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'IDENTIFICADOR')    # Check for reserved words
     return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("DEMASIADO GRANDER PARA CONVERTIR A FLOAT %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("DEMASIADO GRANDE PARA CONVERTIR A INT %d", t.value)
        t.value = 0
    return t

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Caracter no reconocido '%s'" % t.value[0])
    # error = Error("LEXICO","Caracter no reconocido '%s'" % t.value[0],t.lexer.lineno)
    # errores.agregar(error)
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','ABSOLUTO'),
    ('left','MAS','MENOS'),
    ('left','MUL','DIV'),
    ('right','NEGATIVO'),
    )

from instrucciones import *
from expresiones import *

def p_inicio(t):
    'inicio                     :   lista_instrucciones'
    id =  inc()
    t[0] = t[1]
    dot.node(str(id),"Inicio")
    for item in t[1]:
        dot.edge(str(id),str(item.id_dot))

def p_lista_instrucciones(t):
    'lista_instrucciones        :   lista_instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_lista_instrucciones_instruccion(t):
    'lista_instrucciones        :   instruccion'
    t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion              :   instruccion_funcion
                                |   declaracion_variable
                                |   definir_struct'''
    t[0] = t[1]

def p_definir_struct(t):
    '''definir_struct            :   STRUCT IDENTIFICADOR declaracion_compuesta PUNTOCOMA'''
    id = inc()
    t[0] = Struct(id,t.lexer.lineno,t[2],t[3])
    dot.node(str(id),"Struct: "+str(t[2]))
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot))

def p_instruccion_funcion_con_params(t):
    'instruccion_funcion        :   tipo IDENTIFICADOR ABREPARENTESIS params CIERRAPARENTESIS declaracion_compuesta'
    id = inc()
    t[0] = Funcion(id,t.lexer.lineno,t[1],str(t[2]),t[6],t[4].valor)
    dot.node(str(id),"Función: "+str(t[2]))
    dot.edge(str(id),str(t[1].id_dot))
    dot.edge(str(id),str(t[4].id_dot))
    for item in t[6]:
        dot.edge(str(id),str(item.id_dot))

#Sin parametros
def p_instruccion_funcion_sin_params(t):
    'instruccion_funcion        :   tipo IDENTIFICADOR ABREPARENTESIS CIERRAPARENTESIS declaracion_compuesta'
    id = inc()
    t[0] = Funcion(id,t.lexer.lineno,t[1],str(t[2]),t[5])
    dot.node(str(id),"Función: "+str(t[2]))
    dot.edge(str(id),str(t[1].id_dot))
    for item in t[5]:
        dot.edge(str(id),str(item.id_dot))

def p_declaracion_compuesta(t):
    'declaracion_compuesta      :   ABRELLAVE lista_sentencias CIERRALLAVE'
    t[0] = t[2]

def p_declaracion_compuesta_empty(t):
    'declaracion_compuesta      :   ABRELLAVE CIERRALLAVE'
    t[0] = []

def p_lista_sentencias(t):
    'lista_sentencias           :   lista_sentencias sentencia'
    t[1].append(t[2])
    t[0] = t[1]

def p_lista_sentencias_sentencia(t):
    'lista_sentencias           :   sentencia'
    t[0] = [t[1]]

def p_sentencia(t):
    '''sentencia                :   declaracion_variable
                                |   definir_struct
                                |   declaracion_struct
                                |   sentencia_asignacion PUNTOCOMA
                                |   sentencia_asignacion_struct
                                |   sentencia_while
                                |   sentencia_dowhile
                                |   sentencia_if
                                |   sentencia_for
                                |   sentencia_etiqueta
                                |   sentencia_goto
                                |   sentencia_switch
                                |   sentencia_break
                                |   sentencia_continue
                                |   sentencia_return
                                |   sentencia_print
                                '''
    t[0] = t[1]

# def p_declaracion_variable_array(t):
#     'declaracion_variable       :   tipo IDENTIFICADOR ABRECORCHETE CIERRACORCHETE PUNTOCOMA'

def p_declaracion_variable_array(t):
    'declaracion_variable       :   tipo IDENTIFICADOR indices PUNTOCOMA'
    id = inc()
    t[0] = DeclaracionArray(id,t.lexer.lineno,t[1].valor,t[2],t[3])
    dot.node(str(id),"Declaración array:")
    dot.edge(str(id),str(t[2]),"tipo")
    dot.edge(str(id),str(t[1].id_dot),"variable")
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot),"indice")

def p_declaracion_variable_array(t):
    'declaracion_variable       :   tipo IDENTIFICADOR indices IGUAL exp PUNTOCOMA'
    id = inc()
    t[0] = DeclaracionArray(id,t.lexer.lineno,t[1].valor,t[2],t[3],t[5])
    dot.node(str(id),"Declaración array:")
    dot.edge(str(id),str(t[2]),"tipo")
    dot.edge(str(id),str(t[1].id_dot),"variable")
    dot.edge(str(id),str(t[5].id_dot),"valor")
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot),"indice")

def p_declaracion_variable_array_inicializado(t):
    'declaracion_variable       :   tipo IDENTIFICADOR indices IGUAL ABRELLAVE lista_expresiones CIERRALLAVE PUNTOCOMA'
    print(3)
    id = inc()
    t[0] = DeclaracionArray(id,t.lexer.lineno,t[1].valor,t[2],t[3],t[6])
    dot.node(str(id),"Declaración array:")
    dot.edge(str(id),str(t[2]),"variable")
    dot.edge(str(id),str(t[1].id_dot),"tipo")
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot),"indice")
    for item in t[6]:
        dot.edge(str(id),str(item.id_dot),"valor")

def p_multiple_declaracion(t):
    'declaracion_variable       :   tipo identificadores PUNTOCOMA'
    id = inc()
    t[0] = Declaracion(id,t.lexer.lineno,t[1].valor,t[2])
    dot.node(str(id),"Declaración")
    dot.edge(str(id),str(t[1].id_dot))
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))

def p_identificadores(t):
    'identificadores            :   lista_identificadores'
    t[0] = t[1]

def p_lista_identificadores(t):
    'lista_identificadores      :   lista_identificadores COMA declaracion_identificador'
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_identificadores_identificador(t):
    'lista_identificadores      :   declaracion_identificador'
    t[0] = [t[1]]

def p_declaracion_identificador(t):
    'declaracion_identificador    :   IDENTIFICADOR'
    id = inc()
    t[0] = Variable(id,t.lexer.lineno,str(t[1]))
    dot.node(str(id),str(t[1]))

def p_declaracion_identificador_inicializado(t):
    'declaracion_identificador    :   IDENTIFICADOR IGUAL exp'
    id = inc()
    t[0] = Variable(id,t.lexer.lineno,str(t[1]),t[3])
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[3].id_dot))

def p_declaracion_identificador_puntero(t):
    '''declaracion_identificador    :   MUL IDENTIFICADOR
                                    |   MUL MUL IDENTIFICADOR'''     

def p_sentencia_asignacion(t):
    'sentencia_asignacion       :   IDENTIFICADOR asignacion_compuesta exp'
    id = inc()
    t[0] = Asignacion(id,t.lexer.lineno,t[1],t[2].valor,t[3])
    dot.node(str(id),"Asignación: "+str(t[1]))
    dot.edge(str(id),str(t[2].id_dot))
    dot.edge(str(id),str(t[3].id_dot))

def p_sentencia_asignacion_arreglo(t):
    'sentencia_asignacion       :   IDENTIFICADOR indices asignacion_compuesta exp'
    id = inc()
    t[0] = AsignacionArray(id,t.lexer.lineno,t[1],t[3].valor,t[2],t[4])
    dot.node(str(id),"Asignación Array")
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))
    dot.edge(str(id),str(t[3].id_dot))
    dot.edge(str(id),str(t[4].id_dot))

def p_sentencia_while(t):
    'sentencia_while            :   WHILE ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta'
    id = inc()
    t[0] = While(id,t.lexer.lineno,t[3],t[5])
    dot.node(str(id),"While")
    dot.edge(str(id),str(t[3].id_dot))
    for item in t[5]:
        dot.edge(str(id),str(item.id_dot))

def p_sentencia_dowhile(t):
    'sentencia_dowhile          :   DO declaracion_compuesta WHILE ABREPARENTESIS exp CIERRAPARENTESIS PUNTOCOMA'
    id = inc()
    t[0] = DoWhile(id,t.lexer.lineno,t[5],t[2])
    dot.node(str(id),"Do while")
    dot.edge(str(id),str(t[5].id_dot))
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))

def p_sentencia_if(t):
    'sentencia_if               :   IF ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta'
    id = inc()
    t[0] = If(id,t.lexer.lineno,t[3],t[5])
    dot.node(str(id),"IF")
    dot.edge(str(id),str(t[3].id_dot))
    for item in t[5]:
        dot.edge(str(id),str(item.id_dot))

def p_sentencia_else(t):
    'sentencia_if               :   IF ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta listado_else'
    id = inc()
    t[6].append(If(id,t.lexer.lineno,t[3],t[5]))
    dot.node(str(id),"IF")
    dot.edge(str(id),str(t[3].id_dot))
    for item in t[5]:
        dot.edge(str(id),str(item.id_dot))

    id = inc()
    t[0] = Ifelse(id,t.lexer.lineno,t[6])
    dot.node(str(id),"IF-ELSE")
    for item in t[6]:
        dot.edge(str(id),str(item.id_dot))

def p_listado_else(t):
    'listado_else               :   listado_else  ifelse'
    t[1].append(t[2])
    t[0] = t[1]

def p_listado_else_(t):
    'listado_else               :   ifelse'
    t[0] = [t[1]]

def p_ifelse(t):
    'ifelse                     :   ELSE declaracion_compuesta'
    id = inc()
    t[0] = If(id,t.lexer.lineno,None,t[2])
    dot.node(str(id),"Else")
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))

def p_ifelse_(t):
    'ifelse                     :   ELSE IF ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta'
    id = inc()
    t[0] = If(id,t.lexer.lineno,t[4],t[6])
    dot.node(str(id),"Else If")
    dot.edge(str(id),str(t[4].id_dot))
    for item in t[6]:
        dot.edge(str(id),str(item.id_dot))

def p_sentencia_for(t):
    'sentencia_for              :   FOR ABREPARENTESIS sentencia exp PUNTOCOMA sentencia_asignacion CIERRAPARENTESIS declaracion_compuesta'
    id = inc()
    t[0] = For(id,t.lexer.lineno,t[3],t[4],t[6],t[8])
    dot.node(str(id),"For")
    dot.edge(str(id),str(t[3].id_dot))
    dot.edge(str(id),str(t[4].id_dot))
    dot.edge(str(id),str(t[6].id_dot))
    for item in t[8]:
        dot.edge(str(id),str(item.id_dot))


def p_declaracion_struct(t):
    'declaracion_struct         :   STRUCT IDENTIFICADOR IDENTIFICADOR PUNTOCOMA'
    id = inc()
    t[0] = DeclaracionStruct(id,t.lexer.lineno,t[3],t[2])
    dot.node(str(id),"Asignacion Struct")
    dot.edge(str(id),str(t[2]))
    dot.edge(str(id),str(t[3]))

def p_declaracion_struct_arreglo(t):
    'declaracion_struct         :   STRUCT IDENTIFICADOR IDENTIFICADOR indices PUNTOCOMA'
    id = inc()
    t[0] = DeclaracionStructArray(id,t.lexer.lineno,t[3],t[2],t[4])
    dot.node(str(id),"Asignacion Struct")
    dot.edge(str(id),str(t[2]))
    dot.edge(str(id),str(t[3]))
    for item in t[4]:
        dot.edge(str(id),str(item.id_dot))

def p_sentencia_asignacion_struct(t):
    'sentencia_asignacion_struct    :   IDENTIFICADOR PUNTO IDENTIFICADOR asignacion_compuesta exp PUNTOCOMA'
    id   = inc()
    t[0] = AsignacionStruct(id,t.lexer.lineno,t[1],t[3],t[4],t[5])
    dot.edge(str(id),str(t[5].id_dot),"valor")
    dot.edge(str(id),str(t[4].id_dot))
    dot.node(str(id),"Asignacion struct")
    dot.edge(str(id),"["+str(id)+"]"+str(t[1])+"."+str(t[3]),"variable")

def p_sentencia_asignacion_struct_arreglo(t):
    'sentencia_asignacion_struct    :   IDENTIFICADOR indices PUNTO IDENTIFICADOR asignacion_compuesta exp PUNTOCOMA'
    id   = inc()
    t[0] = AsignacionStruct(id,t.lexer.lineno,t[1],t[4],t[5],t[6],t[2])
    dot.edge(str(id),str(t[6].id_dot),"valor")
    dot.edge(str(id),str(t[5].id_dot))
    dot.node(str(id),"Asignacion struct")
    dot.edge(str(id),"["+str(id)+"]"+str(t[1])+"."+str(t[4]),"variable")
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot),"indice")

def p_sentencia_etiqueta(t):
    'sentencia_etiqueta         :   IDENTIFICADOR DOSPUNTOS'
    id = inc()
    t[0] = Etiqueta(id,t.lexer.lineno,t[1])
    dot.node(str(id),"Etiqueta: "+str(t[1]))

def p_sentencia_goto(t):
    'sentencia_goto             :   GOTO IDENTIFICADOR PUNTOCOMA'

def p_sentencia_switch(t):
    'sentencia_switch           :   SWITCH ABREPARENTESIS exp CIERRAPARENTESIS ABRELLAVE cases CIERRALLAVE'
    id = inc()
    t[0] = Switch(id,t.lexer.lineno,t[3],t[6])
    dot.node(str(id),"Switch")
    for item in t[6]:
        dot.edge(str(id),str(item.id_dot))

def p_sentencia_break(t):
    'sentencia_break            :   BREAK PUNTOCOMA'
    id = inc()
    t[0] = Break(id,t.lexer.lineno)
    dot.node(str(id),"Break")

def p_sentencia_continue(t):
    'sentencia_continue         :   CONTINUE PUNTOCOMA'

def p_sentencia_return(t):
    'sentencia_return           :   RETURN exp PUNTOCOMA'
    id = inc()
    t[0] = Return(id,t.lexer.lineno,t[2])
    dot.node(str(id),"Return")
    dot.edge(str(id),str(t[2].id_dot))

def p_sentencia_print(t):
    'sentencia_print            :   PRINTF ABREPARENTESIS prints CIERRAPARENTESIS PUNTOCOMA'
    id = inc()
    t[0] = Print(id,t.lexer.lineno,t[3])
    dot.node(str(id),"Print")
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot))

def p_prints(t):
    'prints                     :   print_list'
    t[0] = t[1]

def p_print_list(t):
    'print_list                 :   print_list COMA print'
    t[1].append(t[3])
    t[0] = t[1]

def p_print_list_print(t):
    'print_list                 :   print'
    t[0] = [t[1]]

def p_print(t):
    '''print                    :   exp'''
    id = inc()
    t[0] = Valor(id,t[1])
    dot.node(str(id),"Valor")
    dot.edge(str(id),str(t[1].id_dot))

def p_cases_con_default(t):
    'cases                      :   lista_case  default_case'
    t[1].append(t[2])
    t[0] = t[1]

def p_cases_sin_default(t):
    'cases                      :   lista_case'
    t[0] = t[1]

def p_cases_default(t):
    'cases                      :   default_case'
    t[0] = [t[1]]

def p_lista_cases(t):
    'lista_case                 :   lista_case case'
    t[1].append(t[2])
    t[0] = t[1]

def p_lista_case(t):
    'lista_case                 :   case'
    t[0] = [t[1]]

def p_case(t):
    'case                       :   CASE exp DOSPUNTOS lista_sentencias'
    id = inc()
    t[0] = Case(id,t.lexer.lineno,t[2],t[4])
    dot.node(str(id),"Case")
    dot.edge(str(id),str(t[2].id_dot))
    for item in t[4]:
        dot.edge(str(id),str(item.id_dot))

def p_default_case(t):
    'default_case               :   DEFAULT DOSPUNTOS lista_sentencias'
    id = inc()
    t[0] = Case(id,t.lexer.lineno,None,t[3])
    dot.node(str(id),"Default")
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot))

def p_exp(t):
    '''exp                      :   exp MAS         exp
                                |   exp MENOS       exp
                                |   exp MUL         exp
                                |   exp DIV         exp
                                |   exp RESIDUO     exp
                                |   exp AND         exp
                                |   exp OR          exp
                                |   exp XOR         exp
                                |   exp COMPARACION exp
                                |   exp DIFERENTE   exp
                                |   exp MAYORIGUAL  exp
                                |   exp MENORIGUAL  exp
                                |   exp MAYOR       exp
                                |   exp MENOR       exp
                                |   exp AMPERSAN    exp
                                |   exp ORBIT       exp
                                |   exp XORBIT      exp
                                |   exp SHIFTIZQ    exp
                                |   exp SHIFTDER    exp
                                '''
    id = inc()
    #Aritmeticas
    if t[2] == "+":
        t[0] = ExpresionAritmetica(id,t.lexer.lineno,t[1],OPERACION.SUMA,t[3])
    elif t[2] == "-":
        t[0] = ExpresionAritmetica(id,t.lexer.lineno,t[1],OPERACION.RESTA,t[3])
    elif t[2] == "*":
        t[0] = ExpresionAritmetica(id,t.lexer.lineno,t[1],OPERACION.MULTIPLICACION,t[3])
    elif t[2] == "/":
        t[0] = ExpresionAritmetica(id,t.lexer.lineno,t[1],OPERACION.DIVISION,t[3])    
    elif t[2] == "%":
        t[0] = ExpresionAritmetica(id,t.lexer.lineno,t[1],OPERACION.RESIDUO,t[3])

    #Logicas
    elif t[2] == "&&":
        t[0] = ExpresionLogica(id,t.lexer.lineno,t[1],LOGICO.AND,t[3])
    elif t[2] == "||":
        t[0] = ExpresionLogica(id,t.lexer.lineno,t[1],LOGICO.OR,t[3])
    elif t[2] == "xor":
        t[0] = ExpresionLogica(id,t.lexer.lineno,t[1],LOGICO.XOR,t[3])
    
    #Relacionales
    elif t[2] == "==":
        t[0] = ExpresionRelacional(id,t.lexer.lineno,t[1],RELACIONAL.COMPARACION,t[3])
    elif t[2] == "!=":
        t[0] = ExpresionRelacional(id,t.lexer.lineno,t[1],RELACIONAL.DIFERENTE,t[3])
    elif t[2] == ">=":
        t[0] = ExpresionRelacional(id,t.lexer.lineno,t[1],RELACIONAL.MAYORIGUAL,t[3])
    elif t[2] == "<=":
        t[0] = ExpresionRelacional(id,t.lexer.lineno,t[1],RELACIONAL.MENORIGUAL,t[3])
    elif t[2] == ">":
        t[0] = ExpresionRelacional(id,t.lexer.lineno,t[1],RELACIONAL.MAYOR,t[3])
    elif t[2] == "<":
        t[0] = ExpresionRelacional(id,t.lexer.lineno,t[1],RELACIONAL.MENOR,t[3])

    #Bit a Bit
    elif t[2] == "&":
        t[0] = ExpresionBit(id,t.lexer.lineno,t[1],BIT.AND,t[3])
    elif t[2] == "|":
        t[0] = ExpresionBit(id,t.lexer.lineno,t[1],BIT.OR,t[3])
    elif t[2] == "^":
        t[0] = ExpresionBit(id,t.lexer.lineno,t[1],BIT.XOR,t[3])
    elif t[2] == "<<":
        t[0] = ExpresionBit(id,t.lexer.lineno,t[1],BIT.SHIFTIZQUIERDA,t[3])
    elif t[2] == ">>":
        t[0] = ExpresionBit(id,t.lexer.lineno,t[1],BIT.SHIFTDERECHA,t[3])

    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),str(t[2]))
    dot.edge(str(id),str(t[3].id_dot))

def p_exp_negativo(t):
    'exp                        :   MENOS exp %prec NEGATIVO'
    id = inc()
    t[0] = ExpresionNegativo(id,t.lexer.lineno,t[2])
    dot.node(str(id),str("-"))
    dot.edge(str(id),str(t[2].id_dot))

def p_exp_absoluto(t):
    'exp                        :   ABS ABREPARENTESIS exp CIERRAPARENTESIS %prec ABSOLUTO'
    id = inc()
    t[0] = ExpresionAbsoluto(id,t.lexer.lineno,t[3])
    dot.node(str(id),str("ABS"))
    dot.edge(str(id),str(t[3].id_dot))

def p_exp_not(t):
    'exp                        :   NOT exp'''
    id = inc()
    t[0] = ExpresionLogica(id,t.lexer.lineno,t[2],LOGICO.AND,None)
    dot.node(str(id),"Not")
    dot.edge(str(id),str(t[2].id_dot))

def p_exp_not_bit(t):
    'exp                        :   NOTBIT exp'''
    id = inc()
    t[0] = ExpresionBit(id,t.lexer.lineno,t[2],BIT.NOT,None)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[2].id_dot))

def p_exp_parentesis(t):
    'exp                        :   ABREPARENTESIS exp CIERRAPARENTESIS'

def p_exp_num(t):
    '''exp                      :   ENTERO
                                |   DECIMAL'''
    id = inc()
    t[0] = ExpNum(id,t.lexer.lineno,t[1])
    dot.node(str(id),str(t[1]))

def p_exp_variable(t):
    '''exp                      :   IDENTIFICADOR'''
    id = inc()
    t[0] = ExpIdentificador(id,t.lexer.lineno,t[1])
    dot.node(str(id),t[1])

def p_exp_puntero(t):
    '''exp                      :   AMPERSAN IDENTIFICADOR'''
    id = inc()
    t[0] = ExpresionPuntero(id,t.lexer.lineno,t[2])
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[2]))

def p_exp_array_index(t):
    'exp                        :   IDENTIFICADOR indices'
    id = inc()
    t[0] = ExpArray(id,t.lexer.lineno,t[1],t[2])
    dot.node(str(id),"Array: "+str(t[1]))
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))

def p_exp_sizeof(t):
    'exp                        :   SIZEOF ABREPARENTESIS exp CIERRAPARENTESIS'

def p_exp_casteo(t):
    'exp                        :   ABREPARENTESIS tipo_variable CIERRAPARENTESIS exp'

def p_exp_funcion(t):
    'exp                        :   IDENTIFICADOR ABREPARENTESIS CIERRAPARENTESIS'

def p_exp_funcion_con_parametros(t):
    'exp                        :   IDENTIFICADOR ABREPARENTESIS params CIERRAPARENTESIS'
    id = inc()
    t[0] = ExpFuncion(id,t.lexer.lineno,t[1],t[3])
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[3].id_dot))

def p_exp_ternario(t):
    'exp                        :   exp TERNARIO exp DOSPUNTOS exp'

def p_exp_cadena(t):
    'exp                        :   CADENA'
    id = inc()
    t[0] = ExpresionCadena(id,t.lexer.lineno,t[1])
    dot.node(str(id),str(t[1]))

def p_exp_struct(t):
    'exp                        :   IDENTIFICADOR PUNTO IDENTIFICADOR'
    id = inc()
    t[0] = ExpresionStruct(id,t.lexer.lineno,t[1],t[3])
    dot.node(str(id),str(t[1])+"."+str(t[3]))

def p_exp_struct_arreglo(t):
    'exp                        :   IDENTIFICADOR indices PUNTO IDENTIFICADOR'
    id = inc()
    t[0] = ExpresionStruct(id,t.lexer.lineno,t[1],t[4],t[2])
    dot.node(str(id),str(t[1])+"."+str(t[4]))
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot),"indice")

def p_params(t):
    'params                     :   param_list'
    id = inc()
    t[0] = Valor(id,t[1])
    dot.node(str(id),"Parametros")
    for item in t[1]:
        dot.edge(str(id),str(item.id_dot))

def p_param_list(t):
    'param_list                 :   param_list COMA param'
    t[1].append(t[3])
    t[0] = t[1]

def p_param_list_param(t):
    'param_list                 :   param'
    t[0] = [t[1]]

def p_param(t):
    '''param                    :   exp'''
    id = inc()
    t[0] = Parametro(id,t.lexer.lineno,t[1])
    dot.node(str(id),"Parametro")
    dot.edge(str(id),str(t[1].id_dot))

def p_param_tipo(t):
    'param                      :   tipo exp'
    id = inc()
    t[0] = Parametro(id,t.lexer.lineno,t[2],t[1])
    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),"Parametro")
    dot.edge(str(id),str(t[2].id_dot))


# def p_param(t):
#     '''param                    :   tipo IDENTIFICADOR
#                                 |   IDENTIFICADOR
#                                 |   tipo IDENTIFICADOR ABRECORCHETE CIERRACORCHETE
#                                 |   exp'''
#     t[0] = t[1]
def p_lista_expresiones(t):
    'lista_expresiones          :   lista_expresiones COMA exp'
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_expresiones_expresion(t):
    'lista_expresiones                :   exp'
    t[0] = [t[1]]

def p_indices_listado(t):
    'indices                    :   indices indice'
    t[1].append(t[2])
    t[0] = t[1]
    # addGramatical('indices -> indices indice')

def p_indices(t):
    'indices                    :   indice'
    t[0] = [t[1]]
    # addGramatical('indices -> indice')

def p_indice(t):
    'indice                     :   ABRECORCHETE exp  CIERRACORCHETE'
    t[0] = t[2]
    # addGramatical('indice -> ABRECORCHETE expresion_general CIERRACORCHETE')

def p_indice_empty(t):
    'indice                     :   ABRECORCHETE CIERRACORCHETE'
    id = inc()
    t[0] = Valor(id,"Vacío")

def p_tipo(t):
    '''tipo                     :   INT
                                |   VOID
                                |   CHAR
                                |   DOUBLE
                                |   FLOAT
                                |   IDENTIFICADOR'''
    id = inc()
    t[0] = Valor(id,t[1])
    dot.node(str(id),str(t[1]))


#Uso para castear
def p_tipo_variable(t):
    '''tipo_variable        :   INT
                            |   FLOAT
                            |   CHAR
                            |   DOUBLE'''

def p_asignacion_compuesta(t):
    '''asignacion_compuesta     :   IGUAL
                                |   INCREMENTO
                                |   DECREMENTO
                                |   MULTIPLYAND
                                |   DIVIDEAND
                                |   MODULUSAND
                                |   LEFTSHIFTAND
                                |   RIGHTSHIFTAND
                                |   BITWISEAND
                                |   BITWISEEXCLUSIVE
                                |   BITWISEINCLUSIVE'''
    id = inc()
    t[0] = Valor(id,t[1]) 
    dot.node(str(id),str(t[1]))

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)
    print(t.lexer.lineno)

import ply.yacc as yacc
parser = yacc.yacc()

dot = Graph()
dot.attr(splines="false")
dot.node_attr.update(shape='circle')
dot.edge_attr.update(color="blue4")

# print(input)
# g = parser.parse(input)
# print(g)

def parse(input):
    dot.clear()
    resultado = parser.parse(input)
    return resultado