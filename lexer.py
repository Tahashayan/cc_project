import ply.lex as lex

# List of token names
tokens = [
    'ID', 'NUMBER', 'ASSIGN', 'SEMICOLON', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE', 'MOD',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'AND', 'OR',
] 
# Reserved keywords
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'print': 'PRINT',
    'int': 'TYPE',
    'float': 'TYPE',
    'bool': 'TYPE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'break': 'BREAK',
}

tokens += ['COLON'] + list(reserved.values())

# Regular expression rules
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_MOD        = r'%'
t_COLON      = r':'
t_ASSIGN     = r'='
t_EQ         = r'=='
t_NEQ        = r'!='
t_LT         = r'<'
t_LE         = r'<='
t_GT         = r'>'
t_GE         = r'>='
t_AND        = r'&&'
t_OR         = r'\|\|'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'

# Identifier and number
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

# Newline tracking
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"❌ Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
