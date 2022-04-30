# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

# table and class definitions for Decaf's AST
# Each class represents some sort of node in the table/tree

# All classes in this block are records
# Part of Class Table
class ClassRecord:
    def __init__(self, name="", superName="", constructors=None, methods=None, fields=None):
        self.name = name # string
        self.superName = superName # string
        # list of MethodRecord objects
        if methods is None:
            self.methods = []
        else:
            self.methods = methods 
        # list of ConstructorRecord objects
        if constructors is None:
            self.constructors = []
        else:
            self.constructors = constructors 
        # list of FieldRecord objects
        if fields is None:
            self.fields = []
        else:
            self.fields = fields 

class ConstructorRecord:
    def __init__(self, id=-1, visibility="", parameters=None, variableTable=None, body=None):
        self.id = id # unique id
        self.visibility = visibility # string; public/private
        self.body = body # a single Statement object
        # list of VariableRecord objects passed to the constructor
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters
        # list of all VariableRecord objects (local vars + params)
        if variableTable is None:
            self.variableTable = []
        else:
            self.variableTable = variableTable

class MethodRecord:
    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability="", body=None, variableTable=None, returnType=None, parameters=None):
        self.name = name # string
        self.id = id # unique int
        self.containingClass = containingClass # string
        self.visibility = visibility # string; public/private
        self.applicability = applicability # string; static/non-static
        self.body = body # a single Statement object
        self.returnType = returnType # a single TypeRecord object
        # list of VariableRecord objects
        if variableTable is None:
            self.variableTable = []
        else:
            self.variableTable = variableTable
        # list of VariableRecord objects passed to the constructor
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters

class FieldRecord:
    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability="", type=None):
        self.name = name # string
        self.id = id # unique int
        self.containingClass = containingClass # string
        self.visibility = visibility # string; public/private
        self.applicability = applicability # string; static/non-static
        self.type = type # a single TypeRecord object

class VariableRecord:
    # Part of Variable Table
    def __init__(self, name="", id=-1, kind="", type=None):
        self.name = name # string
        self.id = id # unique int
        self.kind = kind # string; formal/local
        self.type = type # a single TypeRecord object

class TypeRecord:
    def __init__(self, name=""):
        self.name = name # string; int, float, boolean, or custom user defined type
        # added for hw4: void, error, null, class-literal

class Statement:
    # kinds: If, While, For, Return, Expr, Block, Break, Continue, Skip
    # attributes: key is the attribute name and the value is mapped
    # @Sean for Block statements have the key in attributes named 'stmnts'
    def __init__(self, lineRange=None, kind='', attributes=None):
        self.kind = kind # string; see above for valid kinds
        # dict; key is attribute, value is mapped
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
        # 2 int list; [startLine, endLine]
        if lineRange is None:
            self.lineRange = []
        else:
            self.lineRange = lineRange

# If you want to nest expressions have a key that is 'Expression'
#   that maps to a *list* of Expression object
# Have 'Constant' kinds with an 'Expression' attribute that maps to
#   another expression with the kind set to the proper form
#   ex: Integer-constant, Float-Constant, String-constant, True, etc.
# This, Super, and Class-reference(maybe?) as well as Null, True, and False
#   just need to have the kind set and no other attributes
# You can change this design if you want, this is just how I have it currently
#   implemented for printing; just change the prints or lmk
class Expression:
    # kinds: Constant, Variable, Unary, Binary, Assign, Auto, Field-access, 
    #   Method-call, New-object, This, Super, Class-reference
    def __init__(self, lineRange=None, kind='', attributes=None):
        self.kind = kind # string; see above
        # dict; key is attribute, value is mapped
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
        # 2 int list; [startLine, endLine]
        if lineRange is None:
            self.lineRange = []
        else:
            self.lineRange = lineRange

# Abstract Syntax Tree Table
"""
    TODO
    Error Checking Section
"""
class AST:

    # Initialize In and Out class
    def __init__(self):
        # list of ClassRecord objects, each of these are the root
        # this is essentially the class table
        self.classes = []

        # In class
        scanInt = MethodRecord(name="scan_int", id=1, containingClass="In", visibility="public", applicability="static", returnType=TypeRecord(name="int"))
        scanFloat = MethodRecord(name="scan_float", id=2, containingClass="In", visibility="public", applicability="static", returnType=TypeRecord(name="float"))
        inMethods = [scanInt, scanFloat]
        inClass = ClassRecord(name="In", methods=inMethods)

        # Out class
        i = VariableRecord(name="i", id=1, kind="formal", type=TypeRecord(name="int"))
        f = VariableRecord(name="f", id=2, kind="formal", type=TypeRecord(name="float"))
        b = VariableRecord(name="b", id=3, kind="formal", type=TypeRecord(name="boolean"))
        s = VariableRecord(name="s", id=4, kind="formal", type=TypeRecord(name="string"))
        print1 = MethodRecord(name="print", id=1, containingClass="Out", visibility="public", applicability="static", parameters=[i], variableTable=[i], returnType = TypeRecord('void'))
        print2 = MethodRecord(name="print", id=2, containingClass="Out", visibility="public", applicability="static", parameters=[f], variableTable=[f], returnType = TypeRecord('void'))
        print3 = MethodRecord(name="print", id=3, containingClass="Out", visibility="public", applicability="static", parameters=[b], variableTable=[b], returnType = TypeRecord('void'))
        print4 = MethodRecord(name="print", id=4, containingClass="Out", visibility="public", applicability="static", parameters=[s], variableTable=[s], returnType = TypeRecord('void'))
        outMethods = [print1, print2, print3, print4]
        outClass = ClassRecord(name="Out", methods=outMethods)

        # adding classes
        self.classes.append(inClass)
        self.classes.append(outClass)

    # returns a list of class names in the tree (str)
    def get_classes(self):
        cnames = []
        for c in self.classes:
            cnames.append(c.name)
        return cnames

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
                params = str(p.id)
            else:
                params += ', ' + str(p.id)
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
        if stmnt is None or stmnt is list:
            return
        content = ''
        if stmnt.kind == 'Block':
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
            if type(stmnt) is list:
                continue
            elif stmnt.kind == 'Block':
                content += self.block_str(stmnt.attributes['stmnts']) + ', '
            else:
                tmp = self.stmnt_str(stmnt)
                if tmp != '':
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
        if stmnt.kind == 'Skip':
            return content
        for val in stmnt.attributes.values():
            if type(val) is Statement:
                if val.kind == 'Block':
                    content += self.block_str(val.attributes['stmnts'])
                elif val.kind == 'Skip':
                    continue
                else:
                    content += self.stmnt_str(val)
            elif type(val) is Expression:
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

        # prevent printing out variable name (vname)
        if 'vname' in expr.attributes.keys():
            del expr.attributes['vname']

        for val in expr.attributes.values():
            if type(val) is Expression:
                content += self.expr_str(val)
            elif type(val) is list and len(val) > 0 and type(val[0]) is Expression:
                content += self.expr_list_str(val)
            else:
                content += str(val)
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
            content += self.expr_str(expr) + ', '
        return '[' + content[0:-2] + ']'