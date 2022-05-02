# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

'''
    Evaluates type constraints for name resolution
'''

currClass = None
currFunc = None
tree = None
base_types = ['int', 'float', 'boolean', 'string']

# checks the types of the ast input
def check_types(ast):
    global currClass
    global tree
    tree = ast
    
    # deep copy of classes array
    classes = []
    for i in range(2, len(tree.classes)):
        classes.append(tree.classes[i])

    while len(classes) > 0:
        currClass = classes.pop()

        check_funcs(currClass.constructors)

        check_funcs(currClass.methods)

    return

# type checks function like strucutures
# (constructors and methods)
def check_funcs(funcs):
    global currFunc
    for func in funcs:
        currFunc = func
        check_block(func.body)
    return

def check_block(block):
    block_queue = [block]
    while len(block_queue) != 0:
        block = block_queue.pop()
        block_queue += block.attributes['inner-blocks']
        tc_block(block)
    return

# returns whether the block is type correct (tc)
def tc_block(block):
    for stmt in block.attributes['stmnts']:
        if not tc_stmt(stmt):
            block.isTypeCorrect = False
            return False # comment out to keep things running
            # causes issues with overloaded Out class
            # everything after an out class call
            # doesn't get its type checked

    block.isTypeCorrect = True
    return True

# returns whether a stmt is type correcet
def tc_stmt(stmt):
    if type(stmt) is list:
        # skip over variable record declarations
        return True
    elif stmt.kind == 'If':
        # condition is boolean
        condition = stmt.attributes['condition']
        stmt.isTypeCorrect = tc_expr(condition)
        if not stmt.isTypeCorrect or condition.type != 'boolean':
            stmt.isTypeCorrect = False
            return False

        # then is type correct
        if stmt.isTypeCorrect:
            expr = stmt.attributes['then']
            if expr.kind == 'Block':
                stmt.isTypeCorrecet = tc_block(expr)
            else:
                stmt.isTypeCorrect = tc_expr(expr)

        # else is type correct
        c = True
        if 'else' in stmt.attributes.keys():
            expr = stmt.attributes['else']
            if expr.kind == 'Block':
                c = tc_block(expr)
            else:
                c = tc_expr(stmt.attributes['else'])

        stmt.isTypeCorrect = c
    elif stmt.kind == 'While':
        # condition is boolean
        condition = stmt.attributes['loop-condition']
        stmt.isTypeCorrect = tc_expr(condition)
        if not stmt.isTypeCorrect or condition.type != 'boolean':
            stmt.isTypeCorrect = False
            return False

        # body is type correct
        stmt.isTypeCorrect = tc_expr(stmt.attributes['loop-body'])
    elif stmt.kind == 'For':
        # condition is boolean
        condition = stmt.attributes['loop-condition']
        stmt.isTypeCorrect = tc_expr(condition)
        if not stmt.isTypeCorrect or condition.type != 'boolean':
            stmt.isTypeCorrect = False
            return False

        # init expr tc
        if stmt.isTypeCorrect:
            stmt.isTypeCorrect = tc_expr(stmt.attributes['initialize-expression'])

        # update expr tc
        if stmt.isTypeCorrect:
            stmt.isTypeCorrect = tc_expr(stmt.attributes['update-expression'])

        # body expr tc
        if stmt.isTypeCorrect:
            stmt.isTypeCorrect = tc_expr(stmt.attributes['loop-body'])

    elif stmt.kind == 'Return':
        if 'return-expression' in stmt.attributes.keys():
            # TODO should there be an error if 
            # a return is found in a constructor?
            # ret type of the current method
            ret_type = ''
            if currFunc.returnType.name not in base_types:
                ret_type = 'user(' + currFunc.returnType.name + ')'
            else:
                ret_type = currFunc.returnType.name

            # expr must be type correct
            expr = stmt.attributes['return-expression']
            stmt.isTypeCorrect = tc_expr(expr)
            
            # type must be subtype of declared return type
            if stmt.isTypeCorrect and expr != None:
                stmt.isTypeCorrect = is_subtype(expr.type, ret_type)
        else:
            # expr must be empty if method type is void and vice versa
            stmt.isTypeCorrect = ret_type == 'void'
    elif stmt.kind == 'Expr':
        stmt.isTypeCorrect = tc_expr(stmt.attributes['expression'])
    elif stmt.kind == 'Block':
        # skips blocks since they're dealt with in tc_block
        # assumes they're valid
        return True
    else:
        # Breaks, continues, skips
        stmt.isTypeCorrect = True
    
    return stmt.isTypeCorrect

