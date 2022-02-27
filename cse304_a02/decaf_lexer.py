# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/lex scanner specification file

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
t_ignore_COMMENT = r'\/\/.*'
t_ignore_MULTILINE_COMMENT = r'\\\*(.*|\n)*\*\\'


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

# Literal characters
literals = ['{', '}', ';', '.', '!', ',']

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_EQUALITY = r'=='
t_GREATER = r'>'
t_LESSER = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_INEQUALITY = r'!='
t_AND = r'&&'
t_OR = r'\|\|'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Identifier rule
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_LBRACE(t):
    r'\{'
    t.type = '{'  # Set token type to the expected literal
    return t


def t_RBRACE(t):
    r'\}'
    t.type = '}'  # Set token type to the expected literal
    return t


def t_STRING_CONST(t):
    r'\".*\"'
    t.value = t.value[1:len(t.value) - 1]
    return t


def t_FLOAT_CONST(t):
    r'\d+(\.(\d+)?([eE][-+]?\d+)?|[eE][-+]?\d+)'
    t.value = float(t.value)
    return t


def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t


tokens = list(reserved.values()) + ['ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'ASSIGN', 'EQUALITY', 'STRING_CONST', 'FLOAT_CONST', 'INT_CONST',
    'GREATER', 'LESSER', 'GEQ', 'LEQ', 'INEQUALITY', 'AND', 'OR']
