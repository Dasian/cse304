# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

from numpy import block
import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer
import decaf_ast as ast

#block_depth = 0
#block_stmnts = {block_depth: []}
currentClass = ""
conID = 1
fieldID = 1
methodID = 1
varID = 1

tree = ast.AST()

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

    if len(p) != 3:
        tree.print_table()

# done
# The class declaration with or without inheritance and one or more class body declarations
def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                  | CLASS ID '{' class_body_decl '}'
                  '''
    # Reset Global vars
    #global block_stmnts
    #global block_depth
    global fieldID
    global methodID
    global varID
    global conID
    global currentClass

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
        if type(record) is ast.ConstructorRecord:
            record.containingClass = currentClass
            record.id = conID
            conID = conID + 1
            p[0].constructors.append(record)
        elif type(record) is ast.MethodRecord:
            record.containingClass = currentClass
            record.id = methodID
            methodID = methodID + 1
            p[0].methods.append(record)
        else:   # record must be a list of fields
            for field in record:
                field.containingClass = currentClass
                field.id = fieldID
                fieldID = fieldID + 1
                p[0].fields.append(field)


    # debug.print_p(p, msg="Printing p from class_decl")
    tree.add_class(p[0])

# done
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
# this is a little sus
# I feel like something needs to be done here
# scope things and variable table things
def p_var_decl(p):
    '''var_decl : type variables ';' '''
    p[0] = {"type" : p[1], "variables" : p[2]}

# done
def p_variables(p):
    '''variables : variable
                 | variable ',' variables'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

# done
def p_variable(p):
    '''variable  : ID '''
    p[0] = p[1]

# done
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
        applicability = 'static'
    else:
        applicability = 'instance'

    var_decl = p[2]
    type = var_decl["type"]
    p[0] = []
    if var_decl["variables"] is not None:
        for var in var_decl["variables"]:
            field = ast.FieldRecord(name = var, id = 1, containingClass= currentClass, visibility= visibility, applicability= applicability, type= type)
            p[0] += [field]

# TODO: method_body variable table
def p_method_decl(p):
    '''method_decl      : modifier type ID '(' optional_formals ')' block
                        | modifier VOID ID '(' optional_formals ')' block'''

    # never set but needs to be
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

    varID = 1
    variableTable = []
    for param in parameters:
        param.id = varID
        varID = varID + 1
        variableTable.append(param)

    # TODO replace empty list with variable table
    p[0] = ast.MethodRecord(name= p[3], id=1, containingClass=currentClass
    , visibility=visibility, applicability=applicability, body=method_body
    , variableTable = variableTable, returnType=methodType, parameters=parameters)

# done
def p_optional_formals(p):
    '''optional_formals : formals
                        | empty'''
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]

# done
def p_formals(p):
    '''formals  : formal_param
                | formal_param ',' formals'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    if len(p) == 2:
        p[0] = [p[1]]

# TODO: field_id, variable table, field_id again
def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = ast.VariableRecord(name = p[2], id = 1, kind = "formal", type= p[1])

# A method declaration with modifiers, return type, method name, and optional parameters
# A constructor declaration with modifiers, class name, and optional parameters
# TODO: method_body variable table
def p_constructor_decl(p):
    '''constructor_decl : modifier ID '(' optional_formals ')' block'''

    visibility = ''
    modifiers = p[1]

    if 'public' in modifiers:
        visibility = 'public'
    else:
        visibility = 'private'

    parameters = p[4]
    body = p[6]
    varID = 1
    variableTable = []
    for param in parameters:
        param.id = varID
        varID = varID + 1
        variableTable.append(param)

    p[0] = ast.ConstructorRecord(id=1, visibility=visibility, parameters=parameters,variableTable=variableTable, body=body)

# TODO include line range
def p_block(p):
    '''block : '{' optional_stmts '}'
             | '{' '}'
    '''
    # create block object
    p[0] = ast.Statement()
    p[0].kind = 'Block'
    # { }
    if len(p) == 3:
        p[0].attributes['stmnts'] = []
    else:
        p[0].attributes['stmnts'] = p[2]

# if there are ordering problems check this recursion magic
# returns a list of statements
def p_optional_stmts(p):
    '''optional_stmts : stmt optional_stmts
                       | empty'''
    if len(p) == 3:
        if p[2] is None: # stmnt + empty
            p[0] = [p[1]]
        else: # stmnt + optional_stmts
            p[0] = [p[1]] + p[2]
    else: # empty
        p[0] = []


# TODO line range, var_decl?
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
    '''

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
        p[0].kind = 'Return'
        p[0].attributes.update({'return-expression': p[2]})
    elif len(p) == 3 and type(p[1]) is ast.Expression and p[2] == ';': # expr-stmnt
        p[0].kind = 'Expr'
        p[0].attributes.update({'expression': p[1]})
    elif p[1] == 'break':
        p[0].kind = 'Break'
    elif p[1] == 'continue':
        p[0].kind = 'Continue'
    elif type(p[1]) is ast.Statement and p[1].kind == 'Block':
        p[0] = p[1]
    # skip statement?

    # adding line range?

