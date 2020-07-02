

from errores import *

lisErr=TablaError([])

reservadas = {
    'goto'  : 'GOTO',
    'unset' : 'UNSET',
    'print' : 'PRINT',
    'read'  : 'READ',
    'exit'  : 'EXIT',
    'int'   : 'INT',
    'float' : 'FLOAT',
    'char'  : 'CHAR',
    'abs'   : 'ABS',
    'xor'   : 'XOR',
    'array' : 'ARRAY',
    'if'    : 'IF'
}

tokens  = [
    'MAS',
    'MENOS',
    'MULTI',
    'DIVISION',
    'RESIDUO',
    'IGUAL',
    'PARIZQ',
    'PARDER',
    'PTCOMA',
    'NOT',
    'AND',
    'OR',
    'NOTBB',
    'ANDBB',
    'ORBB',
    'XORBB',
    'SHIFTIZQ',
    'SHIFTDER',
    'IGUALQUE',
    'DISTINTO',
    'MAYORIG',
    'MENORIG',
    'MAYORQUE',
    'MENORQUE',
    'CORIZQ',
    'CORDER',
    'TEMPVAR',
    'PARAM',
    'FUNVAL',
    'RA',
    'STACK',
    'SP',
    'DOSPTS',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CADENADOBLE',
    'ID'
] + list(reservadas.values())

# Tokens
t_MAS       = r'\+'
t_MENOS     = r'-'
t_MULTI     = r'\*'
t_DIVISION  = r'/'
t_RESIDUO   = r'%'
t_IGUAL     = r'='
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_PTCOMA    = r';'
t_NOT       = r'!'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOTBB     = r'~'
t_ANDBB     = r'&'
t_ORBB      = r'\|'
t_XORBB     = r'\^'
t_SHIFTIZQ  = r'<<'
t_SHIFTDER  = r'>>'
t_IGUALQUE  = r'=='
t_DISTINTO  = r'!='
t_MAYORIG   = r'>='
t_MENORIG   = r'<='
t_MAYORQUE  = r'>'
t_MENORQUE  = r'<'
t_CORIZQ    = r'\['
t_CORDER    = r']'
t_TEMPVAR   = r'[$]t\d+' 
t_PARAM     = r'[$]a\d+'
t_FUNVAL    = r'[$]v\d+'
t_RA        = r'[$]ra'
t_STACK     = r'[$]s\d+'
t_SP        = r'[$]sp'
t_DOSPTS    = r':'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1]
    return t 

