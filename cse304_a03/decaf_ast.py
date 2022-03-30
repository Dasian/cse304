# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

# table and class definitions for Decaf's AST
# Each class represents some sort of node in the table/tree

# All classes in this block are records
# Part of Class Table
class ClassRecord:
    
    def __init__(self, name="", superName="", constructors=[], methods=[], fields=[]):
        self.name = name
        self.superName = superName
        self.methods = methods
        self.constructors = constructors
        self.fields = fields

class ConstructorRecord:

    def __init__(self, id=-1, visibility="", parameters=[], variableTable=[], body=None):
        self.id = id
        self.visibility = visibility
        self.parameters = parameters
        self.variableTable = variableTable
        self.body = body

class MethodRecord:

    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability="", body=None, variableTable=[], returnType="", paramaters=[]):
        self.name = name
        self.id = id
        self.containingClass = containingClass
        self.visibility = visibility
        self.applicability = applicability
        self.body = body
        self.variableTable = variableTable
        self.returnType = returnType
        self.paramaters = paramaters

class FieldRecord:

    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability="", type=None):
        self.name = name
        self.id = id
        self.containingClass = containingClass
        self.visibility = visibility
        self.applicability = applicability
        self.type = type

class VariableRecord:
    # Part of Variable Table
    def __init__(self, name="", id=-1, kind="", type=None):
        self.name = name
        self.id = id
        self.kind = kind
        self.type = type

class TypeRecord:
    def __init__(self, name=""):
        self.name = name

class Statement:
    # kinds: If, While, For, Return, Expr, Block, Break, Continue, Skip
    # attributes: key is the attribute name and the value is mapped
    # @Sean for Block statements have the key in attributes named 'stmnts'
    def __init__(self, lineRange=[], kind='', attributes={}):
        self.lineRange = lineRange
        self.kind = kind
        self.attributes = attributes

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
        self.lineRange = lineRange
        self.kind = kind
        self.attributes = attributes
