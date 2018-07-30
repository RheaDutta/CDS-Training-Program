#Does not use Multithreading or Multiprocessing to find the P-Matrix.
#Produces P-Matrix using sequential computations.
#Generates reduced matrix.

"""
Program to generate a P-Matrix.

Functions in the program -
	a) compute()
	b) first_iteration()
	c) iterations()
	d) do()
	e) update_super_states()
	f) printing_results()
	g) find_new_states()
	h) reorder()
	i) reorder_helper()
	j) reduced_matrix()
	k) reduced_matrix_helper()
	l) reduced_matrix_helper2()

Written by - Rhea Dutta. Date - 07/23/2018.
"""

"""pMatrix script computes the probabilities associated with one state (one tree).
It essentially gives one row in the pMatrix."""

import pMatrix
import time
import itertools

#Global lists
all_results = []
all_states_explored = []
all_trees = []
all_total_states = []
super_states = []

#-----------------------------------------------------------------------------#

def compute(input, must_print):
	"""
	PRINTS: The P-Matrix and the reduced #matrix for the given matrix.

	PARAMETERS:	mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
				input[list]: [mat, num_range]
				must_print [bool]: True if results must be printed, False otherwise.
	
	"""
	
	#Input
	mat = input[0]
	num_range = input[1]

	#First iteration ever
	first_iteration(mat, num_range)
	
	#Next iterations
	iterations(num_range)
	
	#Reordering results. 
	reordered_p_matrix = reorder()
	
	#Simplifying the P-Matrix
	p_matrix = compress_p_matrix(reordered_p_matrix)
	
	#Finding the reduced matrix
	r_matrix = reduced_matrix(reordered_p_matrix)
	
	#Printing results
	if must_print:
		printing_p_matrix(p_matrix)
		printing_r_matrix(r_matrix)
		print_summary(p_matrix, r_matrix)
	
	return [p_matrix, r_matrix]
	
#-----------------------------------------------------------------------------#

def first_iteration(mat, num_range):
	"""
	Fourfold function -
	-> Creates tree for the first iteration and adds it to the global list all_trees.
	-> Calculates the total number of states in the first iteration and adds it to the
		global list all_total_states.
	-> Finds all states that must be explored in the first iteration and adds it to the
		golbal list all_states_explored.
	-> Finds the probability row matrix for the given matrix and adds this row to the
		global matrix all_results.
	
	PARAMETERS: mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	#Creating the tree for the first iteration. 
	tree = pMatrix.create_tree(mat, num_range)
	
	#Adding the tree to all_trees. 
	all_trees.append(tree)
	
	#Calculating the total number of states in the first iteration.
	num_states = tree.get_num_states()
	
	#Adding total number of states for the first iteration to all_total_states.
	all_total_states.append(num_states)
	
	#Adding all states to be explored in the first iteration to all_states_explored.
	for st in tree.get_all_states():
		all_states_explored.append(st)
		
	#Adding super states from first tree to super_states.
	for sp in tree.get_super_states():
		super_states.append(sp)
	
	#Adding results for first iteration to final list.
	all_results.append(pMatrix.main(mat, num_range))

#-----------------------------------------------------------------------------#

def iterations(num_range):
	"""
	Finds probability row matrix for all the vectors (i.e. states) in the all_states_explored
	list and builds the all_results P-Matrix. 
	
	PARAMETERS: num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	
	i=1
	
	while i<len(all_states_explored):
		
		do(num_range,i)
		
		#Incrementing iterator. 	
		i+=1
	
#-----------------------------------------------------------------------------#