def t_CADENADOBLE(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t 

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_COMENTARIO(t):
    r'\#.*\n'
    t.lexer.lineno += 1

    
def t_error(t):
    print("Caracter NO Valido: '%s'" % t.value[0])
    t.lexer.skip(1)
    nErr=ErrorRep('Lexico','Caracter NO Valido %s' % t.value[0],t.lexer.lineno)
    lisErr.agregar(nErr)

#-----------------------
import ply.lex as lex
lexer = lex.lex()
#-----------------------


#-------------------------------
from expresiones import *
from instrucciones import *
cadena=''

def p_init(t) :
    'init : in_instrucciones'
    t[0] = t[1]

def p_in_instrucciones(t) :
    'in_instrucciones : instruccion instrucciones'
    t[1].extend(t[2])
    t[0]=t[1]
    concat('<TR><TD> in_instrucciones → instruccion instrucciones </TD><TD> t[1].extend(t[2]) <BR/> t[0]=t[1] </TD></TR>')
    

def p_instrucciones_lista(t) :
    'instrucciones    : instruccion instrucciones'
    t[1].extend(t[2])
    t[0] = t[1]
    concat('<TR><TD> instrucciones → instruccion instrucciones </TD><TD> t[1].extend(t[2]) <BR/> t[0]=t[1] </TD></TR>')
    

def p_instrucciones_empty(t) :
    'instrucciones    :  '
    t[0] = []
    concat('\n <TR><TD> instrucciones → empty </TD><TD> t[0]=[] </TD></TR>')


def p_empty(t) :
    'empty : '
    pass

def p_instr_error(t) :
    'instruccion  :   error'
    t[0] = []

def p_instruccion(t) :
    '''instruccion      : asignacion_heredada
                        | print_instr
                        | goto_instr
                        | unset_instr
                        | exit_instr
                        | def_etiqueta_instr
                        | if_instr'''
    t[0] = [t[1]]
    ##concat('\n <TR><TD> instruccion = '+str(t[1].)+' </TD><TD> instrucciones=t[1] </TD></TR>')

def p_def_etiqueta_vacia(t) :
    '''def_etiqueta_instr   : ID DOSPTS'''
    t[0] = Etiqueta(t[1])
    concat('<TR> \n <TD>def_etiqueta_instr → '+str(t[1])+' : </TD> \n <TD>  t[0]=Etiqueta(t[1]) </TD> \n </TR> \n')


def p_asignacion_heredada(t) :
    'asignacion_heredada : tipo_variable lista_asignaciones'
    t[0]=t[2]
    concat('<TR> \n <TD>asignacion_heredada → '+str(t[1].id)+' lista_asignaciones </TD> \n <TD>  t[0]=t[2] </TD> \n </TR> \n')


def p_lista_asignaciones(t) :
    '''lista_asignaciones :  IGUAL asignacion_valor'''
    t[0] = t[2]
    concat('<TR> \n <TD>lista_asignaciones → = asignacion_valor  </TD> \n <TD>  t[0]=t[2] </TD> \n </TR> \n')

def p_lista_asignacion_arr(t) :
    '''lista_asignaciones :  asignacion_arr_st'''
    t[0] = t[1]
    concat('<TR> \n <TD>lista_asignaciones → = asignacion_arr_st  </TD> \n <TD>  t[0]=t[1] </TD> \n </TR> \n')

def p_asignacion_valor(t) :
    'asignacion_valor   :   expresion PTCOMA'
    t[0] = Asignacion(t[-2],t[1])
    concat('\n <TR><TD> asignacion_valor → expresion ;  </TD><TD> t[0]=Asignacion(t[-2],t[1]) '+str(t[-2].id)+'</TD></TR>')

def p_dec_array_instr(t) :
    'asignacion_valor   : ARRAY PARIZQ PARDER PTCOMA'
    t[0] = Array(t[-2])
    concat('\n <TR><TD> asignacion_valor → Array() ; </TD><TD>t[0]=Array(t[-2]) '+str(t[-2].id)+' </TD> </TR> ')


def p_asignacion_arr_St(t) :
    'asignacion_arr_st   : def_par lista_parametros  IGUAL expresion PTCOMA'
    t[1].extend(t[2])
    t[0] = AsignacionArrSt(t[-1],t[1],t[4])
    concat('\n <TR><TD> asignacion_arr_st → def_par lista_parametros =  expresion ; </TD><TD> t[0] = AsignacionArrSt(t[-1],t[2],t[4]) </TD> </TR> ')

def p_asignacion_arr_err(t):
    'asignacion_arr_st   :  def_par lista_parametros error PTCOMA'
    print("Error sintáctico en '%s'" % (t[3]))
    nErr=ErrorRep('Sintactico','Error de sintaxis en asignacion arreglo '+str(t[3].value),t[3].lineno)
    lisErr.agregar(nErr)

def p_lista_parametros(t) :
    'lista_parametros    : def_par lista_parametros'
    t[1].extend(t[2])
    t[0] = t[1]

    concat('\n <TR><TD> lista_parametros → def_par lista_parametros </TD><TD> t[1].append(t[2]) <BR/> t[0] = t[1] </TD> </TR> ')

def p_parametro(t) :
    'lista_parametros : ' 
    t[0] = []
    concat('\n <TR><TD> lista_parametros →   </TD><TD> t[0] = [] </TD> </TR> ')


def p_def_par(t) : 
    'def_par    : CORIZQ expresion CORDER'
    t[0] = [Parametro(t[2])]
    concat('\n <TR><TD> def_par → [ expresion ] </TD><TD> t[0] = Parametro(t[2]) </TD> </TR> ')


def p_tipo_variable_tempvar(t) :
    'tipo_variable      : TEMPVAR'
    t[0] = Variable(t[1],TIPO_VARIABLE.TEMPORAL)
    concat('\n <TR><TD> tipo_variable → = '+str(t[1])+' </TD><TD> t[0] = Variable(t[1],TIPO_VARIABLE.TEMPORAL) </TD> </TR> ')


def p_tipo_variable_param(t) :
    'tipo_variable      : PARAM'
    t[0] = Variable(t[1],TIPO_VARIABLE.PARAMETRO)
    concat('\n <TR><TD> tipo_variable → = '+str(t[1])+' </TD><TD>  t[0] = Variable(t[1],TIPO_VARIABLE.PARAMETRO) </TD> </TR> ')

def p_tipo_variable_valorfuncion(t) :
    'tipo_variable      : FUNVAL'
    t[0] = Variable(t[1],TIPO_VARIABLE.VALOR_DEV_FUN)
    concat('\n <TR><TD> tipo_variable → = '+str(t[1])+' </TD><TD>  t[0] = Variable(t[1],TIPO_VARIABLE.VALOR_DEV_FUN) </TD> </TR> ')


def p_tipo_variable_ra(t) :
    'tipo_variable      : RA'
    t[0] = Variable(t[1],TIPO_VARIABLE.RA)
    concat('\n <TR><TD> tipo_variable → = '+str(t[1])+' </TD><TD>  t[0] = Variable(t[1],TIPO_VARIABLE.RA) </TD> </TR> ')


def p_tipo_variable_stack(t) :
    'tipo_variable      : STACK'
    t[0] = Variable(t[1],TIPO_VARIABLE.STACK)
    concat('\n <TR><TD> tipo_variable → = '+str(t[1])+' </TD><TD>  t[0] = Variable(t[1],TIPO_VARIABLE.STACK) </TD> </TR> ')


def p_tipo_variable_sp(t) :
    'tipo_variable      : SP'
    t[0] = Variable(t[1],TIPO_VARIABLE.SP)
    concat('\n <TR><TD> tipo_variable → = '+str(t[1])+' </TD><TD>  t[0] = Variable(t[1],TIPO_VARIABLE.SP) </TD> </TR> ')

def p_instruccion_print(t) :
    'print_instr     : PRINT PARIZQ valor PARDER PTCOMA'
    t[0] = Print(t[3])
    concat('\n <TR><TD> print_instr → = PRINT ( valor ) ;</TD><TD>  t[0] = Print(t[3]) </TD> </TR> ')



def p_goto_instr(t) :
    'goto_instr     : GOTO ID PTCOMA'
    t[0] = GoTo(t[2])
    concat('\n <TR><TD> goto_instr → = GOTO ( '+str(t[2])+' ) ;</TD><TD>  t[0] = GoTo(t[2]) </TD> </TR> ')



def p_unset_instr(t) :
    'unset_instr        : UNSET PARIZQ tipo_variable PARDER PTCOMA'
    t[0] = Unset(t[3])
    concat('\n <TR><TD> unset_isntr → = Unset ( tipo_variable ) ; ( valor ) ;</TD><TD> t[0] = Unset(t[3]) </TD> </TR> ')



def p_exit_instr(t) :
    'exit_instr         : EXIT PTCOMA'
    t[0] = ExitInstruccion()
    concat('\n <TR><TD> exit_isntr → = Exit ; ( tipo_variable ) ; ( valor ) ;</TD><TD> t[0] = ExitInstruccion() </TD> </TR> ')


def p_expresion_valor(t) :
    '''expresion  : valor expresiones'''
    t[0]=t[2]
    concat('\n <TR><TD> expresion → valor expresiones </TD><TD> t[0] = t[2] </TD> </TR> ')

def p_expresion_unaria(t) :
    '''expresion  : expresion_unaria'''
    t[0] = t[1]
    concat('\n <TR><TD> expresion → expresion_unaria </TD><TD> t[0] = t[1] </TD> </TR> ')


def p_expresiones(t) :
    '''expresiones :  MAS valor
                    | MENOS valor
                    | MULTI valor
                    | DIVISION valor
                    | RESIDUO valor
                    | IGUALQUE valor
                    | DISTINTO valor
                    | MAYORIG valor
                    | MENORIG valor
                    | MAYORQUE valor
                    | MENORQUE valor
                    | AND valor
                    | OR valor
                    | XOR valor
                    | ANDBB valor
                    | ORBB valor
                    | XORBB valor
                    | SHIFTIZQ valor
                    | SHIFTDER valor
                    | empty
    '''
    if t[1] == '+'  : 
        t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.MAS)
        concat('\n <TR><TD> expresiones → =  + valor</TD><TD> t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.MAS) </TD> </TR> ')
    elif t[1] == '-': 
        t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.MENOS)
        concat('\n <TR><TD> expresiones → =  - valor</TD><TD> t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.MENOS) </TD> </TR> ')
    elif t[1] == '*': 
        t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.MULTI)
        concat('\n <TR><TD> expresiones → =  * valor</TD><TD> t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.MULTI) </TD> </TR> ')
    elif t[1] == '/': 
        t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.DIVIDIDO)
        concat('\n <TR><TD> expresiones → =  / valor</TD><TD> t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.DIVIDIDO) </TD> </TR> ')
    elif t[1] == '%': 
        t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.RESIDUO)
        concat('\n <TR><TD> expresiones → =  % valor</TD><TD> t[0] = ExpresionAritmetica(t[-1], t[2], OPERACION_ARITMETICA.RESIDUO) </TD> </TR> ')

    elif t[1] == '==' : 
        t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.IGUALQUE)
        concat('\n <TR><TD> expresiones →  IGUALQUE valor </TD><TD>  t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.IGUALQUE) </TD> </TR> ')
    elif t[1] == '!=' : 
        t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.DISTINTO)
        concat('\n <TR><TD> expresiones →  DISTINTO valor </TD><TD>  t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.DISTINTO) </TD> </TR> ')
    elif t[1] == '>=' : 
        t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MAYORIGUAL)
        concat('\n <TR><TD> expresiones →  MAYORIG valor </TD><TD>  t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MAYORIG) </TD> </TR> ')
    elif t[1] == '<=' : 
        t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MENORIGUAL)
        concat('\n <TR><TD> expresiones →  MENORIG valor </TD><TD>  t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MENORIG) </TD> </TR> ')
    elif t[1] == '>'  : 
        t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MAYORQUE)
        concat('\n <TR><TD> expresiones →  MAYORQUE valor </TD><TD>  t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MAYORQUE) </TD> </TR> ')
    elif t[1] == '<' : 
        t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MENORQUE)
        concat('\n <TR><TD> expresiones →  MENORQUE valor </TD><TD>  t[0] = ExpresionRelacional(t[-1], t[2], OPERACION_RELACIONAL.MENORQUE) </TD> </TR> ')

    elif t[1] == '&&' : 
        t[0] = ExpresionLogica(t[-1],t[2],OPERACION_LOGICA.AND)
        concat('\n <TR><TD> expresiones → AND valor </TD><TD> ExpresionLogica(t[-1],t[2],OPERACION_LOGICA.AND) </TD> </TR> ')
    elif t[1] == '||' : 
        t[0] = ExpresionLogica(t[-1],t[2],OPERACION_LOGICA.OR)
        concat('\n <TR><TD> expresiones → OR valor </TD><TD> ExpresionLogica(t[-1],t[2],OPERACION_LOGICA.OR) </TD> </TR> ')
    elif t[1] == 'xor' : 
        t[0] = ExpresionLogica(t[-1],t[2],OPERACION_LOGICA.XOR)
        concat('\n <TR><TD> expresiones → XOR valor </TD><TD> ExpresionLogica(t[-1],t[2],OPERACION_LOGICA.XOR) </TD> </TR> ')
    elif t[1] == '&' : 
        t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.AND)
        concat('\n <TR><TD> expresiones → ANDBB valor </TD><TD>  t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.AND) </TD> </TR> ')
    elif t[1] == '|' : 
        t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.OR)
        concat('\n <TR><TD> expresiones → ORBB valor</TD><TD>  t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.OR) </TD> </TR> ')
    elif t[1] == '^' : 
        t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.XOR)
        concat('\n <TR><TD> expresiones → XORBB valor </TD><TD>  t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.XOR) </TD> </TR> ')
    elif t[1] == '<<': 
        t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.SHIFT_IZQ)
        concat('\n <TR><TD> expresiones → SHIFTIZQ valor </TD><TD>  t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.SHIFT_IZQ) </TD> </TR> ')
    elif t[1] == '>>': 
        t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.SHIFT_DER)
        concat('\n <TR><TD> expresiones → SHIFTDER valor </TD><TD>  t[0] = ExpresionBitABit(t[-1],t[2],OPERACION_BIT_A_BIT.SHIFTDER) </TD> </TR> ')
    else:
        t[0]=t[-1]
        concat('\n <TR><TD> expresiones → empty </TD><TD>  t[0] = t[-1] </TD> </TR> ')

