# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

# table and class definitions for Decaf's AST
# Each class represents some sort of node in the table/tree

# All classes in this block are records
class ClassRecord:
    def __init__(self, name="", superName="", constructors=[], methods=[], fields=[]):
        self.name = name
        self.superName = superName
        self.methods = methods
        self.constructors = constructors
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
        self.name = name
        self.id = id
        self.containingClass = containingClass
        self.visibility = visibility
        self.applicability = applicability
        self.type = type

class VariableRecord:

    def __init__(self, name="", id=-1, kind="", type=None):
        self.name = name
        self.id = id
        self.kind = kind
        self.type = type

class TypeRecord:
    def __init__(self, name=""):
        self.name = name

# inherited classes (each represent one type of record)
# TODO: figure out better scheme for Statements and Expressions
class Statement:
    # kinds: If, While, For, Return, Expr, Block, Break, Continue, Skip
    # attributes: key is the attribute name and the value is mapped
    # @Sean for Block statements have the key in attributes named 'stmnts'
    def __init__(self, lineRange=[], kind='', attributes={}):
        self.lineRange = lineRange
        self.kind = kind
        self.attributes = attributes

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
