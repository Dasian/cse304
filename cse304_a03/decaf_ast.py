# David Espiritu despiritu 112264228
# Sean Yang sjyang 110766661

# table and class definitions for Decaf's AST

# Driver to initialize tables and print contents 
# in decaf_checker
from asyncio.windows_events import NULL
from pdb import line_prefix
from statistics import linear_regression


class ASTDriver:
    def __init__(self):
        # something
        print("INIT")

    # prints the contents of the AST
    def print_table(self):
        print("table lmao get it?")

# All other class definitions after this point are nodes for the table
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

    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability=""):
        self.name = name
        self.id = id
        self.containingClass = containingClass
        self.visibility = visibility
        self.applicability = applicability

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

class Record:
    def __init__(self, lineRange=[]):
        self.lineRange = lineRange

# All Statements in this block
class IfStatement(Record):
    def __init__(self, condition=None, then=None, elseStatement=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.condition = condition
        self.then = then
        self.elseStatement = elseStatement

class WhileStatement(Record):
    def __init__(self, condition=None, body=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.condition = condition
        self.body = body

class ForStatement(Record):
    def __init__(self, init=None, condition=None, body=None, update=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.condition = condition
        self.init = init
        self.body = body
        self.update = update

class ReturnStatement(Record):
    def __init__(self, value=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.value = value

class ExprStatement(Record):
    def __init__(self, expr=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.expr = expr

class BlockStatement(Record):
    def __init__(self, stmnts=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.stmnts = stmnts

class BreakStatement(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class ContinueStatement(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class SkipStatement(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

# All Expressions in this block
class ConstExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class VarExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class UnaryExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class BinaryExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class AssignExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class AutoExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class FieldAccessExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class MethodCallExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class NewObjectExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class ThisExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class SuperExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class ClassReferenceExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)