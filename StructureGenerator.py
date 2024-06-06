from astnode import *

class StructureGenerator:
    def __init__(self):
        self.output = ""
        self.units = set()  # Utiliser un ensemble pour éviter les doublons
        self.functions = {}  # Dictionnaire pour stocker les fonctions par unité

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_ProgramNode(self, node):
        for child in node.children:
            self.visit(child)
        self.generate_structures_and_addresses()
        #self.generate_function_prototypes()

    def visit_UnitNode(self, node):
        self.units.add(node.value)
        if node.value not in self.functions:
            self.functions[node.value] = {"set_address": True, "send_functions": []}

    def visit_MessageNode(self, node):
        message_id = node.value
        name = None
        variables = []
        for child in node.children:
            if isinstance(child, NameNode):
                name = child.value
            elif isinstance(child, AssignmentNode):
                unit = child.children[0].value
                role = child.children[1].value
                if role in ['broadcast', 'sender']:
                    if unit in self.functions:
                        self.functions[unit]["send_functions"].append(f"send_{name}_{unit}")
            elif isinstance(child, VariableNode):
                var_type, var_name = child.value.split()
                variables.append(f"{var_type} {var_name};")

        if name:
            self.output += f"typedef struct {name} {{\n"
            self.output += f"  char message_id = {message_id};\n"
            for var in variables:
                self.output += f"  {var}\n"
            self.output += f"}} {name};\n\n"
            self.output += f"{name} data_{name};\n\n"

    def generate_structures_and_addresses(self):
        for unit in self.units:
            self.output += f"uint8_t {unit}_address[] = {{0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}};\n"
        self.output += "uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};\n"

    def generate_function_prototypes(self):
        # Générer des fonctions set_address
        for unit in self.units:
            self.output += f"void set_{unit}_address(uint8_t *address);\n"
        # Générer des fonctions d'envoi pour chaque unité sur la base des rôles définis dans les messages
        for unit, details in self.functions.items():
            for func in details["send_functions"]:
                self.output += f"void {func}();\n"
        # Générer le prototype de la fonction OnDataRecv
        self.output += "void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len);\n"

    def generate_code(self, ast):
        self.visit(ast)
        return self.output
