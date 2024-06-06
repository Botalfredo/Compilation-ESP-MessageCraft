from astnode import *
from Scope import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = None
        self.advance()
        self.symbol_table = SymbolTable()
        self.messageNuber = 0

    def advance(self):
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
            self.current_token_index += 1
        else:
            self.current_token = None

    def parse(self):
        return self.program()

    def program(self):
        program_node = ProgramNode()
        while self.current_token is not None:
            if self.current_token.type == 'UNIT':
                program_node.children.append(self.parse_unit())
            elif self.current_token.type == 'MESSAGE_START':
                program_node.children.append(self.parse_message())
            else:
                self.advance()
        #self.symbol_table.display_all_units()
        return program_node

    def parse_unit(self):
        unit_name = self.current_token.value.split()[1]
        self.advance()
        # Vérifier si l'unité est déjà définie dans le scope actuel ou un scope parent
        if self.symbol_table.lookup_symbol(unit_name):
            raise Exception(f"Unit '{unit_name}' is already defined.")
        # Définir la nouvelle unité dans la table des symboles
        self.symbol_table.define_symbol(unit_name, 'Unit')
        
        return UnitNode(unit_name)

    def parse_message(self):
        message_node = MessageNode(self.messageNuber)
        self.symbol_table.enter_scope()
        if self.messageNuber == 255:
            raise Exception(f"You have reached the maximum number of messages at {self.current_token.position}.")
        else:
            self.messageNuber += 1      
        self.advance()  # Skip 'message :'
        isVariablebeforComment = False
        while self.current_token and self.current_token.type != 'UNIT' and self.current_token.type != 'MESSAGE_START':
            # parseing des units
            if self.current_token.type == 'IDENTIFIER':
                if not self.symbol_table.lookup_symbol(self.current_token.value):
                    raise Exception(f"Unit '{self.current_token.value}' not defined at {self.current_token.position}. You must declare the unit at the top of the programme")
                
                identifier = IdentifierNode(self.current_token.value)
                self.advance()  # passe l'identifient
                if self.current_token.type == 'ASSIGN':
                    self.advance()  # Skip '='
                    if self.current_token.type in ['ROLE', 'IDENTIFIER']:
                        role_or_value_node = RoleNode(self.current_token.value) if self.current_token.type == 'ROLE' else IdentifierNode(self.current_token.value)
                        assignment = AssignmentNode(identifier, role_or_value_node)
                        message_node.children.append(assignment)
                        self.advance() 
            # prise en charge du mon des messages
            elif self.current_token.type == 'NAME':
                self.advance()
                if self.current_token.type == 'IDENTIFIER':
                    message_name = self.current_token.value
                    # Vérifier si l'unité est déjà définie dans le scope actuel ou un scope parent
                    if self.symbol_table.lookup_symbol(message_name):
                        raise Exception(f"Each message must have a different name '{message_name}' is already defined change the message name at {self.current_token.position}.")
                    # Définir la nouvelle unité dans la table des symboles
                    self.symbol_table.define_symbol(message_name, 'Message_name')

                    name_node = NameNode(message_name)
                    message_node.children.append(name_node)
            # Variable parsing
            elif self.current_token.type == 'VARIABLE':
                self.advance()  # Dépasser 'Variable :'
                if self.current_token.type == 'TYPE':
                    type_value = self.current_token.value
                    self.advance()  # Passer au jeton suivant, qui peut être une taille de tableau ou un nom de variable.
                    array_size = None
                    if self.current_token.type == 'ARRAY_SIZE':
                        array_size = self.current_token.value  # Saisir la taille du tableau
                        self.advance()  # Passer au nom de la variable
                        isVariablebeforComment = True
                    if self.current_token.type == 'IDENTIFIER':
                        variable_name = self.current_token.value
                        if array_size:
                            variable_name += array_size  # Ajouter la taille du tableau au type pour plus de clarté
                        variable_node = VariableNode(type_value, variable_name)
                        message_node.children.append(variable_node)
                        isVariablebeforComment = True
                        self.advance()  # Dépasser le nom de la variable
            # Comment parsing
            elif self.current_token.type == 'COMMENT':
                if isVariablebeforComment == False:
                    raise Exception(f"You need to define a variable before adding a comment at {self.current_token.position}.")
                comment_value = self.current_token.value.split('=', 1)[1].strip()  # Assuming 'Comment = Some comment text'
                comment_node = CommentNode(comment_value)
                message_node.children.append(comment_node)
                self.advance()  # Passer outre le commentaire
            else:
                self.advance()

        return message_node