def p_unitaria_negativo(t):
    'expresion_unaria : MENOS valor'
    t[0] = UnitariaNegAritmetica(t[2])
    concat('\n <TR><TD> valexpresion_unaria → - valor </TD><TD>  t[0] = UnariaNegAritmetica(t[2]) </TD> </TR> ')

def p_unaria_notlogica(t) :
    'expresion_unaria : NOT valor '
    t[0] = UnitariaLogicaNOT(t[2])
    concat('\n <TR><TD> valexpresion_unaria → NOT valor </TD><TD>  t[0] = UnariaLogicaNOT(t[2]) </TD> </TR> ')

def p_unaria_notbb(t) :
    'expresion_unaria : NOTBB valor '
    t[0] = UnitariaNotBB(t[2])
    concat('\n <TR><TD> expresion_unaria → NOTBB valor </TD><TD> t[0] = UnitariaNotBB(t[2]) </TD> </TR> ')

def p_unaria_referencia(t) :
    'expresion_unaria : ANDBB valor '
    t[0] = UnariaReferencia(t[2])
    concat('\n <TR><TD> expresion_unaria → ANDD valor </TD><TD>  t[0] = UnariaReferencia(t[2]) </TD> </TR> ')


def p_casteo(t) :
    'valor : PARIZQ tipo  PARDER valor '
    t[0] = Casteo(t[2],t[4])
    concat('\n <TR><TD> valor → ( tipo ) valor </TD><TD>  t[0] = Casteo(t[2],t[4]) </TD> </TR> ')


