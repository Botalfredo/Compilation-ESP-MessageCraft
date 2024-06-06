class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value}, children={self.children})"

class ProgramNode(ASTNode):
    def __init__(self):
        super().__init__('Program')

class UnitNode(ASTNode):
    def __init__(self, name):
        super().__init__('Unit', value=name)

class MessageNode(ASTNode):
    def __init__(self, ID):
        super().__init__('Message', value=ID)

class NameNode(ASTNode):
    def __init__(self, name):
        super().__init__('Name', value=name)

class AssignmentNode(ASTNode):
    def __init__(self, left, right):
        super().__init__('Assignment', children=[left, right])

class IdentifierNode(ASTNode):
    def __init__(self, name):
        super().__init__('Identifier', value=name)

class RoleNode(ASTNode):
    def __init__(self, role):
        super().__init__('Role', value=role)

class VariableNode(ASTNode):
    def __init__(self, type, name):
        super().__init__('Variable', value=f"{type} {name}")

class CommentNode(ASTNode):
    def __init__(self, name):
        super().__init__('Comment', value=name)