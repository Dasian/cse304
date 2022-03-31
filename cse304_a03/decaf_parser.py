# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer
import decaf_ast as ast
from decaf_checker import AST

# DELETE THIS
import debug

currentClass = ""
currentVisibility = ""
currentType = None
isCurrentStatic = False
id = 0
block_stmnts = []
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

    p[0] = ast.ClassRecord()        # Initializes an empty class record
    p[0].name = p[2]            # Set class record's name to p[2]
    currentClass = p[0].name

    body_index = 4          # Represents the index where class_body_decl starts
    if p[3] == 'extends':         # Checks if class record is a child class
        body_index = 6
        p[0].superName = p[4]

    # Loop through all the class body declarations to add appropriate records to
    # class record's constructors, methods, and fields
    for i in range(body_index, len(p)):
        if(type(p[i]) is ast.ConstructorRecord):
            p[0].constructor.append(p[i])
        elif(type(p[i]) is ast.MethodRecord):
            p[0].methods.append(p[i])
        elif(type(p[i]) is ast.FieldRecord):
            p[0].fields.append(p[i])

    debug.print_p(p, msg="Printing p from class_decl")

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

    # print all values of p; debug

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
            p[0].type = currentType

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

    # when this function is first called/ends 
    # the block_statements list should be reset
    global block_stmnts
    block_stmnts = []

    if len(p) == 8:  # method_decl
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
    elif len(p) == 7: # constructor_decl
        p[0] = ast.ConstructorRecord()
        p[0].id = p[2]
        p[0].visibility = p[1]
        p[0].parameters = p[4]
        p[0].body = p[6]
        for i in range(4, len(p)):
            if(type(p[i]) is ast.VariableRecord):
                p[0].variableTable.push(p[i])

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
        p[1].attributes.update({'stmnts': block_stmnts}) # might need to be copied? not sure 
    elif p[1] == 'break':
        p[0].kind = 'Break'
    elif p[1] == 'continue':
        p[0].kind = 'Continue'
    # skip statement?

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
