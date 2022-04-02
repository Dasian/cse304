# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer

currentClass = ""
currentVisibility = ""
currentType = None
isCurrentStatic = False
fieldID = 0
methodID = 0
varID = 0

tree = AST()

# Assignment is right-associative, relational operators are non-associative, and all others are left-associative
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALITY', 'INEQUALITY'),
    ('nonassoc', 'LESSER', 'GREATER', 'GEQ', 'LEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'NOT')
)


# The program with zero or more class declarations
def p_program(p):
    '''program : class_decl
               | empty
    class_decl : class_decl class_decl'''


# The class declaration with or without inheritance and one or more class body declarations
def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                  | CLASS ID '{' class_body_decl '}'
                  '''

    p[0] = ast.ClassRecord()        # Initializes an empty class record
    p[0].name = p[2]            # Set class record's name to p[2]
    currentClass = p[0].name

    body_index = 4          # Represents the index where class_body_decl starts
    if p[2] == EXTENDS:         # Checks if class record is a child class
        body_index = 6
        p[0].superName = p[4]

# Loop through all the class body declarations to add appropriate records to
# class record's constructors, methods, and fields

# TODO Fix append line of methods list
    """for i in p[body_index]:
        if(type(i) is ast.ConstructorRecord):
            p[0].constructors.append(p[i])
        elif(type(i) is ast.MethodRecord):
            p[0].methods.append(p[i])
        elif(type(i) is ast.FieldRecord):
            p[0].fields.append(p[i])"""

# One or more class body declarations that contains either fields, methods, and/or constructors
def p_class_body_decl(p):
    '''class_body_decl : class_body_decl class_body_decl
                       | field_decl
                       | method_decl
                       | constructor_decl'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    if len(p) == 2:
        p[0] = [p[1]]

def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | ID'''
    p[0] = ast.TypeRecord(p[1])

def p_modifier(p):
    '''modifier : PRIVATE STATIC
                | PRIVATE
                | PUBLIC STATIC
                | PUBLIC
                | STATIC
                | empty'''
    p[0] = p[1:]

def p_var_decl(p):
    '''var_decl : type variables ';' '''
    p[0] = {"type" : p[1], "variables" : p[2]}

def p_variables(p):
    '''variables : variable
                 | variable ',' variables'''
    if len(p) == 3:
        p[0] = p[1] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

def p_variable(p):
    '''variable  : ID '''
    p[0] = p[1]

# Field declaration with a type, variable name, and optional modifiers
def p_field_decl(p):
    '''field_decl : modifier var_decl'''

    containingClass = currentClass
    visibility = ''
    applicability = ''

    modifiers = p[1]
    if modifiers in 'public':
        visibility = 'public'
    else:
        visibility = 'private'

    if modifiers in 'static':
        applicability = 'static'
    else:
        applicability = 'non-static'

    var_decl = p[2]
    type = var_decl["type"]

    p[0] = []
    x = fieldID
    for var in var_dcl["variables"]:
        x += 1
        field = ast.FieldRecord(var, x, containingClass, visibility, applicability, type)
        p[0] += [field]

def p_method_decl(p):
    '''method_decl      : modifier type ID '(' optional_formals ')' block
                        | modifier VOID ID '(' optional_formals ')' block'''
    methodType = ''
    if p[2] == 'void':
        methodType = 'void'
    else:
        methodType = p[2]

    visibility = ''
    applicability = ''

    modifiers = p[1]
    if 'public' in modifiers:
        visibility = 'public'
    else:
        visibility = 'private'

    if 'static' in modifiers:
        applicability = 'static'
    else:
        applicability = 'non-static'

    parameters = p[5]
    method_body = p[7]

    x = methodID
    x += 1
    # TODO replace empty list with variable table
    p[0] = ast.MethodRecord(p[3], x, currentClass
    , visibility, applicability, method_body, [], methodType, parameters)

def p_optional_formals(p):
    '''optional_formals : formals
                        | empty'''
    p[0] = p[1]

def p_formals(p):
    '''formals  : formal_param ',' formals
                | formal_param'''
    if len(p) == 3:
        p[0] = p[1] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = {"type" : p[1], "variable": p[2]}

# A method declaration with modifiers, return type, method name, and optional parameters
# A constructor declaration with modifiers, class name, and optional parameters
def p_constructor_decl(p):
    '''constructor_decl : modifier ID '(' optional_formals ')' block'''

    name = p[2]
    visibility = ''
    applicability = ''
    modifiers = p[1]

    if 'public' in modifiers:
        visibility = 'public'
    else:
        visibility = 'private'

    if 'static' in modifiers:
        applicability = 'static'
    else:
        applicability = 'non-static'

    parameters = p[4]
    body = p[6]
    variableTable = parameters + body

    p[0] = ast.ConstructorRecord(name, visibility, parameters,variableTable, body)


def p_statements(p):
    '''block        : '{' stmt '}'
                    | '{' '}'
    stmt            : stmt stmt
                    | IF '(' expr ')' stmt ELSE stmt
                    | IF '(' expr ')' stmt
                    | WHILE '(' expr ')' stmt
                    | FOR '(' optional_stmt_expr ';' optional_expr ';' optional_stmt_expr ')' stmt
                    | RETURN optional_expr ';'
                    | stmt_expr ';'
                    | BREAK ';'
                    | CONTINUE ';'
                    | block
                    | var_decl
                    | ';'
    optional_expr   : expr
                    | empty
    optional_stmt_expr : stmt_expr
                    | empty'''

    if p[1] == FOR:
        p[0] = new ForStatement(p[3], p[5], p[9], p[7])   # number line range
    elif p[1] == WHILE:
        p[0] = new WhileStatement(p[3], p[5])
    elif p[1] == BREAK:
        p[0] = new BreakStatement()
    elif p[1] == CONTINUE:
        p[0] = new ContinueStatement()


def p_expressions(p):
    '''literal : INT_CONST
               | FLOAT_CONST
               | STRING_CONST
               | NULL
               | TRUE
               | FALSE
    primary : literal
            | THIS
            | SUPER
            | '(' expr ')'
            | NEW ID '(' arguments ')'
            | NEW ID '(' ')'
            | field_access
            | method_invocation
    arguments : expr
              | expr ',' arguments
    field_access : primary '.' ID
                 | ID
    method_invocation : field_access '(' arguments ')'
                      | field_access '(' ')'
    expr : primary
         | assign
         | expr arith_op expr
         | expr bool_op expr
         | unary_op expr
    assign : field_access ASSIGN expr
     | field_access INCREMENT
     | INCREMENT field_access
     | field_access DECREMENT
     | DECREMENT field_access
    stmt_expr : assign
              | method_invocation'''


def p_operators(p):
    """arith_op : PLUS
            | MINUS
            | TIMES
            | DIVIDE
    bool_op : AND
            | OR
            | EQUALITY
            | INEQUALITY
            | LESSER
            | GREATER
            | LEQ
            | GEQ
    unary_op : PLUS
            | MINUS
            | NOT"""


# Error rule for syntax errors
def p_error(p):
    if p is not None:
        print("Syntax error at line: %d column: %d" % (p.lexer.lineno, p.lexpos - lexer.line_start))
    else:
        print("Unexpected EOF")
    exit()


# Handles empty productions
def p_empty(p):
    'empty :'
    pass
