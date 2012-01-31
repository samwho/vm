#!/usr/bin/env python
# version 1.1 adds instruction syntax checking

instruction = 0
operands = 1
badInstruction = -1
incorrectNumberofOperands = -2

def readAssemblyTable():
    table = []
    assemblyTableFile = open('src/assembly_table.txt', 'r')

    for line in assemblyTableFile:
        line = line.upper().split(' ')
        # line[1] is the number of operands allowed for a given instruction.
        # It will be read in as a string so we need to cast it to an int.
        line[1] = int(line[1])
        table.append(line)

    return table

def returnAssemblyTable():
    """This function abstracts the details of obtaining the assembly table
        and returns a list of instructions with their number of operands,
        with the index of the list being the opcode of the respective
        instruction"""
    return assemblyTable

def parseCodeFile(filename):
    """ This function parses a text file consisting of lines of
        assembly code and places them in a contiguous memory block"""
    code = []
    codeFile = open(filename, 'r')

    for line in codeFile: #parse through codefile line by line
        # Don't parse comment lines
        if line.startswith('//'):
            continue

        line = line.rstrip('\r\n') #strip trailing CR and LF
        line = line.upper() #convert all to caps for simplicity
        line = line.split(" ",1) #split keywords and parameters by leftmost space
        code.append(line)   #add list of keywords and parameters to memory array

    return code

def displayError(lineNumber, errorType, line = None):
    """This function displays an error occuring in the stated line number
       and prints details if it is a know error type"""

    print "Error on line", lineNumber

    if errorType == badInstruction:
        print "Bad Instruction"

    if errorType == incorrectNumberofOperands:
        print "Incorrect Number of Operands"

    if line != None:
        print "Offending line:", line

def assemble(code):
    """This function substituts opcodes for instruction,
       flagging an error if anything is unknown"""

    machineCode = [] #allocate pointer for our machine code
    linecount = 1

    for line in code:   #parse through code assebling opcodes for keywords
        opcode = parseInstruction(line[instruction])

        # check to see if instruction parsed properly
        if opcode == badInstruction:
            displayError(linecount, badInstruction, line)#displays error if not
            return 0

        # checks to see if number of operands parsed properly
        if parseOperands(opcode, line[operands]) == incorrectNumberofOperands:
            # display error if not
            displayError(linecount, incorrectNumberofOperands, line)
            return 0

        line[instruction] = opcode
        linecount += 1
        machineCode.append(line)

    return machineCode #return machine code

def parseInstruction(inputInstruction):
    """This function looks up a provided instruction,
    returning its opcode if valid or -1 otherwise"""
    lookupIndex = 0
    for lookup in returnAssemblyTable(): #lookup opcode for instructions

        if inputInstruction == lookup[instruction]:
            return lookupIndex

        lookupIndex +=1

    return badInstruction

def parseOperands(opcode, inputOperands):
    """This function checks that an instruction has the right number of operands
    returning an error value if not"""
    instructionset = returnAssemblyTable()
    correctNumberofOperands = instructionset[opcode][1]
    if correctNumberofOperands == len(inputOperands.split(',')):
        return correctNumberofOperands
    return incorrectNumberofOperands

assemblyTable = readAssemblyTable()
code = parseCodeFile('examplecode.txt')
code = assemble(code)

print code

