# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

import ply.yacc as yacc
from decaf_lexer import tokens


precedence = (
    ('nonassoc', 'ASSIGN'),
    ('nonassoc', 'OR'),
    ('nonassoc', 'AND'),
    ('nonassoc', 'EQUALITY', 'INEQUALITY'),
    ('nonassoc', 'LESSER', 'GREATER', 'GEQ', 'LEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'NOT')
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


# One or more class body declarations that contains either fields, methods, and/or constructors
def p_class_body_decl(p):
    '''class_body_decl : class_body_decl class_body_decl
                       | field_decl
                       | method_decl
                       | constructor_decl'''


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
     | field_access PLUS PLUS
     | PLUS PLUS field_access
     | field_access MINUS MINUS
     | MINUS MINUS field_access
    arith_op : PLUS
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
            | NOT
    stmt_expr : assign
              | method_invocation'''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error at (%d, %d)" % (p.lexer.lineno, p.lexpos+1))
    exit()


# Handles empty productions
def p_empty(p):
    'empty :'
    pass
