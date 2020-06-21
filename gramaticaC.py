#
#LUDWIN ROMARIO BURRIÓN IMUCHAC
#201314001
#
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
    'printf'    :   'PRINT',
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


def p_inicio(t):
    'inicio                     :   lista_instrucciones'
    # t[0] = t[1]

def p_lista_instrucciones(t):
    'lista_instrucciones        :   lista_instrucciones instruccion'

def p_lista_instrucciones_instruccion(t):
    'lista_instrucciones        :   instruccion'

def p_instruccion(t):
    '''instruccion              :   instruccion_funcion
                                |   declaracion_variable
                                |   definir_stuct'''

def p_definir_stuct(t):
    '''definir_stuct            :   STRUCT IDENTIFICADOR declaracion_compuesta PUNTOCOMA'''

def p_instruccion_funcion(t):
    'instruccion_funcion        :   tipo IDENTIFICADOR ABREPARENTESIS params CIERRAPARENTESIS declaracion_compuesta'

#Sin parametros
def p_instruccion_funcion_sin_params(t):
    'instruccion_funcion        :   tipo IDENTIFICADOR ABREPARENTESIS CIERRAPARENTESIS declaracion_compuesta'

def p_declaracion_compuesta(t):
    'declaracion_compuesta      :   ABRELLAVE lista_sentencias CIERRALLAVE'

def p_declaracion_compuesta_empty(t):
    'declaracion_compuesta      :   ABRELLAVE CIERRALLAVE'

def p_lista_sentencias(t):
    'lista_sentencias           :   lista_sentencias sentencia'

def p_lista_sentencias_sentencia(t):
    'lista_sentencias           :   sentencia'

def p_sentencia(t):
    '''sentencia                :   declaracion_variable
                                |   definir_stuct
                                |   declaracion_struct
                                |   sentencia_asignacion
                                |   sentencia_asignacion_struct
                                |   sentencia_while
                                |   sentencia_if
                                |   sentencia_for
                                |   sentencia_etiqueta
                                |   sentencia_goto
                                |   sentencia_switch
                                |   sentencia_break'''

def p_declaracion_variable_array(t):
    'declaracion_variable       :   tipo IDENTIFICADOR ABRECORCHETE CIERRACORCHETE PUNTOCOMA'

def p_declaracion_variable_array(t):
    'declaracion_variable       :   tipo IDENTIFICADOR indices PUNTOCOMA'

def p_multiple_declaracion(t):
    'declaracion_variable       :   tipo identificadores PUNTOCOMA'

def p_identificadores(t):
    'identificadores            :   lista_identificadores'

def p_lista_identificadores(t):
    'lista_identificadores      :   lista_identificadores COMA declaracion_identificador'

def p_lista_identificadores_identificador(t):
    'lista_identificadores      :   declaracion_identificador'

def p_declaracion_identificador(t):
    '''declaracion_identificador    :   IDENTIFICADOR
                                    |   IDENTIFICADOR IGUAL exp'''

def p_declaracion_identificador_puntero(t):
    '''declaracion_identificador    :   MUL IDENTIFICADOR
                                    |   MUL MUL IDENTIFICADOR'''     

def p_sentencia_asignacion(t):
    'sentencia_asignacion       :   IDENTIFICADOR asignacion_compuesta exp PUNTOCOMA'

def p_sentencia_asignacion_arreglo(t):
    'sentencia_asignacion       :   IDENTIFICADOR indices asignacion_compuesta exp PUNTOCOMA'

def p_sentencia_while(t):
    'sentencia_while            :   WHILE ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta'

def p_sentencia_if(t):
    'sentencia_if               :   IF ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta'

def p_sentencia_else(t):
    'sentencia_if               :   IF ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta listado_else'

def p_listado_else(t):
    'listado_else               :   listado_else  ifelse'

def p_listado_else_(t):
    'listado_else               :   ifelse'

def p_ifelse(t):
    'ifelse                     :   ELSE declaracion_compuesta'

def p_ifelse_(t):
    'ifelse                     :   ELSE IF ABREPARENTESIS exp CIERRAPARENTESIS declaracion_compuesta'

def p_sentencia_for(t):
    'sentencia_for              :   FOR ABREPARENTESIS exp PUNTOCOMA exp PUNTOCOMA exp CIERRAPARENTESIS declaracion_compuesta'

def p_declaracion_struct(t):
    'declaracion_struct         :   STRUCT IDENTIFICADOR IDENTIFICADOR PUNTOCOMA'

