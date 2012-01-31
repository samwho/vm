import sys
import re

class lexer: # enum class to seperate instructions from operands etc.
	INSTRUCTION=0
	OPERAND=1
	OPERATOR=2
	DIGIT=3
	COMMENT=4
	END_STMNT=5

def instruction(scanner, token): # called when scanner comes across an instruction
	lookupIndex=0
	for lookup in assemblyTable: # lookup opcode for instructions
		if token == lookup[0]:
			return lexer.INSTRUCTION, lookup[1]
	return -1, token

def operator(scanner, token): # called when scanner comes across an operator
	return lexer.OPERATOR, token

def operand(scanner, token): # called when scanner comes across an operand
	#token = token.rstrip(',')
	for lookup in operandTable: # loopup operand in operand table
		if token == lookup[0]:
			return lexer.OPERAND, lookup[1]
	return -1, token

def digit(scanner, token): # called when scanner comes across a digit
	return lexer.DIGIT, token

def end_stmnt(scanner, token): # called when scanner comes across an end of line
	return lexer.END_STMNT, "END_STATEMENT"

def comment(scanner, token): # called when scanner comes across a comment
	return lexer.COMMENT, token

def token(code):
	machineCode=""
	i=0
	while i < code.length:
		tmp=[]
		while code[i][0] != lexer.END_STMNT: # get one line of file
			tmp.append(code[i][1])
		assemble(tmp) # assemble line
	return machineCode

def assemble(code):
	returnvar=""
	for i in code: # for each token in the code handle the token
		evaluate={
			lexer.INSTRUCTION: handleInstruction(returnvar, i),
			lexer.OPERAND: handleOperand(returnvar, i),
			lexer.OPERATOR: handleOperator(returnvar, i),
			lexer.DIGIT: handleDigit(returnvar, i),
		}
		returnvar = evaluate.get(i[0], returnvar) # equivalent of switch statement
	return returnvar

def handleInstruction(cur, i): # convert instruction to machine code
	cur += " " + str(i[1])
	return cur

def handleOperand(cur, i): # convert operand into machine code
	cur += " " + str(i[1])
	return cur

def handleOperator(cur, i): # convert operator into machine code
	cur += " " + str(i[1])
	return cur

def handleDigit(cur, i): # convert digit into machine code
	cur += " " + str(i[1])
	return cur

scanner = re.Scanner([
   (r"//.*", comment), # find comments in code
   (r"[A-Z]+", instruction), # find instructions in code
   (r"[a-zA-Z0-9]+,??", operand), # find operands in code
   (r"[+\-*/=]", operator), # find operators in code
   (r"[0-9]+(\.[0-9]+)?", digit), # find digits in code
   (r"\n", end_stmnt), # find end of line
   (r"\s+", None) # do nothing with the rest
])

assemblyTable=[ ['MOV', 'MOV'], ['JMP', 'JMP'] ] # assembly table
operandTable=[ ['ax', 'ax'], ['bx', 'bx'] ] # operand table
file = open(sys.argv[1])
tokens, remainder = scanner.scan(file.read())
#tokens = assemble(tokens)
print(tokens)