# sets the expr type to error
# can be used for future type error handling
def tc_expr_err(expr):
    expr.type = 'error'
    expr.isTypeCorrect = False

# checks and sets the type of the expr
# returns whether an expr is type correct
def tc_expr(expr):
    if expr == None:
        return True # skip empties
    if expr.kind == 'Constant':
        tc_constant(expr)
    elif expr.kind == 'Variable':
        tc_var(expr)
    elif expr.kind == 'Unary':
        tc_unary(expr)
    elif expr.kind == 'Binary':
        tc_binary(expr)
    elif expr.kind == 'Assign':
        tc_assign(expr)
    elif expr.kind == 'Auto':
        tc_auto(expr)
    elif expr.kind == 'Field-access':
        tc_field(expr)
    elif expr.kind == 'Method-call':
        tc_method_call(expr)
    elif expr.kind == 'New-object':
        tc_new_obj(expr)
    elif expr.kind == 'This':
        expr.type = 'user(' + currClass.name + ')'
        expr.isTypeCorrect = True
    elif expr.kind == 'Super':
        if currClass.superName != '':
            expr.type = 'user(' + currClass.superName + ')'
            expr.isTypeCorrect = True
        else:
            tc_expr_err(expr)
    elif expr.kind == 'Class-reference':
        tc_class_ref(expr)

    return expr.isTypeCorrect

def tc_constant(expr):
    # setting types for this and inner expr
    const_expr = expr.attributes['Expression']
    if const_expr.kind == 'Integer-constant':
        expr.type = 'int'
        const_expr.type = 'int'
    elif const_expr.kind == 'Float-constant':
        expr.type = 'float'
        const_expr.type = 'float'
    elif const_expr.kind == 'String-constant':
        expr.type = 'string'
        const_expr.type = 'string'
    elif const_expr.kind == 'true' or const_expr.kind == 'false':
        expr.type = 'boolean'
        const_expr.type = 'boolean'
    elif const_expr.kind == 'null':
        expr.type = 'null'
        const_expr.type = 'null'
    
    # setting type correctess
    if expr.type != None and const_expr.type != None:
        expr.isTypeCorrect = True
        const_expr.isTypeCorrect = True
    else:
        tc_expr_err(expr)

def tc_var(expr):
    # type is the same as what it was declared
    global currFunc
    vtable = currFunc.variableTable
    for vr in vtable:
        if vr.id == expr.attributes['id']:
            # class name
            if vr.type.name not in base_types:
                expr.type = 'user(' + vr.type.name + ')'
            else:
                expr.type = vr.type.name
            expr.isTypeCorrect = True
            return
    tc_expr_err(expr)

def tc_unary(expr):
    operand = expr.attributes['operand']
    tc_expr(operand)
    op = None
    if 'operator' in expr.attributes.keys():
        op = expr.attributes['operator']
    if op == 'uminus':        
        # valid if e is int or float, error otherwise
        if operand.type == 'int' or operand.type == 'float':
            expr.type = operand.type
            expr.isTypeCorrect = True
        else:
            tc_expr_err(expr)
    elif op == 'neg':
        # valid if e is boolean, error otherwise
        if operand.type == 'boolean':
            expr.type = operand.type
            expr.isTypeCorrect = True
        else:
            tc_expr_err(expr)       
    else:
        # + or no operand? 
        expr.type = operand.type
        expr.isTypeCorrect = operand.isTypeCorrect

