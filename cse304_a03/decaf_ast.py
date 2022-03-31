# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

# table and class definitions for Decaf's AST
# Each class represents some sort of node in the table/tree

# All classes in this block are records
# Part of Class Table
class ClassRecord:
    def __init__(self, name="", superName="", constructors=[], methods=[], fields=[]):
        self.name = name # string
        self.superName = superName # string
        self.methods = methods # list of MethodRecord objects
        self.constructors = constructors # list of ConstructorRecord objects
        self.fields = fields # list of FieldRecord objects

class ConstructorRecord:
    def __init__(self, id=-1, visibility="", parameters=[], variableTable=[], body=None):
        self.id = id # unique int
        self.visibility = visibility # string; public/private
        self.parameters = parameters # list of VariableRecord objects passed to the constructor
        self.variableTable = variableTable # list of all VariableRecord objects (local vars + params)
        self.body = body # a single Statement object

class MethodRecord:
    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability="", body=None, variableTable=[], returnType=None, paramaters=[]):
        self.name = name # string
        self.id = id # unique int
        self.containingClass = containingClass # string
        self.visibility = visibility # string; public/private
        self.applicability = applicability # string; static/non-static
        self.body = body # a single Statement object
        self.variableTable = variableTable # list of VariableRecord objects
        self.returnType = returnType # a single TypeRecord object
        self.paramaters = paramaters # list of VariableRecord objects passed to the method

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
        self.kind = kind # ??
        self.type = type # a single TypeRecord object

class TypeRecord:
    def __init__(self, name=""):
        self.name = name # string; int, float, boolean, or custom user defined type

class Statement:
    # kinds: If, While, For, Return, Expr, Block, Break, Continue, Skip
    # attributes: key is the attribute name and the value is mapped
    # @Sean for Block statements have the key in attributes named 'stmnts'
    def __init__(self, lineRange=[], kind='', attributes={}):
        self.lineRange = lineRange # 2 int list; [startLine, endLine]
        self.kind = kind # string; see above for valid kinds
        self.attributes = attributes # dict; key is attribute, value is mapped

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
    def __init__(self, lineRange=[], kind='', attributes={}):
        self.lineRange = lineRange # 2 int list; [startLine, endLIne]
        self.kind = kind # string; see above
        self.attributes = attributes # dict; key is attribute, value is mapped