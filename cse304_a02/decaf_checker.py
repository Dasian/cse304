# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

# File containing the main python function to put together
# the lexer and parser, take the input from the Decaf
# program file, etc., and perform syntax checking
# Input: The name of the file containing the Decaf program
# Output: "Yes" if the Decaf program is syntactically correct or an error message describing the first
# error and where it occurred (line and column number)
# Usage: python3 decaf_checker.py [filename]

import sys
from os.path import exists
import ply.lex as lex
import ply.yacc as yacc


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
    parser = yacc.yacc(module=decaf_parser, debug=True)

    file = open(filename, 'r')
    file_string = file.read()
    file.close()

    parser.parse(file_string, lexer=lexer)
    print("YES")


if __name__ == "__main__":
    main()
