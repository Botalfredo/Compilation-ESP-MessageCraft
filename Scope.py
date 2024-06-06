class Symbol:
    """ Représente un symbole dans la table des symboles avec un nom et un type. """
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.value = value

class SymbolTable:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_scope(self):
        new_scope = Scope(parent=self.current_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    def define_symbol(self, name, type, value=None):
        symbol = Symbol(name, type, value)
        self.current_scope.define(symbol)

    def lookup_symbol(self, name):
        return self.current_scope.lookup(name)

    def display_all_units(self):
        """ Afficher toutes les unités définies dans toutes les portées """
        def display_scope_units(scope):
            for symbol_name, symbol in scope.symbols.items():
                if symbol.type == 'Unit':
                    print(f"Unit '{symbol.name}' defined in scope")
            # Recursively display units from child scopes
            if scope.parent:
                display_scope_units(scope.parent)
        
        display_scope_units(self.current_scope)

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        scope = self
        while scope:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent
        return None

    def __repr__(self):
        return f"Scope(id={id(self)}, level={self.get_level()})"

    def get_level(self):
        level = 0
        scope = self
        while scope.parent:
            scope = scope.parent
            level += 1
        return level