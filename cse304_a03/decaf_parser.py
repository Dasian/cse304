# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

#  PLY/yacc parser specification file

import ply.yacc as yacc
from decaf_lexer import tokens
import decaf_lexer as lexer
import decaf_ast as ast


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


def p_class_id(p):
    '''
    class_id : ID
    '''
    global currentClass
    currentClass = p[1]
    p[0] = p[1]

# done
# The class declaration with or without inheritance and one or more class body declarations
def p_class_decl(p):
    '''class_decl : CLASS class_id EXTENDS ID '{' class_body_decl '}'
                  | CLASS class_id '{' class_body_decl '}'
                  '''
    # Reset Global vars
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

# TODO add void, class literal, error, and null
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
# causes printing errors when returned to stmt
# will need to add to variable table (i think)
def p_var_decl(p):
    '''var_decl : type variables ';' '''
    p[0] = []
    for var_name in p[2]:
        p[0] += [ast.VariableRecord(name = var_name, id = -1, kind = "local", type = p[1])]

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

    variables = p[2]     # list of VariableRecords
    type = variables[0].type
    p[0] = []
    for var in variables:
        field = ast.FieldRecord(name = var.name, id = var.id, containingClass= currentClass, visibility= visibility, applicability= applicability, type= type)
        p[0] += [field]

# TODO fix variableTable to include nested vars
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

    # adding formals
    vtable = []
    for param in parameters:
        param.kind = "formal"
        vtable.append(param)

    # adding local vars
    block_queue = [method_body]
    while len(block_queue) != 0:
        block = block_queue.pop()
        block_queue += block.attributes['inner-blocks']
        vtable += block.attributes['vtable']
    
    # creating var ids for the vtable
    id = 1
    for vr in vtable:
        if vr.kind != 'formal':
            vr.kind = 'local'
        vr.id = id
        id += 1

    # add var ids to the expression objects within this method
    add_var_ids(body=method_body, variableTable=vtable)

    p[0] = ast.MethodRecord(name= p[3], id=1, containingClass=currentClass
    , visibility=visibility, applicability=applicability, body=method_body
    , variableTable = vtable, returnType=methodType, parameters=parameters)

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

# done
def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = ast.VariableRecord(name = p[2], id = 1, kind = "formal", type= p[1])

# TODO fix variableTable to include nested variables
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

    # adding formals
    vtable = []
    for param in parameters:
        param.kind = "formal"
        vtable.append(param)

    # adding local vars
    block_queue = [body]
    while len(block_queue) != 0:
        block = block_queue.pop()
        block_queue += block.attributes['inner-blocks']
        vtable += block.attributes['vtable']
    
    # creating var ids for the vtable
    id = 1
    for vr in vtable:
        if vr.kind != 'formal':
            vr.kind = 'local'
        vr.id = id
        id += 1

    # adding var ids to the expression objects in this constructor
    add_var_ids(body=body, variableTable=vtable)

    p[0] = ast.ConstructorRecord(id=1, visibility=visibility, parameters=parameters,variableTable=vtable, body=body)

