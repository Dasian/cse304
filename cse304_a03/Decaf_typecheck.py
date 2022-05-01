'''
    Evaluates type constraints for name resolution
'''

import decaf_ast
from decaf_parser import tree

currClass = None
currFunc = None

# checks the types of the ast input
def check_types():
    global currClass
    classes = tree.classes

    while len(classes) > 2:
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
            return False

    block.isTypeCorrect = True
    return True

# returns whether a stmt is type correcet
def tc_stmt(stmt):
    if stmt.kind == 'If':
        # condition is boolean
        condition = stmt.attributes['condition']
        stmt.isTypeCorrect = tc_expr(condition)
        if not stmt.isTypeCorrect or condition.type != 'boolean':
            stmt.isTypeCorrect = False
            return False

        # then is type correct
        if stmt.isTypeCorrect:
            stmt.isTypeCorrect = tc_expr(stmt.attributes['then'])

        # else is type correct
        c = True
        if 'else' in stmt.attributes.keys():
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
            ret_type = currFunc.returnType.name

            # expr must be type correct
            expr = stmt.attributes['return-expression']
            stmt.isTypeCorrect = tc_expr(expr)
            
            # type must be subtype of declared return type
            if stmt.isTypeCorrect:
                stmt.isTypeCorrect = is_subtype(expr.type, ret_type)
        else:
            # expr must be empty if method type is void and vice versa
            stmt.isTypeCorrect = ret_type == 'void'
    elif stmt.kind == 'Expr':
        stmt.isTypeCorrect = tc_expr(stmt.attributes['expression'])
    
    return stmt.isTypeCorrect

# returns whether an expr is type correct
def tc_expr(expr):
    if expr.kind == 'Constant':
        const_expr = expr.attributes['Expression']
    elif expr.kind == 'Variable':
        return 
    elif expr.kind == 'Unary':
        return
    elif expr.kind == 'Binary':
        return
    elif expr.kind == 'Assign':
        # TODO link types
        expr.attributes['ltype'] = 'error'
        expr.attributes['rtype'] = 'error'
    elif expr.kind == 'Auto':
        return
    elif expr.kind == 'Field-access':
        # TODO link this to corresponding field id
        expr.attributes['id'] = -1
        return
    elif expr.kind == 'Method-call':
         # TODO connect methodID
        expr.attributes['id'] = -1
    elif expr.kind == 'New-object':
        # TODO link this to corresponding constructor id
        expr.attributes['id'] = -1
    elif expr.kind == 'This':
        return
    elif expr.kind == 'Super':
        return
    elif expr.kind == 'Class-reference':
        return
    return expr.isTypeCorrect

# returns whether type1 is a subtype of type2
def is_subtype(type1, type2):
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