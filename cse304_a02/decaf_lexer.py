# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/lex scanner specification file

reserved = {
    'boolean': 'BOOLEAN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'class': 'CLASS',
    'do': 'DO',
    'else': 'ELSE',
    'extends': 'EXTENDS',
    'false': 'FALSE',
    'float': 'FLOAT',
    'for': 'FOR',
    'if': 'IF',
    'int': 'INT',
    'new': 'NEW',
    'null': 'NULL',
    'private': 'PRIVATE',
    'public': 'PUBLIC',
    'return': 'RETURN',
    'static': 'STATIC',
    'super': 'SUPER',
    'this': 'THIS',
    'true': 'TRUE',
    'void': 'VOID',
    'while': 'WHILE'
}

tokens = list(reserved.values()) + ['ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
                                    'ASSIGN', 'EQUALITY', 'STRING_CONST', 'FLOAT_CONST',
                                    'INT_CONST', 'NOT',
                                    'GREATER', 'LESSER', 'GEQ', 'LEQ', 'INEQUALITY', 'AND', 'OR']

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
t_ignore_COMMENT = r'\/\/.*'

# Variable used to keep track of columns for errors
line_start = 1

# Literal characters
literals = ['(', ')', '{', '}', ';', '.', ',']

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQUALITY = r'=='
t_GREATER = r'>'
t_LESSER = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_INEQUALITY = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global line_start
    line_start = t.lexpos + 1


# Define a rule so we can track line numbers within multi-line comments
def t_multi_line_comment(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')


# Error handling rule
def t_error(t):
    print("Illegal character %s at (%d, %d)" % (t.value[0], t.lexer.lineno, (t.lexpos - line_start) + 1))
    exit()


# Identifier rule
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# String constants
def t_STRING_CONST(t):
    r'\".*?\"'
    t.value = t.value[1:len(t.value) - 1]
    return t


# Float constants
def t_FLOAT_CONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


# Integer constants
def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t