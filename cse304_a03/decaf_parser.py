# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer
import decaf_ast as ast
from decaf_checker import AST

currentClass = ""
currentVisibility = ""
currentType = None
isCurrentStatic = False
id = 0
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
    if len(p) == 2:
        tree.print_table()

# The class declaration with or without inheritance and one or more class body declarations
def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                  | CLASS ID '{' class_body_decl '}'
                  '''

    for i in range(len(p)):
        print(i, p[i], type(p[i]))

    p[0] = ast.ClassRecord()        # Initializes an empty class record
    p[0].name = p[2]            # Set class record's name to p[2]
    currentClass = p[0].name

    body_index = 4          # Represents the index where class_body_decl starts
    if p[2] == 'extends':         # Checks if class record is a child class
        body_index = 6
        p[0].super = p[4]

# Loop through all the class body declarations to add appropriate records to
# class record's constructors, methods, and fields
    for i in range(body_index, len(p)):
        if(type(p[i]) is ast.ConstructorRecord):
            p[0].constructor += p[i]
        elif(type(p[i]) is ast.MethodRecord):
            p[0].methods += p[i]
        elif(type(p[i]) is ast.FieldRecord):
            p[0].fields += p[i]

    tree.add_class(p[0])

# One or more class body declarations that contains either fields, methods, and/or constructors
def p_class_body_decl(p):
    '''class_body_decl : class_body_decl class_body_decl
                       | field_decl
                       | method_decl
                       | constructor_decl'''
    if len(p) == 2:
        p[0] = p[1]


# Field declaration with a type, variable name, and optional modifiers
def p_field_decl(p):
    '''field_decl : modifier var_decl
    modifier      : PRIVATE STATIC
                  | PRIVATE
                  | PUBLIC STATIC
                  | PUBLIC
                  | STATIC
                  | empty
    var_decl      : type variables ';'
    type          : INT
                  | FLOAT
                  | BOOLEAN
                  | ID
    variables     : variable
                  | variable ',' variables
    variable      : ID '''

    if p[0] == 'type':
        p[0] = ast.TypeRecord(p[1])
    if p[0] == 'modifier':
        if p[1] == 'private' or p[1] == 'public':
            currentVisibility = p[1]
        if p[1] == 'static' or p[2] == 'static':
            isCurrentStatic = True
    if p[0] == 'variables':
        for i in range(1, len(p)):
            p[0] = ast.FieldRecord()
            p[0].name = p[1]
            p[0].visibility = currentVisibility
            p[0].containingClass = currentClass
            p[0].applicability = isCurrentStatic
            P[0].type = currentType

# A method declaration with modifiers, return type, method name, and optional parameters
# A constructor declaration with modifiers, class name, and optional parameters
def p_method_constructor_decl(p):
    '''method_decl      : modifier type ID '(' optional_formals ')' block
                        | modifier VOID ID '(' optional_formals ')' block
       constructor_decl : modifier ID '(' optional_formals ')' block
       optional_formals : formals
                        | empty
       formals          : formal_param ',' formals
                        | formal_param
       formal_param     : type variable'''

    if p[0] == 'constructor_decl':
        p[0] = ast.ConstructorRecord()
        p[0].id = p[2]
        p[0].visibility = p[1]
        p[0].parameters = p[4]
        p[0].body = p[6]
        for i in range(4, len(p)):
            if(type(p[i]) is ast.VariableRecord):
                p[0].variableTable += p[i].name

    elif p[0] == 'method_decl':
        p[0] = ast.MethodRecord()
        if p[2] == 'void':
            p[0].method_name = p[3]
            p[0].method_visibility = p[1]
            p[0].method_parameters = p[5]
            p[0].return_type = p[2]
            p[0].method_body = p[7]
        else:
            p[0].method_name = p[3]
            p[0].method_visibility = p[1]
            p[0].method_parameters = p[5]
            p[0].return_type = "void"
            p[0].method_body = p[7]


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
    if p[1] == 'for':
        p[0] = ast.ForStatement(p[3], p[5], p[9], p[7])   # number line range
    elif p[1] == 'while':
        p[0] = ast.WhileStatement(p[3], p[5])
    elif p[1] == 'break':
        p[0] = ast.BreakStatement()
    elif p[1] == 'continue':
        p[0] = ast.ContinueStatement()


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
