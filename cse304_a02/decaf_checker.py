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
import decaf_lexer
import ply.yacc as yacc
import decaf_parser


def decaf_scan(filename):
    return 0


# Compute column
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def main():
    if len(sys.argv) != 2:  # Takes input from cmdline
        print("python3 decaf_checker.py [filename]")
        exit()
    filename = sys.argv[1]
    if not exists(filename):
        print("File not found")
        exit()

    lexer = lex.lex(module=decaf_lexer)
    global file
    file = open(filename)

    # make the file one continuous string
    file_string = ''
    multi_line_comment = False
    for line in file.readlines():
        file_string += line

    lexer.input(file_string)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

    """parser = yacc.yacc(tabmodule=decaf_parser)
    while True:
        s = '3+2'
        result = parser.parse(s)
        print(result)"""

    print("Yes")


if __name__ == "__main__":
    main()