def do(num_range,i):	
	"""
	Fourfold function -
	-> Creates tree for the current iteration and adds it to the global list all_trees.
	-> Calculates the total number of states in the current iteration and adds it to the
		global list all_total_states.
	-> Finds all states that must be explored in the current iteration and adds it to the
		golbal list all_states_explored.
	-> Finds the probability row matrix for the given matrix and adds this row to the
		global matrix all_results.
	
	PARAMETERS: num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
				i [int]: Iterator that iterates through all_states_explored list.
	"""
	
	#Converting the vector in all_states_explored to a matrix. 
	matrix = pMatrix.make_matrix(all_states_explored[i])
	
	#Tree for currrent iteration.
	tree = pMatrix.create_tree(matrix, num_range) 
	
	#Adding the tree to all_trees.
	all_trees.append(tree)
	
	#Calculating the number of states in current iteration.
	num_states = tree.get_num_states()
		
	#Adding total number of states to all_total_states. 
	all_total_states.append(num_states) 
	
	#Finding results for each iteration.
	r = pMatrix.main(matrix, num_range)
		
	#Adding results for current iteration to all_results. 
	all_results.append(r)
	
	#Finding any new, previously unseen state and adding it to all_states_explored list.
	find_new_states(tree)
	
	#Adding super_states
	update_super_states(tree)

#-----------------------------------------------------------------------------#

def update_super_states(tree):
	"""
	Updates the global list super_states to reflect new super_states.
	
	PARAMETERS: tree [pMatrix.tree object]: The Tree object of the state whose
				probability row matrix is being calculated.
	
	"""
	
	sp_st = tree.get_super_states()
	
	for i in range(len(sp_st)):
		
		sample = sp_st[i][0]

		present = False
		for super_state in super_states:
			if sample in super_state:
				present = True
				break

		if present is False:
			super_states.append(sp_st[i])
		
#-----------------------------------------------------------------------------#

def printing_p_matrix(new_all_results):
	"""
	Prints the P-Matrix in iterations. 
	
	PARAMETERS: new_all_results [list] - The P-Matrix required in the form of a 3D list.
	
	"""
	print("________________________________PROBABILITY MATRIX__________________________________ ")
	for i in range(len(new_all_results)):
		print("Row Number: ", i+1)
		print("Vector: ", all_states_explored[i])
		print("Number of columns: ", len(new_all_results[i]))
		print("Result: ", new_all_results[i])
		print("-------------------------------------------------------------------------------------")
	print("____________________________________________________________________________________")

#-----------------------------------------------------------------------------#

def printing_r_matrix(r_matrix):
	
	print("________________________________REDUCED MATRIX______________________________________")
	for l in r_matrix:
		print("Super State #: ", r_matrix.index(l))
		for tup in l:
			print("Column #: ", l.index(tup))
			print("Result: ", tup)
			print("-------------------------------------------------------------------------------------")
	print("____________________________________________________________________________________")

#-----------------------------------------------------------------------------#

def find_new_states(tree):
	"""
	Adds any new, previously unseen states in the current tree to be explored
	to all_states_explored.
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
				iteration of the program.
				num_states [int]: The total number of states present in the given
				tree.
	
	"""
	row = tree.get_all_states()
	
	for state in row:
		if state not in all_states_explored:
				all_states_explored.append(state)

#-----------------------------------------------------------------------------#

def reorder():
	"""
	RETURNS: A reordered form of matrix all_results such that the order of rows is
	the same as the order of columns.
	
	"""
	
	new_all_results = []
	for i in range(0, len(all_states_explored)):
		new_all_results.append(reorder_helper(all_trees[i], all_total_states[i], all_results[i]))
		
	return new_all_results 

#-----------------------------------------------------------------------------#

def reorder_helper(tree, num_states, result):
	"""
	RETURNS: The reordered form of the probability row matrix corresponding to the
			given tree and result such that the order of the rows is the same as the
			order of the columns.
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
											iteration of the program.
				num_states [int]: The total number of states present in the given
								tree.
				result [list]: The 2D list that contains the probability row matrix
								of the given tree. 	
	
	"""
	
	states = tree.get_all_states()
	
	new_result = [[0]]*len(all_states_explored)
	
	for state in states:
		for existing_state in all_states_explored:
			if state == existing_state:
					pos = states.index(state)
					new_result[all_states_explored.index(existing_state)]=result[pos]
					
	return new_result
	