def p_tipo( t) :
    '''tipo : INT
            | FLOAT
            | CHAR'''
    if t[1]=='int' : 
        t[0] = TIPO_DATO.ENTERO
        concat('\n <TR><TD> tipo → int </TD><TD>  t[0] = TIPO_DATO.ENTERO </TD> </TR> ')
    elif t[1]=='float' : 
        t[0] = TIPO_DATO.FLOTANTE
        concat('\n <TR><TD> tipo → float </TD><TD>  t[0] = TIPO_DATO.FLOTANTE </TD> </TR> ')
    elif t[1]=='char' : 
        t[0] = TIPO_DATO.CHAR
        concat('\n <TR><TD> tipo → char </TD><TD>  t[0] = TIPO_DATO.CHAR </TD> </TR> ')

def p_valor_number(t):
    '''valor : ENTERO'''
    t[0] = ExpresionValor(t[1])
    concat('\n <TR><TD> valor → '+str(t[1])+' </TD><TD> t[0] = ExpresionValor(t[1]) </TD> </TR> ')

def p_valor_flotante(t):
    'valor : DECIMAL'
    t[0] = ExpresionValor(t[1])
    concat('\n <TR><TD> valor → '+str(t[1])+' </TD><TD> t[0] = ExpresionValor(t[1]) </TD> </TR> ')
    
