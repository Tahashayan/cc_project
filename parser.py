import ply.yacc as yacc
from lexer import tokens

# Abstract Syntax Tree (AST) container

# --- Grammar Rules ---

def p_program(p):
    '''program : stmt_list'''
    p[0] = ('program', p[1])

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# --- Statements ---

def p_stmt_assign(p):
    '''stmt : ID ASSIGN expr SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_stmt_if(p):
    '''stmt : IF LPAREN expr RPAREN stmt %prec IFX
            | IF LPAREN expr RPAREN stmt ELSE stmt'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if-else', p[3], p[5], p[7])

def p_stmt_declare_assign(p):
    '''stmt : TYPE ID ASSIGN expr SEMICOLON'''
    p[0] = ('declare', p[1], p[2], p[4])

def p_stmt_switch(p):
    '''stmt : SWITCH LPAREN expr RPAREN LBRACE case_list default_clause RBRACE'''
    p[0] = ('switch', p[3], p[6], p[7])

def p_case_list(p):
    '''case_list : case_list case
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_case(p):
    '''case : CASE NUMBER COLON stmt_list BREAK SEMICOLON'''
    p[0] = ('case', p[2], p[4])

def p_default_clause(p):
    '''default_clause : DEFAULT COLON stmt_list
                      | empty'''
    if len(p) == 4:
        p[0] = ('default', p[3])
    else:
        p[0] = None
        
def p_stmt_break(p):
    '''stmt : BREAK SEMICOLON'''
    p[0] = ('break',)

def p_empty(p):
    'empty :'
    p[0] = []


def p_stmt_while(p):
    '''stmt : WHILE LPAREN expr RPAREN stmt'''
    p[0] = ('while', p[3], p[5])

def p_stmt_do_while(p):
    '''stmt : DO stmt WHILE LPAREN expr RPAREN SEMICOLON'''
    p[0] = ('do-while', p[2], p[5])

def p_stmt_block(p):
    '''stmt : LBRACE stmt_list RBRACE'''
    p[0] = ('block', p[2])

def p_stmt_print(p):
    '''stmt : PRINT LPAREN expr RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

# --- Expressions ---

def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MOD expr
            | expr EQ expr
            | expr NEQ expr
            | expr LT expr
            | expr GT expr
            | expr LE expr
            | expr GE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = ('num', p[1])

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ('id', p[1])

# --- Error Handling ---

def p_error(p):
    if p:
        print(f"❌ Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("❌ Syntax error at EOF")

# --- Operator Precedence (resolves dangling else) ---

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD')
)

# --- Build the parser ---

parser = yacc.yacc()
