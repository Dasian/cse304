# A list of methods for debugging

# a debug function for print p in decaf_parser
# takes p as first input
# optional debug message as second input
import decaf_ast as ast
import decaf_lexer as lexer

def print_p(p, msg="Printing p"):
    print(msg)
    for i in range(len(p)):
        if type(p[i]) is ast.Statement:
            print(p.lexer.lineno,"Name:",p[i].kind,"Statement Line Range:", p[i].lineRange)
            for symbol in p[1:]:
                print(symbol)
        elif type(p[i]) is ast.Expression:
            print(p.lexer.lineno,"Name:",p[i].kind,"Expression Line Range:", p[i].lineRange)
            for symbol in p[1:]:
                print(symbol)