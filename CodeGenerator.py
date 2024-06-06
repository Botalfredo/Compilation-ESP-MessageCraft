from astnode import *

class CodeGenerator:
    def __init__(self):
        self.output = ""
        self.listeners = []  # Liste pour stocker les tuples (ID de message, nom du message, variables)

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
        self.generate_unified_recv_function()

    def visit_UnitNode(self, node):
        self.generate_address_function(node.value)  # Générer une fonction d'adresse pour chaque unité

    def visit_MessageNode(self, node):
        message_id = node.value
        name = None
        units = {}
        variables = []
        for child in node.children:
            if isinstance(child, NameNode):
                name = child.value
            elif isinstance(child, AssignmentNode):
                unit = child.children[0].value
                role = child.children[1].value
                units[unit] = role
            elif isinstance(child, VariableNode):
                variables.append((child.value.split()[1], child.value.split()[0]))  # Store as (name, type)
        if any(role == 'listener' for role in units.values()):
            self.listeners.append((message_id, name, variables))
        for unit, role in units.items():
            if role in ['broadcast', 'sender']:
                self.generate_send_function(name, unit, role)

    def generate_send_function(self, message_name, unit, role):
        address = 'broadcastAddress' if role == 'broadcast' else f'{unit}_address'
        self.output += f"void send_{message_name}_{unit}() {{\n"
        self.output += f"    esp_now_send({address}, (uint8_t *) &data_{message_name}, sizeof(data_{message_name}));\n"
        self.output += f"}}\n\n"

    def generate_address_function(self, unit):
        self.output += f"void set_{unit}_address(uint8_t *address) {{\n"
        self.output += f"    memcpy({unit}_address, address, sizeof({unit}_address));\n"
        self.output += f"}}\n\n"

    def generate_unified_recv_function(self):
        self.output += "void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {\n"
        self.output += "\tSerial.print(\"Bytes received: \");\n"
        self.output += "\tSerial.println(len);\n"
        first = True
        for message_id, message_name, variables in self.listeners:
            condition = "if" if first else "else if"
            self.output += f"\t{condition}(incomingData[0] == {message_id}){{\n"
            self.output += f"\t\tmemcpy(&data_{message_name}, incomingData + 1, sizeof(data_{message_name}));\n"
            for var_name, var_type in variables:
                self.output += f"\t\tSerial.println(data_{message_name}.{var_name});\n"
            self.output += "\t}\n"
            first = False
        self.output += "}\n\n"

    def generate_code(self, ast):
        self.visit(ast)
        return self.output
