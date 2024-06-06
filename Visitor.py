class Visitor:
    def __init__(self):
        self.indentation = 0  # Cela permet d'imprimer la structure de l'arbre

    def visit(self, node):
        """Generic visit method that calls the specific visit method for the type of node."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Fallback visit method if no specific visit method exists for a node."""
        print(f"{'  ' * self.indentation}{node.type}: {node.value}")
        self.indentation += 1
        for child in node.children:
            self.visit(child)
        self.indentation -= 1

    def visit_ProgramNode(self, node):
        print(f"{'  ' * self.indentation}Program:")
        self.indentation += 1
        for child in node.children:
            self.visit(child)
        self.indentation -= 1

    def visit_UnitNode(self, node):
        print(f"{'  ' * self.indentation}Unit: {node.value}")

    def visit_MessageNode(self, node):
        print(f"{'  ' * self.indentation}Message: {node.value}")
        self.indentation += 1
        for child in node.children:
            self.visit(child)
        self.indentation -= 1

    def visit_AssignmentNode(self, node):
        print(f"{'  ' * self.indentation}Assignment:")
        self.indentation += 1
        self.visit(node.children[0])
        print(f"{'  ' * self.indentation}equals")
        self.visit(node.children[1])
        self.indentation -= 1

    def visit_IdentifierNode(self, node):
        print(f"{'  ' * self.indentation}Identifier: {node.value}")

    def visit_RoleNode(self, node):
        print(f"{'  ' * self.indentation}Role: {node.value}")

    def visit_VariableNode(self, node):
        print(f"{'  ' * self.indentation}Variable: {node.value}")