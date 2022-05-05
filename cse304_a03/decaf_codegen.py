'''
    Definitions for generating code
'''

'''
    keep a list of all fields and methods as a dict
    where the key is the number in the ast and the key is the 
    label being used 

    match all local vars (say n) to the first n temp registers
    
'''

# returns a (string?) containing the abstract machine code 
# for an expression
def gen_expr(expr):
    return