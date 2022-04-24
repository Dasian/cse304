# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

"""
    hw3
    Takes as input a DECAF file 
    Outputs 
        AST if program or
        Error message of first syntax error (line + col)
"""

import sys
from os.path import exists
import ply.lex as lex
import ply.yacc as yacc
import decaf_ast

# Abstract Syntax Tree Table
"""
    TODO
    Error Checking Section
    Implement Expressions
"""
class AST:

    # Initialize In and Out class
    def __init__(self):
        # list of ClassRecord objects, each of these are the root
        # this is essentially the class table
        self.classes = []

        # In class
        scanInt = decaf_ast.MethodRecord(name="scan_int", id=1, containingClass="In", visibility="public", applicability="static", returnType=decaf_ast.TypeRecord(name="int"))
        scanFloat = decaf_ast.MethodRecord(name="scan_float", id=2, containingClass="In", visibility="public", applicability="static", returnType=decaf_ast.TypeRecord(name="float"))
        inMethods = [scanInt, scanFloat]
        inClass = decaf_ast.ClassRecord(name="In", methods=inMethods)

        # Out class
        i = decaf_ast.VariableRecord(name="i", id=1, kind="formal", type=decaf_ast.TypeRecord(name="int"))
        f = decaf_ast.VariableRecord(name="f", id=2, kind="formal", type=decaf_ast.TypeRecord(name="float"))
        b = decaf_ast.VariableRecord(name="b", id=3, kind="formal", type=decaf_ast.TypeRecord(name="boolean"))
        s = decaf_ast.VariableRecord(name="s", id=4, kind="formal", type=decaf_ast.TypeRecord(name="string"))
        print1 = decaf_ast.MethodRecord(name="print", id=1, containingClass="Out", visibility="public", applicability="static", parameters=[i], variableTable=[i], returnType = decaf_ast.TypeRecord('void'))
        print2 = decaf_ast.MethodRecord(name="print", id=2, containingClass="Out", visibility="public", applicability="static", parameters=[f], variableTable=[f], returnType = decaf_ast.TypeRecord('void'))
        print3 = decaf_ast.MethodRecord(name="print", id=3, containingClass="Out", visibility="public", applicability="static", parameters=[b], variableTable=[b], returnType = decaf_ast.TypeRecord('void'))
        print4 = decaf_ast.MethodRecord(name="print", id=4, containingClass="Out", visibility="public", applicability="static", parameters=[s], variableTable=[s], returnType = decaf_ast.TypeRecord('void'))
        outMethods = [print1, print2, print3, print4]
        outClass = decaf_ast.ClassRecord(name="Out", methods=outMethods)

        # adding classes
        self.classes.append(inClass)
        self.classes.append(outClass)

    # adds class to the tree
    # the class must be completed at this point
    def add_class(self, c):
        self.classes.append(c)

    # prints the contents of the AST
    def print_table(self):
        delimiter = '--------------------------------------------------------------------------'
        print(delimiter)
        i = 0 
        for c in self.classes:
            # disables printing in and out class
            if i < 2:
                i += 1
                continue
            self.print_class(c)
            print(delimiter)

    def print_class(self, c):
        print("Class Name:", c.name)
        print("Superclass Name:", c.superName)
        print("Fields:")
        for f in c.fields:
            self.print_field(f)
        print("Constructors:")
        for constr in c.constructors:
            self.print_constructor(constr)
        print("Methods:")
        for m in c.methods:
            self.print_method(m)

    def print_field(self, f):
        base_types = ['int', 'float', 'boolean']
        type_name = f.type.name
        if type_name not in base_types:
                type_name = 'user(' + str(f.type.name) + ')'
        print("FIELD: "+ str(f.id)+ ', '+ f.name+ ', '+ f.containingClass+ ', '+ f.visibility+ ', '+ f.applicability+ ', '+ type_name)

    def print_constructor(self, c):
        print("CONSTRUCTOR: "+ str(c.id)+ ', '+ c.visibility)

        params = ''
        for p in c.parameters:
            if(params == ''):
                params = str(p.id)
            else:
                params += ', ' + str(p.id)

        print("Constructor Parameters:", params)
        self.print_var_table( c.variableTable)
        print("Constructor Body:")
        self.print_body( c.body)       # commented out for blocks

    def print_method(self, m):
        print("METHOD: "+ str(m.id)+ ', '+ m.name+ ', '+ m.containingClass+ ', '+ m.visibility +', '+ m.applicability+', ' + m.returnType.name)

        params = ''
        for p in m.parameters:
            if(params == ''):
                params = p.id
            else:
                params += ', ' + p.id
        print("Method Parameters:", params)
        self.print_var_table(m.variableTable)
        print("Method Body:")
        self.print_body(m.body) # commented out for blocks


    def print_var_table(self, vt):
        print("Variable Table:")
        base_types = ['int', 'float', 'boolean']
        # type needs to be represented as (int, float, boolean)
        # or user(name)
        # t is a VariableRecord
        # vt is a list of VariableRecords
        for t in vt:
            ty = t.type.name
            if ty not in base_types:
                ty = 'user(' + str(t.type.name) + ')'
            print("VARIABLE "+ str(t.id) + ', '+ t.name + ', ' + t.kind + ', ' + ty)

    # prints the body object
    # input: stmnt is a Statement Object
    def print_body(self, stmnt):
        if stmnt is None:
            return
        content = ''
        if(stmnt.kind == 'Block'):
            content = self.block_str(stmnt.attributes['stmnts'])
        else:
            content = self.stmnt_str(stmnt)
        print(content)
    
    # returns the string of a block to be printed
    # always a sequence of statements
    # input: stmnts is a list of Statement Objects
    def block_str(self, stmnts):
        content = ''
        for stmnt in stmnts:
            if stmnt.kind == 'Block':
                content += self.block_str(stmnt.attributes['stmnts']) + ', '
            else:
                content += self.stmnt_str(stmnt) + ', '
        content = content[0:-2] # delete extra comma and space
        s = "Block ([\n" + content + "\n])"
        return s

    # returns the string of a single statement to be printed
    # can contain expressions or statements as attributes
    # the input statement can't be/isn't a block
    # input: stmnt is a Statement Object
    def stmnt_str(self, stmnt):
        content = ''
        for val in stmnt.attributes.values():
            if type(val) is decaf_ast.Statement:
                if val.kind == 'Block':
                    content += self.block_str(val.attributes['stmnts'])
                else:
                    content += self.stmnt_str(val)
            elif type(val) is decaf_ast.Expression:
                content += self.expr_str(val)
            else:
                content += val
            content += ', '
        # remove () for statements without attributes
        if content == '':
            s = stmnt.kind
        else:
            s = stmnt.kind +'(' + content[0:-2] + ')' # delete extra comma and space
        return s

    # returns the string of an expression to be printed
    # attribute values can only be other expressions/list of expressions, not a statement
    def expr_str(self, expr):
        content = ''
        for val in expr.attributes.values():
            if type(val) is decaf_ast.Expression:
                content += self.expr_str(val)
            elif type(val) is list:
                content += self.expr_list_str(val)
            else:
                content += val
            content += ', '
        # remove () for expressions without attribute values
        if content == '':
            s = expr.kind
        else:
            s = expr.kind + '(' + content[0:-2] + ')'
        return s

    # returns the string of a list of expressions to be printed
    def expr_list_str(self, list):
        content = ''
        for expr in list:
            content += self.expr_str(expr)
        return content


def main():
    if len(sys.argv) != 2:  # Takes input from cmdline
        print("USAGE: python3 decaf_checker.py [filename]")
        exit()
    filename = sys.argv[1]
    if not exists(filename):
        print("File not found")
        exit()

    import decaf_lexer
    import decaf_parser
    lexer = lex.lex(module=decaf_lexer)
    parser = yacc.yacc(module=decaf_parser)

    file = open(filename, 'r')
    file_string = file.read()
    file.close()

    parser.parse(file_string, lexer=lexer)


if __name__ == "__main__":
    main()
