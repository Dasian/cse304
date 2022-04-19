# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

from numpy import block
import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer
import decaf_ast as ast
from decaf_checker import AST
import debug

block_depth = 0
block_stmnts = {block_depth: []}
currentClass = ""
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

# done
# The program with zero or more class declarations
def p_program(p):
    '''program : class_decl
               | empty
    class_decl : class_decl class_decl'''
    tree.print_table()

# done
# The class declaration with or without inheritance and one or more class body declarations
def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                  | CLASS ID '{' class_body_decl '}'
                  '''
    # Reset Global vars
    global block_stmnts
    global block_depth
    global fieldID
    global methodID
    global varID
    global conID
    global currentClass

    block_depth = 0
    block_stmnts = {block_depth: []}
    fieldID = 0
    methodID = 0
    varID = 0
    conID = 0
    currentClass = ""

    p[0] = ast.ClassRecord()        # Initializes an empty class record
    p[0].name = p[2]            # Set class record's name to p[2]
    currentClass = p[2]

    body_index = 4          # Represents the index where class_body_decl starts
    if p[3] == 'extends':         # Checks if class record is a child class
        body_index = 6
        p[0].superName = p[4]

    # Loop through all the class body declarations to add appropriate records to
    # class record's constructors, methods, and fields
    for record in p[body_index]:
        if(type(record) is ast.ConstructorRecord):
            record.containingClass = currentClass
            p[0].constructors.append(record)
        elif(type(record) is ast.MethodRecord):
            record.containingClass = currentClass
            p[0].methods.append(record)
        else:   # record must be a list of fields
            for field in record:
                field.containingClass = currentClass
                p[0].fields.append(field)


    debug.print_p(p, msg="Printing p from class_decl")
    tree.add_class(p[0])

# TODO: fields, statements, decl
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

# done
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | ID'''
    p[0] = ast.TypeRecord(p[1])

# done
def p_modifier(p):
    '''modifier : PRIVATE STATIC
                | PRIVATE
                | PUBLIC STATIC
                | PUBLIC
                | STATIC
                | empty'''
    p[0] = p[1:]

# done
def p_var_decl(p):
    '''var_decl : type variables ';' '''
    p[0] = {"type" : p[1], "variables" : p[2]}

# done
def p_variables(p):
    '''variables : variable
                 | variable ',' variables'''
    if len(p) == 3:
        p[0] = p[1] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

# done
def p_variable(p):
    '''variable  : ID '''
    p[0] = p[1]

# TODO: field id?
# Field declaration with a type, variable name, and optional modifiers
def p_field_decl(p):
    '''field_decl : modifier var_decl'''
    global currentClass
    print(currentClass)
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

    var_decl = p[2]
    type = var_decl["type"]

    p[0] = []
    x = fieldID
    for var in var_decl["variables"]:
        x += 1
        field = ast.FieldRecord(name = var, id = x, containingClass= currentClass, visibility= visibility, applicability= applicability, type= type)
        p[0] += [field]

# TODO: replace empty list with variable table
def p_method_decl(p):
    '''method_decl      : modifier type ID '(' optional_formals ')' block
                        | modifier VOID ID '(' optional_formals ')' block'''
    
    # reset blocks dict
    # reset when creating method and constructor
    global block_stmnts
    global block_depth
    block_depth = 0
    block_stmnts = {block_depth: []}

    # never set but needs t0 be
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

    x = methodID
    # TODO replace empty list with variable table
    p[0] = ast.MethodRecord(name= p[3], id=x, containingClass=currentClass
    , visibility=visibility, applicability=applicability, body=method_body, returnType=methodType, parameters=parameters)

# TODO: variable table
def p_optional_formals(p):
    '''optional_formals : formals
                        | empty'''
    var_list = []

    # TODO fix variableTable
    if p[1] is not None:
        var_list = p[1]
    p[0] = var_list

# done
def p_formals(p):
    '''formals  : formal_param ',' formals
                | formal_param'''
    if len(p) == 4:
        p[0] = p[1] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

# TODO: field_id, variable table, field_id again
def p_formal_param(p):
    '''formal_param : type variable'''

    # TODO FIND OUT HOW TO PROPERLY UPDATE FIELD_ID
    p[0] = ast.VariableRecord(name = p[2], id = 1, kind = "formal", type= p[1])

# A method declaration with modifiers, return type, method name, and optional parameters
# A constructor declaration with modifiers, class name, and optional parameters
def p_constructor_decl(p):
    '''constructor_decl : modifier ID '(' optional_formals ')' block'''

    # reset blocks dict
    # reset when creating method and constructor
    global block_stmnts
    global block_depth
    block_stmnts = {}
    block_depth = 0

    name = p[2]
    visibility = ''
    modifiers = p[1]

    if 'public' in modifiers:
        visibility = 'public'
    else:
        visibility = 'private'

    parameters = p[4]
    body = p[6]

    p[0] = ast.ConstructorRecord(id=name, visibility=visibility, parameters=parameters,variableTable=[], body=body)