def tc_binary(expr):
    arith_ops = ['add', 'sub', 'mul', 'div']
    bool_ops = ['and', 'or'] # boolean
    arith_comp = ['lt', 'leq', 'gt', 'geq'] # boolean
    eq_comp = ['eq', 'neq'] # boolean

    operator = expr.attributes['operator']
    op1 = expr.attributes['operand1']
    tc_expr(op1)
    op2 = expr.attributes['operand2']
    tc_expr(op2)

    if operator in arith_ops:
        # int if both int, float if at least one is float
        valid_types = ['float', 'int']
        if op1.type == 'int' and op2.type == 'int':
            expr.type = 'int'
            expr.isTypeCorrect = True
        elif op1.type in valid_types and op2.type in valid_types:
            expr.type = 'float'
            expr.isTypeCorrect = True
        else:
            tc_expr_err(expr)
    elif operator in bool_ops or operator in arith_comp:
        valid_types = []
        if operator in bool_ops:
            # boolean if both are boolean
            valid_types = ['boolean']
        else:
            # boolean if both have int or float
            valid_types = ['int', 'float']
        if op1.type in valid_types and op2.type in valid_types:
            expr.type = 'boolean'
            expr.isTypeCorrect = True
        else:
            tc_expr_err(expr)
    elif operator in eq_comp:
        # if one is a subtype of the other
        if is_subtype(op1.type, op2.type) or is_subtype(op2.type, op1.type):
            expr.type = 'boolean'
            expr.isTypeCorrect = True
        else:
            tc_expr_err(expr)
    else:
        tc_expr_err(expr)

def tc_assign(expr):
    # e1 = e2
    # expr type = type(e2) iff 
    # e1 and e2 tc
    # e2 subtype e1
    e1 = expr.attributes['left']
    tc_expr(e1)
    e2 = expr.attributes['right']
    tc_expr(e2)
    if e1.isTypeCorrect and e2.isTypeCorrect and is_subtype(e2.type, e1.type):
        expr.type = e2.type
        expr.isTypeCorrect = True
    else:
        tc_expr_err(expr)

    # linking types to printout
    expr.attributes['ltype'] = e1.type
    expr.attributes['rtype'] = e2.type

def tc_auto(expr):
    # same type as e if e is int or float
    op = expr.attributes['operand']
    if not tc_expr(op):
        tc_expr_err(expr)

    valid_types = ['int', 'float']
    if op.type in valid_types:
        expr.type = op.type
        expr.isTypeCorrect = True
    else:
        tc_expr_err(expr)

def tc_field(expr):
    # p.x corresponds to field id z
    # expr.type = z.type iff
    # p.type is user(A) and z is not static or
    # p.type is class-literal(A) and z is static
    # error if conditions not met/name resolution fails

    base = expr.attributes['base']
    fname = expr.attributes['field-name']
    if not tc_expr(base):
        tc_expr_err(expr)
        return

    # get the class name and set applicability conditions
    applicability = ''
    cname = ''
    if 'user' in base.type:
        applicability = 'instance'
        cname = base.type[5:base.type.index(')')]
    elif 'class-literal' in base.type:
        applicability = 'static'
        cname = base.type[14:base.type.index(')')]
    else:
        tc_expr_err(expr)

    # find the corresponding field record
    fr = None
    cr = None
    # current class record
    for c in tree.classes:
        if c.name == cname:
            cr = c
            break
    if cr == None:
        # class doesn't exist!
        tc_expr_err(expr)
        return
    # super class record
    scr = None
    if cr.superName != "":
        for c in tree.classes:
            if cr.superName == c.name:
                scr = c
                break
    # find field record in base class
    for f in cr.fields:
        if f.name == fname:
            fr = f
            break
    # find field record in super class
    if fr == None and scr != None:
        for f in scr.fields:
            if f.name == fname:
                fr = f
                break

    # set tc and name resolution
    if fr != None and fr.applicability == applicability:
        if fr.type.name not in base_types:
            expr.type = 'user(' + fr.type.name + ')'
        else:
            expr.type = fr.type.name
        expr.isTypeCorrect = True
        expr.attributes['id'] = fr.id
    else:
        # field doesn't exist/bad typing
        tc_expr_err(expr)