def p_valor_cadena(t):
    '''valor : CADENA
            | CADENADOBLE'''
    t[0] = ExpresionValor(t[1])
    concat('\n <TR><TD> valor → '+str(t[1])+' </TD><TD> t[0] = ExpresionValor(t[1]) </TD> </TR> ')

def p_valor_variable(t):
    'valor   : tipo_variable paramsaccess'
    t[0] = t[2]
    concat('\n <TR><TD> valor → tipo_variable paramsaccess </TD><TD> t[0] = t[2] </TD> </TR> ')

def p_paramsaccess_empty(t) :
    'paramsaccess : empty'
    t[0]=t[-1] # se retorna tipo_variable si no viene ningun parametro
    concat('\n <TR><TD> paramsaccess → empty </TD><TD> t[0] = t[-1] </TD> </TR> ')

def p_paramsaccess(t) :
    'paramsaccess :  def_par lista_parametros'
    t[1].extend(t[2])
    t[0] = AccesoArray(t[-1],t[1])
    concat('\n <TR><TD> paramsaccess → def_par lista_parametros </TD><TD> t[0] = AccesoArray(t[-1],t[1]) </TD> </TR> ')

def p_valor_read(t) :
    'valor : READ PARIZQ PARDER'
    t[0] = Read()
    concat('\n <TR><TD> valor → Read ( ) </TD><TD> t[0] =Read() </TD> </TR> ')