# needed to keep consistent typing
def p_optional_expr(p):
    '''
    optional_expr   : expr
                    | empty
    optional_stmt_expr : stmt_expr
                    | empty
    '''
    p[0] = p[1]

# works and prints correctly when tested on its own
def p_literal(p):
    '''
    literal : INT_CONST
               | FLOAT_CONST
               | STRING_CONST
               | NULL
               | TRUE
               | FALSE
    '''

    p[0] = ast.Expression()
    p[0].kind = "Constant"
    const_expr = ast.Expression() # inner expression for printing
    values = ['true', 'false', 'null']

    # setting the inner expression type
    if type(p[1]) is int:
        const_expr.kind = "Integer-constant"
    elif type(p[1]) is float:
        const_expr.kind = "Float-constant"
    elif type(p[1]) is str and p[1] not in values:
        const_expr.kind = "String-constant"
    else:
        # null, true, false
        const_expr.kind = p[1] 

    # adding value for ints, floats, and strings    
    if p[1] not in values: 
        const_expr.attributes.update({"value": p[1]})

    p[0].attributes.update({"Expression": const_expr})

# works when tested on its own
# check to make sure unary expr and ops are done correctly
def p_expr(p):
    '''
    expr : primary
         | assign
         | expr arith_op expr
         | expr bool_op expr
         | unary_op expr
    '''
    p[0] = ast.Expression()

    if len(p) == 2: # primary or assign
        p[0] = p[1]
    elif len(p) == 3: # unary
        p[0].kind = "Unary"
        p[0].attributes.update({"operator": p[1]})
        p[0].attributes.update({"operand": p[2]})
    elif len(p) == 4: # arith or bool op (Binary)
        p[0].kind = "Binary"
        p[0].attributes.update({"operator": p[2]})
        p[0].attributes.update({"operand1": p[1]})
        p[0].attributes.update({"operand2": p[3]})

# works when tested individually
# TODO resolve what the single ID is supposed to do
#   what is supposed to be returned with just ID?
# all programs will ALWAYS have len == 4
# i.e. x = 2 will never be encountered
# only this.x = 2 or class.x = 2 will happen
# check out the Scopes section on the hw doc
# primary in this case can only be a
# this, super, or a class
# For assign, field_access needs to 
# be either Field-access or Variable(table index)
def p_field_access(p):
    '''
    field_access : primary '.' ID
                 | ID
    '''
    p[0] = ast.Expression()
    p[0].kind = "Field-access"
    if len(p) == 4:
        p[0].attributes.update({"base": p[1]})
        p[0].attributes.update({"field-name": p[3]})
    else: 
        # this is in response to resolving to just ID
        # it sometimes works, sometimes doesn't
        # I think this gets overloaded and creates uninitended behavior
        # e.g. variables being used now have a 'This' prepended
        # Using the Out class for methods will result in This.Out
        # as opposed to just Out
        p[0].attributes.update({"base": ast.Expression(kind='This')})
        p[0].attributes.update({"field-name": p[1]})
        # @SEAN is field access supposed to resolve to 1 id?