def tc_method_call(expr):
    # p.f(e1, e2, ...) correspondes with method h
    # expr.type = h.type iff
    # p.type is user(A) and z is not static or
    # p.type is class-literal(A) and z is static
    # error if conditions not met/name resolution fails

    base = expr.attributes['base']
    mname = expr.attributes['method-name']
    args = expr.attributes['arguments']
    if not tc_expr(base):
        tc_expr_err(expr)
        return

    # get the class name and set applicability conditions
    applicability = ''
    cname = ''
    if 'user' in base.type:
        applicability = 'instance'
        cname = base.type[5:base.type.index(')')]
    elif 'class-literal' in base.type:
        applicability = 'static'
        cname = base.type[14:base.type.index(')')]
    else:
        tc_expr_err(expr)

    # find the corresponding method record
    cr = None
    # current class record
    for c in tree.classes:
        if c.name == cname:
            cr = c
            break
    if cr == None:
        # class doesn't exist!
        tc_expr_err(expr)
        return
    # super class record
    scr = None
    if cr.superName != "":
        for c in tree.classes:
            if c.name == cr.superName:
                scr = c
                break
    # method record in original class
    mr = None
    for m in cr.methods:
        if m.name == mname:
            mr = m
            break
    # method record in super class
    if mr == None and scr != None:
        for m in scr.methods:
            if m.name == mname:
                mr = m
                break
    if mr == None:
        # method doesn't exist
        tc_expr_err(expr)
        return

    # applicability: check if every arg is a subtype of 
    # the paramaters in the method definition
    if not is_subtype(args, mr.parameters):
        tc_expr_err(expr)
        return

    # accessibility: check if accessible (public/private)
    if mr.name != currClass.name and mr.visibility == 'private':
        tc_expr_err(expr)
        return

    # set tc and name resolution
    if mr.applicability == applicability:
        if mr.returnType.name not in base_types:
            expr.type = 'user(' + mr.returnType.name + ')'
        else:
            expr.type = mr.returnType.name
        expr.isTypeCorrect = True
        expr.attributes['id'] = mr.id
    else:
        # bad typing
        tc_expr_err(expr)

# TODO name resolution
def tc_new_obj(expr):
    cname = expr.attributes['class-name']
    args = expr.attributes['arguments']
    
    # find class and constructor
    classRecord = None
    constructorRecord = None
    for c in tree.classes:
        if c.name == cname:
            classRecord = c
            break
    if classRecord == None:
        tc_expr_err(expr)
        return
    for r in classRecord.constructors:
        # should there be more checks?
        if len(r.parameters) == len(args):
            constructorRecord = r
            break
    if constructorRecord == None:
        tc_expr_err(expr)
        return

    # applicability: check if args are subtype of constructor args
    if not is_subtype(args, constructorRecord.paramaters):
        tc_expr_err(expr)
        return

    # accessibility: check if public/private
    # add type and name resolution
    if constructorRecord.visibility == "public" or constructorRecord.visibility == "":
        expr.type = 'user(' + cname + ')'
        expr.isTypeCorrect = True
        expr.attributes['id'] = constructorRecord.id
    else:
        tc_expr_err(expr)    

def tc_class_ref(expr):
    # find the class record
    cname = expr.attributes['class-name']
    cr = None
    for c in tree.classes:
        if c.name == cname:
            cr = c
            break
    
    # add type 
    if cr != None:
        expr.type = 'class-literal(' + cname + ')'
        expr.isTypeCorrect = True
    else:
        # class doesn't exist!
        tc_expr_err(expr)

# returns whether type1 is a subtype of type2
def is_subtype(type1, type2):

    # if all elements in list1 are subtypes of the
    # corresponding elements in list2
    # t1 is a list of expressions
    # t2 is a list of variable records
    if type(type1) is list and type(type2) is list:
        if len(type1) != len(type2):
            return False
        for i in range(0, len(type1)):
            tc_expr(type1[i])
            t1 = type1[i].type
            t2 = type2[i].type.name
            if not is_subtype(t1, t2):
                return False
        return True

    # Type T is a subtype of itself (i.e., the subtype relation is reflexive).
    if type1 == type2:
        return True
    
    # int is a subtype of float
    if type1 == 'int' and type2 == 'float':
        return True

    # null is a subtype of user(A) for any class A
    if type1 == 'null' and 'user' in type2:
        return True

    classA = None
    classB = None
    if 'user' in type1 and 'user' in type2:
        classA = type1[5:type1.index(')')]
        classB = type2[5:type2.index(')')]
    elif 'class-literal' in type1 and 'class-literal' in type2:
        classA = type1[14:type1.index(')')]
        classB = type2[14:type1.index(')')]
    
    # user(A) is a subtype of user(B) if A is a subclass of B.
    # class-literal(A) is a subtype of class-literal(B) if A is a subclass of B.
    if classA != None and classB != None:
        for c in tree.classes:
            if c.name == classA:
                return c.superName == classB
    
    return False