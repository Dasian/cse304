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

    def __init__(self, id=-1, visibility="", parameters=[], variableTable=[], body=None):
        self.id = id
        self.visibility = visibility
        self.parameters = parameters
        self.variableTable = variableTable
        self.body = body

class MethodRecord:

    def __init__(self, name="", id=-1, containingClass="", visibility="", applicability="", body=None, variableTable=[]):
        self.name = name
        self.id = id
        self.containingClass = containingClass
        self.visibility = visibility
        self.applicability = applicability
        self.body = body
        self.variableTable = variableTable

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
    def __init__(self, lineRange=[]):
        self.lineRange = lineRange

"""
# All classes in this block statement (deprecated)
class IfStatement(Statement):
    def __init__(self, condition=None, then=None, elseStatement=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.condition = condition
        self.then = then
        self.elseStatement = elseStatement

class WhileStatement(Statement):
    def __init__(self, condition=None, body=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.condition = condition
        self.body = body

class ForStatement(Statement):
    def __init__(self, init=None, condition=None, body=None, update=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.condition = condition
        self.init = init
        self.body = body
        self.update = update

class ReturnStatement(Statement):
    def __init__(self, value=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.value = value

class ExprStatement(Statement):
    def __init__(self, expr=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.expr = expr

class BlockStatement(Statement):
    def __init__(self, stmnts=None, lineRange=[]):
        super().__init__(lineRange=lineRange)
        self.stmnts = stmnts

class BreakStatement(Statement):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class ContinueStatement(Statement):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class SkipStatement(Statement):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)
"""

# All classes in this block are expressions
class ConstExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class VarExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class UnaryExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class BinaryExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class AssignExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class AutoExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class FieldAccessExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class MethodCallExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class NewObjectExpression(Record):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class ThisExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class SuperExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)

class ClassReferenceExpression(Expression):
    def __init__(self, lineRange=[]):
        super().__init__(lineRange)