def p_valor_abs(t) :
    'valor : ABS PARIZQ expresion PARDER'
    t[0] = Absoluto(t[3])
    concat('\n <TR><TD> valor → ABS ( expresion ) </TD><TD> t[0] =Absoluto(t[3]) </TD> </TR> ')

def p_if_instr(t) :
    'if_instr     : IF PARIZQ expresion PARDER goto_instr'
    t[0] =If(t[3], t[5])
    concat('\n <TR><TD> if_isntr → IF ( expresion ) goto_instr </TD><TD> t[0] =If(t[3], t[5]) </TD> </TR> ')


def p_error(t):    
    if not t:
        print("End of File")
        return
 
    #print("Error sintáctico en '%s'" % (t.value,))
    nErr=ErrorRep('Sintactico','Error de sintaxis en '+str(t.value),t.lineno)
    lisErr.agregar(nErr)
    
    while True:
        tok = parser.token()             
        if not tok or tok.type == 'PTCOMA': 
            break


from graphviz import Digraph, nohtml
from graphviz import escape


def concat(cad):
    global cadena
    cadena+=cad

dot = Digraph('g', filename='gram_desc.gv', format='png',
            node_attr={'shape': 'plaintext', 'height': '.1'})

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input,liser) :
    global cadena,lisErr,dot
    lisErr=liser
    cadena=''
    #parser = yacc.yacc()
    lexer.lineno=1
    par= parser.parse(input,lexer=lexer)
    
    dot.node('table','<<TABLE><TR><TD>PRODUCCION</TD><TD>REGLAS SEMANTICAS</TD></TR>'+cadena+'</TABLE>>')
    #dot.view()
    return par
