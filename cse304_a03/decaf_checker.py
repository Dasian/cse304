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
        self.classes = []
        
        # In class
        inClass = decaf_ast.ClassRecord()

        # Out class
        outClass = decaf_ast.ClassRecord()

        # adding classes
        self.classes.push(inClass)
        self.classes.push(outClass)

    # adds class to the tree
    # the class must be completed at this point
    def add_class(self, c):
        self.classes.append(c)

    # prints the contents of the AST
    def print_table(self):
        delimiter = '--------------------------------------------------------------------------'
        for c in self.classes:
            print(delimiter)
            self.print_class(self, c)
            print(delimiter)

    def print_class(self, c):
        print("Class Name:", c.name)
        print("Superclass Name:", c.superName)
        print("Fields:")
        for f in c.fields:
            self.print_field(self, f)
        print("Constructors:")
        for constr in c.constructors:
            self.print_constructor(self, constr)
        print("Methods")
        for m in c.methods:
            self.print_method(self, m)

    def print_field(self, f):
        print("FIELD:", f.id, ',', f.name, ',', f.containingClass, ',', f.visibility, ',', f.applicability, ',', f.type)

    def print_constructor(self, c):
        print("CONSTRUCTOR", c.id, ',', c.visibility)
        params = ''
        for p in c.paramaters:
            if(params == ''):
                params = p.id
            else:
                params += ', ' + p.id
        print("Constructor Paramaters:", params)
        self.print_var_table(self, c.variableTable)
        print("Constructor Body:")
        self.print_body(self, c.body)

    def print_method(self, m):
        print("METHOD", m.id, ',', m.name, ',', m.containingClass, ',', m.visibility)
        params = ''
        for p in m.paramaters:
            if(params == ''):
                params = p.id
            else:
                params += ', ' + p.id
        print("Method Paramaters:", params)
        self.print_var_table(self, m.variableTable)
        print("Method Body:")
        self.print_body(self, m.body)


    def print_var_table(self, vt):
        print("Variable Table:")
        base_types = ['int', 'float', 'boolean']
        # type needs to be represented as (int, float, boolean)
        # or user(name)
        for t in vt:
            ty = t.type
            if ty not in base_types:
                ty = 'user(' + t.type+ ')'
            print("VARIABLE", t.id, ',', t.name, ',', t.kind, ',', ty)

    def print_body(self, b):
        # TODO
        # print expression
        for i in b:
            if(type(i) == decaf_ast.Statement):
                if(i.kind == 'Block'):
                    print(self.print_block(self, i.attributes['stmnts']))
                else:
                    print(self.gen_print_stmnt(self, i))
            elif (type(i) == decaf_ast.Expression):
                print(i.kind, '(', ')')
    
    # returns the string of a block to be printed
    def print_block(self, stmnts):
        content = ''
        for stmnt in stmnts:
            if content == '':
                content = self.gen_print_stmnt(self, stmnt)
            elif stmnt.kind == 'Block':
                content += ', ' + self.print_block(self, stmnt.attributes['stmnts'])
            else:
                content += ', ' + self.gen_print_stmnt(self, stmnt)
        s = "Block ([" + content + "])"
        return s

    # returns the string of a statement to be printed
    def gen_print_stmnt(self, stmnt):
        content = ''
        for val in stmnt.attributes.values():
            if content == '':
                content = val
            else:
                content += val + ', '
        s = stmnt.kind +'(' + content + ')'
        return s


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
    print("YES")


if __name__ == "__main__":
    main()