# fills variable ids into the proper expression
def add_var_ids(body=None, variableTable=None):
    if body == None or variableTable == None:
        return

    # adding method/constructor params to outermost block vtable
    new_vtable = body.attributes['vtable']
    formal_vrs = []
    for vr in variableTable:
        if vr.kind == 'formal':
            formal_vrs.append(vr)
    new_vtable += formal_vrs
    body.attributes['vtable'] = new_vtable

    # for every block
    # place the id into the variable expression
    block_queue = [body]
    while len(block_queue) != 0:

        block = block_queue.pop(0)

        # block statement objects found within the current block
        block_queue += block.attributes['inner-blocks']
        
        # list of variable expression objects present in the current block
        var_stmnts = block.attributes['var-exprs']

        # dict of variable record objects available to this block
        # includes outer scopes
        # key is priority (start at 0 and has most priority)
        # value is list of variable record objects 
        available_vars = {}
        i = 1
        max = -1
        available_vars[0] = block.attributes['vtable']
        curr_block = block.attributes['outer-block']
        while curr_block != None:
            available_vars[i] = curr_block.attributes['vtable']
            curr_block = curr_block.attributes['outer-block']
            i += 1
        max = i
        
        # for every variable expression
        # find the nearest variable record with the same name
        # and fill in the id
        # includes outer blocks 
        # skips variables not found in the scope
        # stmt should always be a Variable expression object
        for stmt in var_stmnts:
            target = stmt.attributes['vname']
            level = 0
            found = False
            # match variable record to target
            while level <= max:
                for vr in available_vars[level]:
                    if vr.name == target:
                        # update variable expr to match id
                        id = vr.id
                        stmt.attributes['id'] = id
                        found = True
                        break
                if found:
                    break
                # an error can be thrown here if variable
                # isn't found in variable table
                level += 1

# done
def p_block(p):
    '''block : '{' optional_stmts '}'
    '''
    # block statement object
    p[0] = ast.Statement()
    p[0].kind = 'Block'
    p[0].attributes['stmnts'] = p[2]

    # vtable: list of variable records defined at the beginning of this block
    # fills vtable and inits stmt_queue
    stmt_queue = []
    vtable = []
    for stmt in p[2]:
        if type(stmt) is list:
            for vr in stmt:
                vtable.append(vr)
        else:
            stmt_queue.append(stmt)
    p[0].attributes['vtable'] = vtable

    # inner blocks: list of block expr objects inside this one
    # fills inner_blocks, stmt_queue
    # inits expr_queue
    inner_blocks = []
    expr_queue = []
    while len(stmt_queue) != 0:
        stmt = stmt_queue.pop()
        if stmt.kind == 'Block':
            inner_blocks.append(stmt)
        elif stmt.kind == 'If':
            stmt_queue.append(stmt.attributes['then'])
            expr_queue.append(stmt.attributes['condition'])
            if 'else' in stmt.attributes.keys():
                stmt_queue.append(stmt.attributes['else'])
        elif stmt.kind == 'While':
            stmt_queue.append(stmt.attributes['loop-body'])
            expr_queue.append(stmt.attributes['loop-condition'])
        elif stmt.kind == 'For':
            stmt_queue.append(stmt.attributes['loop-body'])
            expr_queue.append(stmt.attributes['initialize-expression'])
            expr_queue.append(stmt.attributes['loop-condition'])
            expr_queue.append(stmt.attributes['update-expression'])
        elif stmt.kind == 'Return':
            expr_queue.append(stmt.attributes['return-expression'])
        elif stmt.kind == 'Expr':
            expr_queue.append(stmt.attributes['expression'])
    p[0].attributes['inner-blocks'] = inner_blocks


    # outer block: block expr object this block is inside (parent/prev or None)
    # should be filled when the outer blocks are complete
    # outermost block should have this attr as None
    p[0].attributes['outer-block'] = None
    for block in inner_blocks:
        block.attributes.update({'outer-block': p[0]})
    
    # var-exprs: list of var expr objects in this block
    var_exprs = []
    while len(expr_queue) != 0:
        expr = expr_queue.pop()
        if expr is None:
            continue
        if expr.kind == 'Variable':
            var_exprs.append(expr)
        elif expr.kind == 'Auto' or expr.kind == 'Unary':
            expr_queue.append(expr.attributes['operand'])
        elif expr.kind == 'Assign':
            expr_queue.append(expr.attributes['left'])
            expr_queue.append(expr.attributes['right'])            
        elif expr.kind == 'Binary':
            expr_queue.append(expr.attributes['operand1'])
            expr_queue.append(expr.attributes['operand2'])
        elif expr.kind == 'Method-call' or expr.kind == 'New-object':
            if 'arguments' in expr.attributes.keys():
                for e in expr.attributes['arguments']:
                    expr_queue.append(e)
            if expr.kind == 'Method-call':
                expr_queue.append(expr.attributes['base'])
    p[0].attributes['var-exprs'] = var_exprs

    # line range
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]     # From the left bracket to the right bracket



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


