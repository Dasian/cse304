# David Espiritu 112264228
# A script to implement an ssm interpreter
# take as input the filename
# outputs the result of execution
# usage: python3 ssm_scanner.py [filename]

import sys
from os.path import exists

# Global vars
# the stack to be used, just use the built in pop function
stack = []
# Key is the address, value is value
store = {} 
# list of instructions
# every element is a tuple that contains the instruction and argument
instructions = []
# map labels to the index where instructions should be executed
# ex: 'here': 2; execute the instruction starting at index 2
labels = {}
valid_instructions = ['ildc', 'iadd', 'isub', 'imul', 'idiv', 'imod', 'pop', 'dup', 'swap', 'jmp', 'jz', 'jnz', 'load', 'store']
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
# imod - find the remainer of 2 elements
# pop
# dup - duplicate top most entry
# swap - swap the top 2 elements
# jmp label - jump to label
# jz label - pop stack, if 0 jmp to label
# jnz label- pop stack, jmp if not 0
# load - pop stack, push value at that address in the store
# store - top element is integer i and second from top is address
#  Put integer i at the adress index in the store
def ssm_execute():
	for i in range(0, len(instructions)):
		inst = instructions[i][0]
		arg = instructions[i][1]
	# TODO

# Takes as input a filename and parses the file
# Assumes that filename checks have already been done
# Instructions are placed into the ordered instruction list
# The indices refer to the instruction order and each index contains a tuple
# The tuples contain the instruction and possible args, None if there are None
# Labels are placed into the labels dictionary
# the keys are the names and the values are a range of line numbers to execute (indices in the instructions list)
# only the first index is placed for the labels 

# deal with label as the last statement. What is mapped to in the labels dictionary?
# can labels be the last statement, can a label declaration be the only statement, case of empty file?
def ssm_scan(filename):
	# open 
	global f
	f = open(filename)

	# remove comments and make the file one continuous string
	file_string = ''
	for l in f.readlines():
		# removing comments
		if '#' in l:
			l = l.replace(l[l.find('#'):l.find('\n')], '')
		file_string += l

	# create a list of consecutive characters (words) separated by 1+ whitespace
	file_string = file_string.replace('\n', ' ')
	file_string = file_string.replace('\t', ' ')
	words = file_string.split(' ')
	while '' in words:
		words.remove('')

	# deal with empty files
	if len(words) == 0:
		scan_error("Empty File")

	print(words)

	# verify words (instructions, labels, integers, or label:instruction)
	# prevents sequential label declarations
	i = 0
	isPrevLabel = False # is the previous word a label?
	for word in words:
		print(word)
		# verify instructions and integers
		if word in valid_instructions or isInt(word):
			isPrevLabel = False
		# verify label definition
		elif isValidLabel(word) and not isPrevLabel:
			isPrevLabel = True
		# split label:instruction words
		elif word.find(':') != len(words[i]) - 1 and not isPrevLabel:
			split = word.split(':')
			split[0] = split[0] + ':'
			# verify label followed by instruction (no whitespace)
			if len(split) == 2 and isValidLabel(split[0]) and split[1] in valid_instructions:
				words.pop(i)
				words.insert(i, split[0])
				words.insert(i+1, split[1])
				isPrevLabel = False
				i += 1 # verified two words so counter must be updated
			# verify label arguments
			elif not isValidLabel(word + ':'):
				scan_error("invalid word (split label)", [word, split, words])
		else:
			scan_error("invalid word (verify words)", [word])
		i += 1

	# all words at this point should be valid
	# argument checks and data structure insertion
	isCurrArg = False # does the current word need to be an argument?
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
				scan_error("invalid argument", [word])
			isCurrArg = False
		# inserting labels
		elif isValidLabel(word):
			word = word[0:-1] # remove colon
			curr_index = len(instructions)
			labels.update({word:curr_index})
			isCurrArg = False
		# inserting instructions
		elif word in no_arg_instructions:
			instructions.append((word, None))
			isCurrArg = False
		elif word in arg_instructions or word in jmp_instructions:
			isCurrArg = True
		else:
			scan_error("invalid word (verify order)", [word])
		prev_word = word

	# determines if label args point to established labels 
	verify_label_args()
	f.close()
	return

# determines if a string literal i is an integer
# An integer can be any number with an optional - in the first position
def isInt(i):
	if i.find('-') == 0 and i[1:len(i)].isdigit():
		return True
	else:
		return i.isdigit()

# Determines if str s is a valid label (end colon not removed)
# Valid labels must start with an alphabetic character
# followed by a sequence of alphabetic or numerica or underscore chars
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
			scan_error("invalid label", [s])
	return True

# Determines if all label arguments point to established labels
def verify_label_args():
	keys = labels.keys()
	for arg in label_args:
		if arg not in keys:
			scan_error("invalid label", [arg])

# prints an scan_error message and optional list of arguments
def scan_error(s, args = []):
	print(s)
	for a in args:
		print(a)
	f.close()
	exit()

def main():
	# take input from cmdline
	# possibly could also mean using input() but idk
	if len(sys.argv) != 2:
		print("Usage:",sys.argv[0], "[filename]")
		exit()
	filename = sys.argv[1]
	if not exists(filename):
		scan_error("File not found")

	# scan the file and place instructions into datastructures used for execution
	# handles compile time scan_errors	
	ssm_scan(filename)

	# debug
	scan_error("Instructions and Labels", [instructions, labels])

	# Execute the instructions
	ssm_execute()

	# Print result (topmost stack element) and exit
	if len(stack) == 0:
		print('empty stack')
		exit()
	print(stack[-1])
	exit()

if __name__ == "__main__":
	main()
