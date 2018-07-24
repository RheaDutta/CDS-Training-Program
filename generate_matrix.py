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

#Test Cases 
#mat = [[2,3],[0,0]] #56 states
#num_range = [0,5]

mat = [[2,0],[0,0]] #10 states
num_range = [0,2]

###############################################################################

def compute(mat, num_range):
	"""
	PRINTS: The P-Matrix and the reduced matrix for the given matrix.
			(Can also return the P-Matrix by adding the line - return p_matrix)
	PARAMETERS:	mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	
	#t1 = time.time()
	#First iteration ever
	first_iteration(mat, num_range)
	#print("first_iteration() took: ", time.time()-t1, "seconds.") 	
	
	#t2 = time.time()
	#Next iterations
	iterations(num_range)
	#print("iterations() took: ", time.time()-t2, "seconds.") 
	
	#t3 = time.time()
	#Reordering results. 
	p_matrix = reorder() #this list is the final result
	#print("reorder() took: ", time.time()-t3, "seconds.")
	
	#t4 = time.time()
	#Finding the reduced matrix
	r_matrix = reduced_matrix(p_matrix)
	#print("reduced_matrix: ", r_matrix)
	#print("len(r_matrix): ", len(r_matrix))
	
	#t5 = time.time()
	#Printing results
	#printing_p_matrix(p_matrix)
	printing_r_matrix(r_matrix)
	#print("printing_p_matrix() took: ", time.time()-t5, "seconds.") 
	
	#print("Total states: ", len(all_states_explored))
	#print("len(all_states_explored): ", len(all_states_explored))
	#print("len(all_results): ", len(all_results))
	#print("len(super_states): ", len(super_states))
	#print("super_states: ", super_states)
	
	#all_states = []
	#for sp in super_states:
	#	for s in sp:
	#		all_states.append(s)
	#print("total number of sub_states in super_states: " , len(all_states))
	
	#return p_matrix
	#print(p_matrix)
	
	#For both matrices -
	return [p_matrix, r_matrix]
	
###############################################################################

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

###############################################################################

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
	
###############################################################################

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
	
	#print("working")
	#t1 = time.time()
	#Converting the vector in all_states_explored to a matrix. 
	matrix = pMatrix.make_matrix(all_states_explored[i])
	#print("				=> Converting to matrix took: ", time.time() - t1, "seconds.")
			
	#t2 = time.time()
	#Tree for currrent iteration.
	tree = pMatrix.create_tree(matrix, num_range) 
	#print("				=> Creating the tree took: ", time.time() - t2, "seconds.")
	
	#Adding the tree to all_trees.
	all_trees.append(tree)
			
	#t3 = time.time()
	#Calculating the number of states in current iteration.
	num_states = tree.get_num_states()
	#print("				=> Calculating num_states took: ", time.time() - t3, "seconds.")
		
	#Adding total number of states to all_total_states. 
	all_total_states.append(num_states) 
		
	#t4 = time.time()
	#Finding results for each iteration.
	r = pMatrix.main(matrix, num_range)
	#print("				=> Finding results took: ", time.time() - t4, "seconds.")
		
	#Adding results for current iteration to all_results. 
	all_results.append(r)
		
	#t5 = time.time()
	#Finding any new, previously unseen state and adding it to
	#all_states_explored list so as to explore it. 
	find_new_states(tree)
	#print("				=> Finding new states took: ", time.time() - t5, "seconds.")
	
	#Adding super_states
	update_super_states(tree)
	
	#print("done")

###############################################################################

def update_super_states(tree):
	"""
	Updates the global list super_states to reflect new super_states.
	
	PARAMETERS: tree [pMatrix.tree object]: The Tree object of the state whose
				probability row matrix is being calculated.
	
	"""
	
	sp_st = tree.get_super_states()
	
	for i in range(len(sp_st)):
		
		sample_state = sp_st[i][0]
		
		present = False
		for super_state in super_states:
			if sample_state in super_state:
				present = True
				break
		
		if present is False:
			super_states.append(sp_st[i])
	
###############################################################################

def printing_p_matrix(new_all_results):
	"""
	Prints the P-Matrix in iterations. 
	
	PARAMETERS: new_all_results [list] - The P-Matrix required in the form of a 3D list.
	
	"""
	for i in range(len(new_all_results)):
		print("Row Number: ", i+1)
		print("Vector: ", all_states_explored[i])
		print("Number of columns: ", len(new_all_results[i]))
		print("Result: ", new_all_results[i])
		print("-------------------------------------------------------------------------------------")

###############################################################################

def printing_r_matrix(r_matrix):
	
	s = 0
	for l in r_matrix:
		print("Super State #: ", r_matrix.index(l))
		for tup in l:
			print("Column #: ", l.index(tup))
			print("Result: ", tup)
			print("-------------------------------------------------------------------------------------")
			s+=1

	print("Total number of tuples = ", s)

###############################################################################

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

###############################################################################

def reorder():
	"""
	RETURNS: A reordered form of matrix all_results such that the order of rows is
	the same as the order of columns.
	
	"""
	
	new_all_results = []
	for i in range(0, len(all_states_explored)):
		new_all_results.append(reorder_helper(all_trees[i], all_total_states[i], all_results[i]))
		
	return new_all_results 

###############################################################################

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
	
###############################################################################

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

###############################################################################

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

###############################################################################

def reduced_matrix_helper2(r_matrix):

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
	
###############################################################################
#Keeping track of how long the program takes to run. 
#start_time = time.time()

#Executing the script. 
compute(mat,num_range)

#print("generate_matrix.py took ", time.time() - start_time, "seconds to run.")