def p_declaracion_struct_arreglo(t):
    'declaracion_struct         :   STRUCT IDENTIFICADOR IDENTIFICADOR indices PUNTOCOMA'

def p_sentencia_asignacion_struct(t):
    'sentencia_asignacion_struct    :   IDENTIFICADOR PUNTO IDENTIFICADOR IGUAL exp PUNTOCOMA'

def p_sentencia_etiqueta(t):
    'sentencia_etiqueta         :   IDENTIFICADOR DOSPUNTOS'

def p_sentencia_goto(t):
    'sentencia_goto             :   GOTO IDENTIFICADOR PUNTOCOMA'

def p_sentencia_switch(t):
    'sentencia_switch           :   SWITCH ABREPARENTESIS exp CIERRAPARENTESIS ABRELLAVE cases CIERRALLAVE'

def p_sentencia_break(t):
    'sentencia_break            :   BREAK PUNTOCOMA'

def p_cases(t):
    'cases                      :   lista_case  default_case'

def p_cases_sin_default(t):
    'cases                      :   lista_case'

def p_cases_default(t):
    'cases                      :   default_case'

def p_lista_cases(t):
    'lista_case                 :   lista_case case'

def p_lista_case(t):
    'lista_case                 :   case'

def p_case(t):
    'case                       :   CASE exp DOSPUNTOS lista_sentencias'

def p_default_case(t):
    'default_case               :   DEFAULT DOSPUNTOS lista_sentencias'

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

def p_exp_negativo(t):
    'exp                        :   MENOS exp %prec NEGATIVO'

def p_exp_absoluto(t):
    'exp                        :   ABS ABREPARENTESIS exp CIERRAPARENTESIS %prec ABSOLUTO'

def p_exp_not(t):
    'exp                        :   NOT exp'''

def p_exp_not_bit(t):
    'exp                        :   NOTBIT exp'''

def p_exp_parentesis(t):
    'exp                        :   ABREPARENTESIS exp CIERRAPARENTESIS'

def p_exp_num(t):
    '''exp                      :   ENTERO
                                |   DECIMAL'''

def p_exp_variable(t):
    '''exp                      :   IDENTIFICADOR'''

def p_exp_puntero(t):
    '''exp                      :   AMPERSAN IDENTIFICADOR'''

def p_exp_array_index(t):
    'exp                        :   IDENTIFICADOR indices'

def p_exp_sizeof(t):
    'exp                        :   SIZEOF ABREPARENTESIS exp CIERRAPARENTESIS'

def p_exp_casteo(t):
    'exp                        :   ABREPARENTESIS tipo_variable CIERRAPARENTESIS exp'

def p_exp_funcion(t):
    'exp                        :   IDENTIFICADOR ABREPARENTESIS CIERRAPARENTESIS'

def p_exp_ternario(t):
    'exp                        :   exp TERNARIO exp DOSPUNTOS exp'

def p_exp_cadena(t):
    'exp                        :   CADENA'

def p_params(t):
    'params                     :   param_list'

def p_param_list(t):
    'param_list                 :   param_list COMA param'

def p_param_list_param(t):
    'param_list                 :   param'

def p_param(t):
    '''param                    :   tipo IDENTIFICADOR
                                |   tipo IDENTIFICADOR ABRECORCHETE CIERRACORCHETE'''

def p_indices_listado(t):
    'indices                    :   indices indice'
    # t[1].append(t[2])
    # t[0] = t[1]
    # addGramatical('indices -> indices indice')

def p_indices(t):
    'indices                    :   indice'
    # t[0] = [t[1]]
    # addGramatical('indices -> indice')

def p_indice(t):
    'indice                     :   ABRECORCHETE exp  CIERRACORCHETE'
    # t[0] = t[2]
    # addGramatical('indice -> ABRECORCHETE expresion_general CIERRACORCHETE')

def p_tipo(t):
    '''tipo                     :   INT
                                |   VOID
                                |   CHAR
                                |   DOUBLE
                                |   FLOAT'''

def p_tipo_variable(t):
    '''tipo_variable        :   INT
                            |   FLOAT
                            |   CHAR
                            |   DOUBLE'''
    # id = inc()
    # t[0] = t[1]
    # dot.node(str(id),str(t[1]))
    # addGramatical("tipo_variable -> TIPOVAR")

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

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)
    print(t.lexer.lineno)

import ply.yacc as yacc
parser = yacc.yacc()


f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)