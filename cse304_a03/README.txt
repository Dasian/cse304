# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

This file documents the contents of the other files.

decaf_lexer.py (Lexer): This file contains various tokens with functions and regular expressions.

decaf_parser.py (Parser): This file contains various grammar rules for the parsing.

decaf_checker.py (Main): This file reads an inputted decaf file name, tokenizes the code using decaf_lexer.py,
and parses it with decaf_parser.py in order to verify proper Decaf syntax. The main method will output either "YES"
or the location of the first syntactical error.

decaf_ast.py (AST): This file contains the organizational code for
storing and constructing an AST of a file