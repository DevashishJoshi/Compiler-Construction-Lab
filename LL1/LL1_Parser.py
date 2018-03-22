'''
cd VJTI Lab/Sem 6 Lab/CC
py -2 LL1_Parser.py
'''
import re, string, pandas as pd, numpy as np
from tabulate import tabulate
from first import first
from follow import follow

def parse(input_string, parsing_table, start):

	print('Stack\t\tInput\t\tAction')

	input_string = input_string + '$' #Append end of input sign
	stack = ['$', start] #Push end of input and start symbol in stack
	i = 0 #Iterator over input string
	action = 'Push'
	flag=False

	while len(stack)!=0 and i<len(input_string):
		print(''.join(stack)+'\t\t'+input_string[i:]+'\t\t'+action)
		#action='Pop'
		top_of_stack = stack.pop()

		if top_of_stack.isupper(): #Top of stack is a non terminal
			if (top_of_stack, input_string[i]) not in parsing_table: #No entry in parsing table, Error
				return False
			table_entry = parsing_table[top_of_stack, input_string[i]] #Found in table
			if table_entry=='@': #Table entry is epsilon production; nothing to be done
				continue
			for char in table_entry[::-1]: #Push reverse of production in table entry in the stack
				stack.append(char)
				action='Push'
				flag = True

		else: #Top of stack is a terminal
			flag=False
			if top_of_stack!=input_string[i]: #Top of stack doesn't match with input string char
				return False
			else:
				i=i+1 #Move the iterator forward (No need to pop from stack as it going to be done at the start of next iteration)
		if not flag:
			action='Pop'
	return True

def ll1(follow_dict, productions):
	
	table = {}
	for key in productions:
		for value in productions[key]: #For each production
			if value!='@': #If not an epsilon production, find first of the production and add in row of non terminal and column of first of production
				for element in first(value, productions):
					table[key, element] = value
			else: #If epsiolon production, find follow of the non terminal and add in row of non terminal and column of follow of the non terminal
				for element in follow_dict[key][0]:
					table[key, element] = value

	#Processing only to make the table look good
	parsing_table = {}
	for pair in table:
		parsing_table[pair[1]] = {}
	
	for pair in table:		
		parsing_table[pair[1]][pair[0]] = table[pair]

	df = pd.DataFrame(parsing_table).fillna('-')
	print tabulate(df, headers='keys', tablefmt='psql')

	return table

#Function main
if __name__=="__main__":
	
	productions=dict()
	#Read the grammar
	grammar = open("grammar", "r")
	#To store first and follow
	first_dict = dict()
	follow_dict = dict()
	#To find start symbol, the lhs of first production
	flag = 1
	start = ""
	for line in grammar:
		l = re.split('( |->|\n|\||)*', line)
		lhs = l[0]
		rhs = set(l[1:])-{''}
		if flag :
			flag = 0
			start = lhs
		productions[lhs] = rhs
	
	print('First')
	for lhs in productions:
		first_dict[lhs] = first(lhs, productions)
	for f in first_dict:
		print(str(f) + ' : ' + ', '.join(str(x) for x in first_dict[f]))
	print('')
	
	print('Follow')
	for lhs in productions:
		#First term represents follow, second term represents if it is valid or not
		follow_dict[lhs] = [set(), False]

	#Add end of input symbol in follow set of first
	follow_dict[start][0] = follow_dict[start][0].union('$')

	for lhs in productions:
		#Find follow of each non terminal (LHS of each production)
		follow_dict = follow(lhs, productions, follow_dict)
	
	for f in follow_dict:
		print(str(f) + ' : ' + ', '.join(str(x) for x in follow_dict[f][0]))
	print('')

	print('LL1 Parsing table')
	parsing_table = ll1(follow_dict, productions)
	print('')

	print('LL1 Parsing')
	input_string = str(raw_input('Enter the input string : '))
	#input_string = '(a+a*a)*(a*(a+a))'
	p = parse(input_string, parsing_table, start)
	if p:
		print('Parsed successfully')
	else:
		print('Parsing failed')