# TODO include line range

def p_block(p):
    '''block : '{' optional_stmts '}'
             | '{' '}'
    '''

def p_optional_stmts(p):
    '''optional_stmts : stmt stmt
                       | empty'''

# TODO line range, nested block statements
def p_statements(p):
    '''stmt         : IF '(' expr ')' stmt ELSE stmt
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

    # splitting stmnt for calculating block size
    if len(p) == 3 and ';' not in p and '{' not in p:
        block_size += 1
    elif p[1] == 'if':
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
        p[0].attributes.update({'stmnts': block_stmnts[block_depth]}) # might need to be copied? not sure
        block_depth += 1
    elif p[1] == 'break':
        p[0].kind = 'Break'
    elif p[1] == 'continue':
        p[0].kind = 'Continue'
    # skip statement?

    # adding line range?

    # add to block statement
    block_stmnts[block_depth].append(p[0])

# TODO: all
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
    # This is all just general information
    # they need to be broken up in a better way
    # copying/pasting/editing for all of these parts is welcome
    # change the indices as needed for each
    # I also tried to get the typing consistent
    p[0] = ast.Expression()

    # added to prevent the expression template code from running
    value = True
    if value:
        return
    
    # Constant
    # ***Remember to change the indices!***
    # need to find a way to assign the values to the table
    p[0].kind = "Constant"
    value_constants = ["Float-constant", "Integer-constant", "String-constant"]
    if type(p[1]) is ast.Expression:
        # adding Integer/Float/String-constant
        if p[1].kind in value_constants:
            # not sure how p[1] would be generated though
            p[0].attributes.update({p[1].kind: p[1]})
        # adding Null, True, or False
        else:
            # this might not be necessary/could screw things up
            # depending on how the inner attributes are generated
            p[0].attributes.update({p[1].kind: ""})

    # Var
    # ***Remember to change the indices!***
    # scoping rules for variables with the same name 
    # needs to be handled somewhere
    p[0].kind = "Var"
    if type(p[1]) is ast.VariableRecord:
        p[0].attributes.update({"ID": p[1].id})

    # Unary
    # ***Remember to change the indices!***
    p[0].kind = "Unary"
    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"operand": p[1]})
    # uminus or negative (-); 
    if type(p[2]) is str:
        p[0].attributes.update({"unary-operator": p[2]})

    # Binary
    # ***Remember to change the indices!***
    p[0].kind = "Binary"
    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"operand1": p[1]})
    if type(p[2]) is ast.Expression:
        p[0].attributes.update({"operand2": p[2]})
    # one of add, sub, mul, div, and, or, eq, neq, lt, leq, gt, and geq
    # or the symbols rather? not sure
    if type(p[3]) is str:
        p[0].attributes.update({"operator": p[3]})

    # Assign
    # ***Remember to change the indices!***
    p[0].kind = "Assign"
    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"left": p[1]})
    if type(p[2]) is ast.Expression:
        p[0].attributes.update({"right": p[2]})

    # Auto
    # ***Remember to change the indices!***
    p[0].kind = "Auto"
    # variable being manipulated: ex: x
    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"operand": p[1]})
    # 'inc' or 'dec'; ex: ++ or --
    if type(p[2]) is str:
        p[0].attributes.update({"operation": p[2]})
    # 'post' or 'pre'; ex: x++ or ++x
    if type(p[3]) is str:
        p[0].attributes.update({"order": p[3]})

    # Field-access
    # ***Remember to change the indices!***
    p[0].kind = "Field-access"
    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"base": p[1]})
    if type(p[2]) is str:
        p[0].attributes.update({"field-name": p[2]})

    # Method-call
    # ***Remember to change the indices!***
    p[0].kind = "Method-call"
    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"base": p[1]})
    if type(p[2]) is str:
        p[0].attributes.update({"method-name": p[2]})
    # list of Expression objects
    if type(p[3]) is list:
        p[0].attributes.update({"arguments": p[3]})

    # New-object
    # ***Remember to change the indices!***
    p[0].kind = "New-object"
    if type(p[1]) is str:
        p[0].attributes.update({"class-name": p[1]})
    # list of expressions to pass to the constructor
    # the list could be empty (no args)
    if type(p[2]) is list:
        p[0].attributes.update({"arguments": p[2]})

    # This
    p[0].kind = "This"

    # Super
    p[0].kind = "Super"

    # Class-reference
    # ***Remember to change the indices!***
    p[0].kind = "Class-reference"
    # denotes the value of literal class names
    if type(p[1]) is str:
        p[0].attributes.update({"class-name": p[1]})

# TODO: all
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
