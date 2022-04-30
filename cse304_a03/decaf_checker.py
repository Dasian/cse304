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
from decaf_parser import tree

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

    # hw3: printing the AST
    tree.print_table()


if __name__ == "__main__":
    main()