# parses assign and auto expressions   
# works when testing individually
# TODO work on dealing with field_access
def p_assign_auto(p):
    '''
    assign : field_access ASSIGN expr
            | field_access INCREMENT
            | INCREMENT field_access
            | field_access DECREMENT
            | DECREMENT field_access
    '''
    p[0] = ast.Expression()
    ops = {
        '++': 'inc',
        '--': 'dec'
    }
    if len(p) == 3:
        order = "invalid" # field_access ambiguity
        # Auto
        p[0].kind = "Auto"
        if type(p[1]) is ast.Expression:
            order = 'post'
            p[0].attributes.update({"operand": p[1]})
            p[0].attributes.update({"operation": ops[p[2]]})
        elif type(p[2]) is ast.Expression:
            order = 'pre'
            p[0].attributes.update({"operand": p[2]})
            p[0].attributes.update({"operation": ops[p[1]]})

        p[0].attributes.update({"order": order})
    else:
        # Assign
        p[0].kind = "Assign"
        # this check is needed bc it can be just ID
        # so uh field_access rule needs to be checkout out
        # p[1] should be an expression that is a Field-access or Variable(table index)
        if type(p[1]) is ast.Expression:
            p[0].attributes.update({"left": p[1]})
        p[0].attributes.update({"right": p[3]})

# I think field access and method prefix needs to be reworked
# since the base and method name are needed
# this.method() => {base: ast.Expression(kind='This'), method-name: "method"}
# actually, methods are only used in conjunction with class/object
# so never just func(), always this.func() or class.func()
# note that field_access might sometimes return Variable(table index)
# unless the design is changed
# TODO fix the grammar then implement
def p_method_invocation(p):
    '''
    method_invocation : field_access '(' arguments ')'
                    | field_access '(' ')'
    '''
    p[0] = ast.Expression()
    p[0].kind = "Method-call"

    if type(p[1]) is ast.Expression:
        p[0].attributes.update({"base": p[1].attributes['base']})
        p[0].attributes.update({"method-name": p[1].attributes['field-name']})

    if len(p) == 5: # including args
        p[0].attributes.update({"arguments": p[3]})

# let arguments be a [list] of expressions
def p_arguments(p):
    '''
    arguments : expr
              | expr ',' arguments
    '''
    p[0] = []
    p[0].append(p[1])
    # add list of prev expr to current list
    if len(p) == 4:
        p[0] += p[3]

# TODO: class ref, var
def p_expressions(p):
    '''
    primary : literal
            | THIS
            | SUPER
            | '(' expr ')'
            | NEW ID '(' arguments ')'
            | NEW ID '(' ')'
            | field_access
            | method_invocation
    stmt_expr : assign
              | method_invocation'''

    p[0] = ast.Expression()

    if len(p) == 2:
        if p[1] == "this":
            p[0].kind = "This"
        elif p[1] == "super":
            p[0].kind = "Super"
        else:
            # literal, field_access, assign, method_invocation
            p[0] = p[1]
    elif p[1] == 'new':
        # New-object
        p[0].kind = "New-object"
        p[0].attributes.update({"class-name": p[2]})
        if type(p[4]) is list:
            p[0].attributes.update({"arguments": p[4]})
    elif len(p) == 4:
        # ( expr )
        p[0] = p[2]

    # added to prevent the expression template code from running
    value = True
    if value:
        return

    # Var
    # might have something to do with field_access id
    # ***Remember to change the indices!***
    # scoping rules for variables with the same name
    # needs to be handled somewhere
    p[0].kind = "Var"
    if type(p[1]) is ast.VariableRecord:
        p[0].attributes.update({"ID": p[1].id})

    # Class-reference
    # might be used when using method prefix instead of field_access
    # ***Remember to change the indices!***
    p[0].kind = "Class-reference"
    # denotes the value of literal class names
    if type(p[1]) is str:
        p[0].attributes.update({"class-name": p[1]})

# returns the string value of whatever operator is read in p[1]
def p_binary_op(p):
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
            | GEQ"""

    bin_operands = {
        "+": "add",
        "-": "sub", 
        "*": "mul", 
        "/": "div", 
        "&&": "and", 
        "||": "or", 
        "==": "eq", 
        "!=": "neq", 
        "<": "lt", 
        "<=": "leq", 
        ">": "gt", 
        ">=": "geq"
    }
    p[0] = bin_operands[p[1]]

def p_unary_op(p):
    '''
    unary_op : PLUS
            | MINUS
            | NOT
    '''
    un_ops = {
        "-": "uminus",
        "!": "neg"
    }
    p[0] = un_ops[p[1]]

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