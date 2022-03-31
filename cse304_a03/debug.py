# A list of methods for debugging

# a debug function for print p in decaf_parser
# takes p as first input
# optional debug message as second input
def print_p(p, msg="Printing p"):
    print(msg)
    for i in range(len(p)):
        print("Index:",i,"Value:",p[i],"Type:",type(p[i]))