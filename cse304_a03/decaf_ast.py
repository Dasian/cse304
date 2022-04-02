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
    def __init__(self, id='', visibility="", parameters=None, variableTable=None, body=None):
        self.id = id # name of the class
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
    # kinds: Constant, Var, Unary, Binary, Assign, Auto, Field-access, 
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