# Projet de compilation
# Moodle ensta compilation

# Presentation
The ESP-NOW compiler project aims to facilitate the development of wireless communication systems using Espressif's ESP-NOW protocol. ESP-NOW is a fast and efficient Wi-Fi communication protocol, ideal for IoT applications and sensor networks. This compiler generates C++ code for ESP-NOW-compatible microcontrollers, simplifying the development process for wireless communication applications.

## Objective
The main aim of the project is to provide an efficient development tool for engineers and developers working on projects involving communication via ESP-NOW. The compiler makes it quick and easy to generate the code needed to configure ESP-NOW devices, send and receive messages, and process exchanged data.

## Key features
- Structured Message Definition:** The compiler makes it easy to define structured messages with specific fields, simplifying the management of data exchanged between devices.
- Automatic generation of C++ code:** Based on message specifications, the compiler automatically generates the C++ code needed to configure ESP-NOW devices, send messages and process received data.
- Communication Optimization:** The generated code is optimized to ensure efficient and reliable communication between ESP-NOW devices.

# Usage
The ESP-NOW compiler is run from the command line. Here's how to run it:
1. Specifying the input file

The compiler requires an input file containing the specifications of the messages to be compiled. Make sure you have created such a file before running the compiler.

2. Run command

Use the following command to run the compiler:

````bash
python3 __main__.py [input file] -v
````

Replace [input file] with the path to the file containing the message specifications.
The -v option is optional and enables verbose mode, which displays additional information during the compilation process.

Example:

````bash
python3 __main__.py examples/messages.txt -v
````
3. Compilation results

Once compilation is complete, the compiler will automatically generate the C++ code corresponding to the message specifications. The generated files will be available in the Output directory.

# Syntax
The code is structured in several parts:
1. Definition of Units
The first part defines the different microcontrollers that will communicate, referred to as units. Each unit is declared with its own name.

Exemple :
```
unit ESP1
unit ESP2 

```
2. Message definition
The second part of the code defines the messages to be generated. Each message begins with the keyword message and is made up of three main parts.

Example message:
```
message : 	
	ESP1 = broadcast
	ESP2 = listener
	Name = Discover
	Variable : char[16] ESP_name
	Comment = Nom de l'ESP

```
# Details of Message Parts

| Parties                   | Fonction                                                                                        |
|---------------------------|-------------------------------------------------------------------------------------------------|
| **unit declarations** | Each unit is declared with its name and can have one of three values: broadcast, sender or listener. |
| Message name            | The message name is mandatory and must be free of spaces, accents or special characters.                                                              |
| Message variable       | Variables are defined in the last part of the message.  


### Unit declaration
Units participating in the message are declared in the first part of the message. These units can adopt one of the following three roles:

| broadcast | The unit sends the message to all other units capable of receiving the message. |
| sender    | The unit sends the message exclusively to units designated as **listener**.     |
| listener  | The unit receives the message, whether broadcast or sent by a sender.           |
In each message, there can only be one **sender** or **broadcast**.

### Message name
The message must have a name. The name cannot contain spaces, accents or special characters.

### Variables 

Message variables are defined with the Variable keyword: followed by the variable type, which can be one of the following: int, char, char[], int8_t, uint8_t, int32_t, uint32_t, bool, float, double. After the type declarator, the variables must be given a name.
Example:
```
Variable : int a 
Variable : char[16] nom
Variable : double decimal
```

### Comment 
Comments can be added after a variable. These comments will be added in the C code. They must be a single line long.
```
Variable : int a 
Comment = is a variable a
```


## Example code

```
unit ESP1
unit ESP2 

message : 	
	ESP1 = broadcast
	ESP2 = listener
	Name = Discover
	Variable : char[16] ESP_name

message : 
	ESP1 = listener
	ESP2 = sender
	Name = Offer
	Variable : int ESP_ID_RES

message : 
	ESP1 = sender
	ESP2 = listener
	Name = Request
	Variable : bool valid_new_ID

message : 
	ESP1 = listener
	ESP2 = sender
	Name = ACK
	Variable : bool valid_comm
```
# Main files
1. __main__.py
This file is the application's entry point. It initializes the compilation process and manages command-line arguments.
2. astnode.py
This file contains the node definitions of the abstract syntax tree (AST). Each node represents a program structure in the source language.
3. lexer.py
The lexer parses the source code into sequences of tokens. Each token represents a syntactic unit (such as a keyword, identifier, operator, etc.).
4. parser.py
The parser analyzes the sequence of tokens produced by the lexer and builds the abstract syntax tree (AST) corresponding to the source program.
5. scope.py
This file contains the logic for managing variable and symbol scopes in the program. It provides name resolution and scope context management.
6. visitor.py
This visitor traverses the abstract syntax tree (AST) and produces a text representation of the source code, preserving its structure and formatting.
7. structuregenerator.py
This visitor parses the AST and generates an intermediate data structure used to generate header files (.h).
8. code_generator.py
This visitor parses the AST and generates C++ code from the intermediate data structure produced by structure_generator.py.

# Limitation 
The compiler only supports 256 different messages due to its implementation in binary frames.
The compiler only provides functions for interacting with a microcontroller.