# done
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
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]

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
    elif type(p[1]) is list and len(p[1]) != 0:      # IF variable declaration, return list of variables
        p[0] = p[1]
    else:
        p[0].kind = 'Skip'

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
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]

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
def p_expr(p):
    '''
    expr : primary
         | assign
         | expr arith_op expr
         | expr bool_op expr
         | unary_op expr
    '''
    p[0] = ast.Expression()
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]

    if len(p) == 2: # primary or assign
        p[0] = p[1]
    elif len(p) == 3: # unary
        p[0].kind = "Unary"
        if p[1] != "":
            p[0].attributes.update({"operator": p[1]})
        p[0].attributes.update({"operand": p[2]})
    elif len(p) == 4: # arith or bool op (Binary)
        p[0].kind = "Binary"
        p[0].attributes.update({"operator": p[2]})
        p[0].attributes.update({"operand1": p[1]})
        p[0].attributes.update({"operand2": p[3]})

def p_field_access(p):
    '''
    field_access : primary '.' ID
                 | ID
    '''
    p[0] = ast.Expression()
    p[0].kind = "Field-access"
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]
    if len(p) == 4:
        p[0].attributes.update({"base": p[1]}) # expression
        p[0].attributes.update({"field-name": p[3]}) # str
        # TODO link this to corresponding field id
        p[0].attributes['id'] = -1
    else: 
        # check if id is a class
        if p[1] in tree.get_classes() or p[1] == currentClass:
            p[0].kind = "Class-reference"
            # denotes the value of literal class names
            p[0].attributes.update({"class-name": p[1]})
        else:            
            p[0].attributes.update({"vname": p[1]})
            p[0].kind = "Variable"
            p[0].attributes.update({"id": -1})

# parses assign and auto expressions   
def p_assign_auto(p):
    '''
    assign : field_access ASSIGN expr
            | field_access INCREMENT
            | INCREMENT field_access
            | field_access DECREMENT
            | DECREMENT field_access
    '''
    p[0] = ast.Expression()
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]
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
        p[0].attributes.update({"left": p[1]})
        p[0].attributes.update({"right": p[3]})

        # TODO link types
        p[0].attributes['ltype'] = 'error'
        p[0].attributes['rtype'] = 'error'

# should work
# TODO: test with class names that don't exist
# TODO: test with objects that do/don't exist
def p_method_invocation(p):
    '''
    method_invocation : field_access '(' arguments ')'
                    | field_access '(' ')'
    '''
    p[0] = ast.Expression()
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]
    p[0].kind = "Method-call"

    if p[1].kind == 'Field-access':
        p[0].attributes.update({"base": p[1].attributes['base']})
        p[0].attributes.update({"method-name": p[1].attributes['field-name']})

    if len(p) == 5: # including args
        p[0].attributes.update({"arguments": p[3]})
    else:
        p[0].attributes.update({"arguments": []})

    # TODO connect methodID
    p[0].attributes['id'] = -1

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

# done
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
    start_left,end_left = p.linespan(1)    # Start,end lines of the left-most symbol
    start_right,end_right = p.linespan(len(p)-1)    # Start,end lines of the right-most symbol
    p[0].lineRange = [start_left, end_right]

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
        else:
            p[0].attributes.update({"arguments": []})
        # TODO link this to corresponding constructor id
        p[0].attributes['id'] = -1
    elif len(p) == 4:
        # ( expr )
        p[0] = p[2]

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

# done
def p_unary_op(p):
    '''
    unary_op : PLUS
            | MINUS
            | NOT
    '''
    un_ops = {
        "-": "uminus",
        "!": "neg",
        "+": ""
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