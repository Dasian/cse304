# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661
# A script to implement an SSM interpreter
# Input: The name of the file containing the SSM instructions
# Output: The result of the execution of the SSM instructions in the input file
# Usage: python3 ssm_scanner.py [filename]

import sys
from os.path import exists

# Global vars
stack = []  # The stack that holds operands for operations
store = {}  # The store that is directly addressed
# List of instructions from input file
# Every element is a tuple that contains the instruction and argument
instructions = []
# Map labels to the index where instructions should be executed
# ex: 'here': 2; execute the instruction starting at index 2
labels = {}
valid_instructions = ['ildc', 'iadd', 'isub', 'imul', 'idiv', 'imod', 'pop', 'dup', 'swap', 'jmp', 'jz', 'jnz', 'load',
                      'store']
no_arg_instructions = ['iadd', 'isub', 'imul', 'idiv', 'imod', 'pop', 'dup', 'swap', 'load', 'store']
arg_instructions = ['ildc']
jmp_instructions = ['jmp', 'jz', 'jnz']
label_args = []


# Instructions
# ildc num - pushes num on the stack
# iadd - pop 2 elements from stack and push the sum
# isub - pop 2 elements, subtract, push difference
# imul - pop 2 elements, multiply, push product
# idiv - pop 2 elements, divide, push quotient
# imod - find the remainder of 2 elements
# pop - pop top most entry
# dup - duplicate top most entry
# swap - swap the top 2 elements
# jmp label - jump to label
# jz label - pop stack, if 0 jmp to label
# jnz label- pop stack, jmp if not 0
# load - pop stack as address, push value at that address in the store
# store - top element is integer i and second from top is address
# Put integer i at the address index in the store
def ssm_execute():
    index = 0
    while index < len(instructions):
        inst = instructions[index][0]
        arg = instructions[index][1]
        if inst == "ildc":
            stack.append(arg)
        elif inst == "iadd":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            first_operand = stack.pop()
            second_operand = stack.pop()
            stack.append(second_operand + first_operand)
        elif inst == "isub":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            first_operand = stack.pop()
            second_operand = stack.pop()
            stack.append(second_operand - first_operand)
        elif inst == "imul":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            first_operand = stack.pop()
            second_operand = stack.pop()
            stack.append(second_operand * first_operand)
        elif inst == "idiv":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            first_operand = stack.pop()
            if first_operand == 0:
                exe_error("Cannot divide a value by 0")
            second_operand = stack.pop()
            stack.append(second_operand // first_operand)
        elif inst == "imod":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            first_operand = stack.pop()
            if first_operand == 0:
                exe_error("Cannot divide a value by 0")
            second_operand = stack.pop()
            stack.append(second_operand % first_operand)
        elif inst == "pop":
            if len(stack) < 1:
                exe_error("Cannot access requested value(s) from stack")
            stack.pop()
        elif inst == "dup":
            if len(stack) < 1:
                exe_error("Cannot access requested value(s) from stack")
            stack.append(stack[-1])
        elif inst == "swap":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            top = stack.pop()
            bottom = stack.pop()
            stack.append(top)
            stack.append(bottom)
        elif inst == "jz":
            if len(stack) < 1:
                exe_error("Cannot access requested value(s) from stack")
            jump_value = stack.pop()
            if jump_value == 0:
                index = labels.get(arg) - 1
        elif inst == "jnz":
            if len(stack) < 1:
                exe_error("Cannot access requested value(s) from stack")
            jump_value = stack.pop()
            if jump_value != 0:
                index = labels.get(arg) - 1
        elif inst == "jmp":
            index = labels.get(arg) - 1
        elif inst == "load":
            if len(stack) < 1:
                exe_error("Cannot access requested value(s) from stack")
            address = stack.pop()
            if store.get(address) is None:
                exe_error("Cannot access requested value from store")
            stack.append(store.get(address))
        elif inst == "store":
            if len(stack) < 2:
                exe_error("Cannot access requested value(s) from stack")
            element = stack.pop()
            address = stack.pop()
            store.update({address: element})
        index = index + 1


# Takes as input a filename and parses the file
# Assumes that filename checks have already been done
# Instructions are placed into the ordered instruction list
# The indices refer to the instruction order and each index contains a tuple
# The tuples contain the instruction and possible args, None if there are None
# Labels are placed into the labels dictionary
# the keys are the names and the values are a range of line numbers to execute (indices in the instructions list)
# only the first index is placed for the labels 
def ssm_scan(filename):
    # open file
    global file
    file = open(filename)

    # remove comments and make the file one continuous string
    file_string = ''
    for line in file.readlines():
        # removing comments
        if '#' in line:
            line = line.replace(line[line.find('#'):line.find('\n')], '')
        file_string += line

    # create a list of consecutive characters (words) separated by 1+ whitespace
    file_string = file_string.replace('\n', ' ')
    file_string = file_string.replace('\t', ' ')
    words = file_string.split(' ')
    while '' in words:
        words.remove('')

    # deal with empty files
    if len(words) == 0:
        scan_error("Empty file")

    # verify words (instructions, labels, integers, or label:instruction)
    # prevents sequential label declarations
    i = 0
    isPrevLabel = False  # is the previous word a label?
    isPrevJmp = False  # is the previous instruction a jmp instruction?
    for word in words:
        # verify instructions and integers
        if word in valid_instructions or isInt(word):
            isPrevLabel = False
            if word in jmp_instructions:
                isPrevJmp = True
            else:
                isPrevJmp = False
        # verify label definition
        elif isValidLabel(word) and not isPrevLabel:
            isPrevLabel = True
            isPrevJmp = False
        # split label:instruction words
        elif word.find(':') != len(words[i]) - 1 and not isPrevLabel:
            if word.find(':') == -1 and not isPrevJmp:
                scan_error("Invalid Word")
            split = word.split(':')
            split[0] = split[0] + ':'
            # verify label followed by instruction (no whitespace)
            if len(split) == 2 and isValidLabel(split[0]) and split[1] in valid_instructions:
                words.pop(i)
                words.insert(i, split[0])
                words.insert(i + 1, split[1])
                isPrevLabel = False
                if split[1] in jmp_instructions:
                    isPrevJmp = True
                else:
                    isPrevJmp = False
                i += 1  # verified two words so counter must be updated
            # verify label arguments (argument to a jmp command)
            elif not isValidLabel(word + ':'):
                scan_error("Invalid word (split label)", [word, split, words])
        else:
            scan_error("Invalid word (verify words)", [word])
        i += 1
    # all words at this point should be valid
    # argument checks and data structure insertion
    isCurrArg = False  # does the current word need to be an argument?
    prev_word = ''
    for word in words:
        # inserting arguments
        if isCurrArg:
            if prev_word in arg_instructions and isInt(word):
                instructions.append((prev_word, int(word)))
            elif prev_word in jmp_instructions and isValidLabel(word + ':'):
                instructions.append((prev_word, word))
                label_args.append(word)
            else:
                scan_error("Invalid argument", [word])
            isCurrArg = False
        # inserting labels
        elif isValidLabel(word):
            word = word[0:-1]  # remove colon
            curr_index = len(instructions)
            labels.update({word: curr_index})
            isCurrArg = False
        # inserting instructions
        elif word in no_arg_instructions:
            instructions.append((word, None))
            isCurrArg = False
        elif word in arg_instructions or word in jmp_instructions:
            isCurrArg = True
        else:
            scan_error("Invalid word (verify order)", [word])
        prev_word = word

    # determines if label args point to established labels
    verify_label_args()
    file.close()
    return


# Determines if a string literal i is an integer
# An integer can be any number with an optional - in the first position
def isInt(i):
    if i.find('-') == 0 and i[1:len(i)].isdigit():
        return True
    else:
        return i.isdigit()


# Determines if str s is a valid label (end colon not removed)
# Valid labels must start with an alphabetic character
# followed by a sequence of alphabetic, numeric, or underscore chars
def isValidLabel(s):
    # determines if : is at the end of the string
    if s.find(':') == len(s) - 1:
        s = s[0:-1]
    else:
        return False
    # first character must be alphabetic
    if not s[0].isalpha():
        return False
    for c in s:
        if not (c.isalpha() or c.isdigit() or c == '_'):
            scan_error("Invalid label", [s])
    return True


# Determines if all label arguments point to established labels
def verify_label_args():
    keys = labels.keys()
    for arg in label_args:
        if arg not in keys:
            scan_error("Invalid label", [arg])


# Prints an scan_error message and optional list of arguments
def scan_error(s, args=[]):
    print(s)
    for a in args:
        print(a)
    file.close()
    exit()


# Prints an execution error message and optional list of arguments
def exe_error(s, args=[]):
    print(s)
    for a in args:
        print(a)
    exit()


def main():
    # Takes input from cmdline
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "[filename]")
        exit()
    filename = sys.argv[1]
    if not exists(filename):
        scan_error("File not found")

    # Scans the file and place instructions into data structures used for execution
    # Handles compile-time input errors
    ssm_scan(filename)

    # Execute the instructions
    # Handles errors with executing instructions
    ssm_execute()

    # Prints result (topmost stack element) and exit
    if len(stack) == 0:
        print('Empty stack')
        exit()
    print(stack[-1])
    exit()


if __name__ == "__main__":
    main()
