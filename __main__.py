import os
import sys

from lexer import Lexer
from p4rser import Parser
from Visitor import Visitor
from StructureGenerator import StructureGenerator
from CodeGenerator import CodeGenerator

def main():
    # Vérification du nombre d'arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <nom_fichier> [-v]")
    else :
        file_path = sys.argv[1]

    # Récupération du nom du fichier
    #file_path = sys.argv[1]   
    #file_path = 'Exemple/exemple5.txt'

    # Vérification de l'option -v
    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "-v":
        verbose = True

    # Lecture du fichier sources
    with open(file_path, "r") as input_file:
            source_code = input_file.readlines()

    # Initialisation du Lexer
    lexer = Lexer()
    tokens = lexer.lex(source_code)

    # Si verbose affichage des tokens
    if verbose:
        print("Tokens:")
        for token in tokens:
            print(token)
        print("\n")
    
    # Initalisation du parser
    parser = Parser(tokens)
    ast = parser.parse()

    # Si verbose affichage de l'ast brut
    if verbose:
        print("\nAST:")
        print(ast)
        print("\n")

    # Initalisation du visiteur
    if verbose:
        visitor = Visitor()
        visitor.visit(ast)
        print("\n")

    # Initalisation du visiteur générant le fichier .h
    structureGenerator = StructureGenerator()
    generated_strucute = structureGenerator.generate_code(ast)
    
    # Sauvgarde dans le répertoire Output
    output_directory = 'Output'
    os.makedirs(output_directory, exist_ok=True)  # Création du répertoire si il n'esiste pas 
    file_path = os.path.join(output_directory, 'generated_structures.h')
    with open(file_path, 'w') as file:
        file.write(generated_strucute)
    # Affichage si verbose
    if verbose:
        print(generated_strucute)
        print(f"C code has been written to {file_path}")

    # Initalisation du visiteur code générateur pour la création du fichier .cpp
    codegenerator = CodeGenerator()
    generated_code = codegenerator.generate_code(ast)
    file_path = os.path.join(output_directory, 'generated_code.cpp')
    
    # Sauvgarde dans le répertoire Output
    with open(file_path, 'w') as file:
        file.write(generated_code)
    if verbose:
        print(generated_code)
        print(f"C code has been written to {file_path}")

    
if __name__ == "__main__":
    main()