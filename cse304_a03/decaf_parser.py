# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer


import decaf_ast as ast
from decaf_checker import AST

block_stmnts = []
conID = 0
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
    tree.print_table()


# The class declaration with or without inheritance and one or more class body declarations
def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                  | CLASS ID '{' class_body_decl '}'
                  '''
    # Reset Global vars
    global block_stmnts
    global fieldID
    global methodID
    global varID
    global conID

    if block_stmnts is None:
        block_stmnts = []
    if fieldID is None:
        fieldID = 0
    if methodID is None:
        methodID = 0
    if varID is None:
        varID = 0
    if conID is None:
        conID = 0

    p[0] = ast.ClassRecord()        # Initializes an empty class record
    p[0].name = p[2]            # Set class record's name to p[2]
    currentClass = p[2]

    body_index = 4          # Represents the index where class_body_decl starts
    if p[2] == 'extends':         # Checks if class record is a child class
        body_index = 6
        p[0].superName = p[4]

# Loop through all the class body declarations to add appropriate records to
# class record's constructors, methods, and fields


    # Loop through all the class body declarations to add appropriate records to
    # class record's constructors, methods, and fields
    for declaration in p[body_index]:
        if(type(declaration) is ast.ConstructorRecord):
            conID += 1
            declaration.id = conID
            p[0].constructors.append(declaration)
        elif(type(declaration) is ast.MethodRecord):
            methodID += 1
            declaration.id = methodID
            declaration.containingClass = currentClass
            p[0].methods.append(declaration)
        elif(type(declaration) is ast.FieldRecord):
            fieldID += 1
            declaration.id = fieldID
            declaration.containingClass = currentClass
            p[0].fields.append(declaration)
    
    tree.add_class(p[0])

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

    visibility = ''
    applicability = ''

    modifiers = p[1]
    if 'public' in modifiers:
        visibility = 'public'
    else:
        visibility = 'private'

    if 'static' in modifiers:
        applicability = 'class field'
    else:
        applicability = 'instance'

    var_decl = p[2]
    type = var_decl["type"]

    p[0] = []
    # TODO FIND OUT HOW TO PROPERLY UPDATE FIELD_ID
    for var in var_decl["variables"]:
        field = ast.FieldRecord(var, 0, '', visibility, applicability, type)
        p[0] += [field]

def p_method_decl(p):
    '''method_decl      : modifier type ID '(' optional_formals ')' block
                        | modifier VOID ID '(' optional_formals ')' block'''
    methodType = ''
    if p[2] == 'void':
        methodType = ast.TypeRecord('void')
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
        applicability = 'instance'

    parameters = p[5]
    method_body = p[7]

    # TODO replace empty list with variable table

    p[0] = ast.MethodRecord(p[3], 0, ''
    , visibility, applicability, method_body, [], methodType, parameters)

def p_optional_formals(p):
    '''optional_formals : formals
                        | empty'''
    var_list = []

    # TODO fix variableTable
    if p[1] is not None:
        for variable in p[1]:
            var_list.append(variable)
    p[0] = var_list

def p_formals(p):
    '''formals  : formal_param ',' formals
                | formal_param'''
    if len(p) == 3:
        p[0] = p[1] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

def p_formal_param(p):
    '''formal_param : type variable'''

    # TODO FIND OUT HOW TO PROPERLY UPDATE FIELD_ID
    p[0] = ast.VariableRecord(p[2], 1, "formal", p[1])

# A method declaration with modifiers, return type, method name, and optional parameters
# A constructor declaration with modifiers, class name, and optional parameters
def p_constructor_decl(p):
    '''constructor_decl : modifier ID '(' optional_formals ')' block'''

    name = p[2]
    visibility = ''
    modifiers = p[1]

    if 'public' in modifiers:
        visibility = 'public'
    else:
        visibility = 'private'

    parameters = p[4]
    body = p[6]

    variableTable = []  # TODO FIX variableTable
    # TODO FIND OUT HOW TO PROPERLY UPDATE FIELD_ID
    p[0] = ast.ConstructorRecord(0, visibility, parameters, variableTable, body)


# TODO include line range

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

    p[0] = ast.Statement()
    if p[1] == 'if':
        p[0].kind = 'If'
        p[0].attributes.update({'condition': p[3]})
        p[0].attributes.update({'then': p[5]})
        if len(p) > 6:
            p[0].attributes.update({'else': p[7]})
    elif p[1] == 'for':
        p[0].kind = 'For'
        p[0].attributes.update({'initialize-expression': p[3]})
        p[0].attributes.update({'loop-condition': p[5]})
        p[0].attributes.update({'update-expression': p[7]})
        p[0].attributes.update({'loop-body': p[9]})
    elif p[1] == 'while':
        p[0].kind = 'While'
        p[0].attributes.update({'loop-condition': p[3]})
        p[0].attributes.update({'loop-body': p[5]})
    elif p[1] == 'return':
        p[0].kind = 'return'
        p[0].attributes.update({'return-expression', p[2]})
    elif type(p[1]) is ast.Expression and p[2] == ';': # expr-stmnt
        p[0].kind = 'Expr'
        p[0].attributes.update({'expression': p[1]})
    elif p[1] == '{': # block
        p[0].kind = 'Block'
        # possible make block_stmnts a double list
        # increment the index in method/constructor
        # decrement here
        # I actually think different inc/decs are needed
        p[0].attributes.update({'stmnts': block_stmnts}) # might need to be copied? not sure
    elif p[1] == 'break':
        p[0].kind = 'Break'
    elif p[1] == 'continue':
        p[0].kind = 'Continue'
    # skip statement?

    # adding line range?

    # add to block statement
    block_stmnts.append(p[0])


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