#-----------------------------------------------------------------------------#

def reduced_matrix(p_matrix):
	"""
	RETURNS: A condensed version of the p_matrix where the states are super_states
			associated with the p_matrix.
	
	PARAMETERS: p_matrix [list] : The P-Matrix required in the form of a 3D list.
	
	"""
	reduced_matrix = []
	for super_state in super_states:
		n = len(super_state)
		row = []
		for other_super_state in super_states:
			result = reduced_matrix_helper(p_matrix, super_state, other_super_state)
			row.append((n, result))
		reduced_matrix.append(row)
	
	
	return reduced_matrix_helper2(reduced_matrix)

#-----------------------------------------------------------------------------#

def reduced_matrix_helper(p_matrix, super_state, other_super_state):
	"""
	RETURNS: One element of the reduced matrix. 
	
	PARAMETERS: p_matrix [list] : The P-Matrix required in the form of a 3D list.
				super_state [2D list] : The super_state whose probability row is being
										calculated.
				other_super_state [2D list]
	
	"""
	result = []
	for sub_state in super_state:
		i = all_states_explored.index(sub_state)
		for other_sub_state in other_super_state:
			j = all_states_explored.index(other_sub_state)
			probability = p_matrix[i][j]
			result.append(probability)
	return result	

#-----------------------------------------------------------------------------#

def reduced_matrix_helper2(r_matrix):
	"""
	RETURNS: A compressed version of the reduced matrix where every tuple is in
			the format (n, numerator, denominator). The number required is
			[(numerator/denominator)*n].
	"""

	new_r_matrix = []
	
	for row in r_matrix:
		new_row = []
		
		for tup in row:
			
			n = tup[0]
			prob_list = tup[1]
			
			denominators = []
			for prob in prob_list:
				for p in prob:
					if p not in denominators and p!=0:
						denominators.append(p)
			
			denominator = 1
			for m in denominators:
				denominator = denominator*m
				
			numerators = []
			for prob in prob_list:
				for p in prob:
					if p!=0:
						numerators.append(denominator//p)
				
			numerator = sum(numerators)
			
			new_tup = (n, numerator, denominator)
			new_row.append(new_tup)
		new_r_matrix.append(new_row)
	
	return new_r_matrix
	
#-----------------------------------------------------------------------------#

def print_summary(p_matrix, r_matrix):
	
	print("________________________________SUMMARY OF DATA_____________________________________")
	print(" 1. P-Matrix")
	print("		-> Number of states: ", len(all_states_explored))
	print("		-> Number of rows in P-Matrix: ", len(p_matrix))
	print(" 2. Reduced P-Matrix")
	print("		-> Number of super states: ", len(super_states))
	print("		-> Number of rows in reduced P-Matrix: ", len(r_matrix))
	
	s = 0
	for st in super_states:
		s+=len(st)
		
	print("		-> Total number of sub states: ", s)
	print("____________________________________________________________________________________")

#-----------------------------------------------------------------------------#

def compress_p_matrix(p_matrix):
	
	#Produces the P-Matrix in a compressed form in format - [numerator, denominator]
	
	simple_p_matrix = []
	for row in p_matrix:
		new_row = []
		for p in row:
			if p[0]==0:
				new_p = [0]
			else:
				n = len(p)
				new_p = [n, p[0]] #[numerator, denominator]
			new_row.append(new_p)
		simple_p_matrix.append(new_row)	
	
	return simple_p_matrix		
	
#-----------------------------------------------------------------------------#


#Keeping track of how long the program takes to run. 
#start_time = time.time()

#Executing the script. 
#compute(mat,num_range)

#print("generate_matrix.py took ", time.time() - start_time, "seconds to run.")
#print("____________________________________________________________________________________")