#Does not use Multithreading or Multiprocessing to find the P-Matrix.
#Produces P-Matrix using sequential computations. 

"""
Program to generate a P-Matrix.

Functions in the program -
	a) compute()
	b) first_iteration()
	c) iterations()
	f) make_matrix()
	g) printing_results()
	h) find_new_states()
	j) reorder()
	k) reorder_helper()

Written by - Rhea Dutta. Date - 06/16/2018.
"""

"""pMatrix script computes the probabilities associated with one state (one tree).
It essentially gives one row in the pMatrix."""

import pMatrix
import threading
import time

#Global lists
all_results = []
all_states_explored = []
all_trees = []
all_total_states = []
super_states = [] 

#Test Cases 
mat = [[2,0],[0,0]] #10 states
num_range = [0,2]

###############################################################################

def compute(mat, num_range):
	"""
	PRINTS: The P-Matrix for the given matrix.
			(Can also return the P-Matrix by adding the line - return new_all_results)
	PARAMETERS:	mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	
	#t1 = time.time()
	#First iteration ever
	if len(all_states_explored)==0:
		first_iteration(mat, num_range)
	#print("first_iteration() took: ", time.time()-t1, "seconds.") 	
	
	#t2 = time.time()
	#Next iterations
	iterations(num_range)
	#print("iterations() took: ", time.time()-t2, "seconds.") 
	
	#t3 = time.time()
	#Reordering results. 
	new_all_results = reorder() #this list is the final result
	#print("reorder() took: ", time.time()-t3, "seconds.") 
	
	#t4 = time.time()
	#Printing results
	#printing_results(new_all_results)
	#print("printing_results() took: ", time.time()-t4, "seconds.") 
	
	#print("Total states: ", len(all_states_explored))
	
	print("len(all_states_explored): ", len(all_states_explored))
	print("len(all_results): ", len(all_results))
	#return new_all_results
	
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
	
	#print("working")
	#t1 = time.time()
	#Converting the vector in all_states_explored to a matrix. 
	matrix = make_matrix(i)
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
	find_new_states(tree, num_states)
	#print("				=> Finding new states took: ", time.time() - t5, "seconds.")
	#print("done")

###############################################################################

def make_matrix(i):
	"""
	Makes matrix out of the current vector being processed in all_states_explored.
	
	PARAMETERS: i [int]: Iterator for the while loop in iterations. 
	
	"""
	
	vector = all_states_explored[i]
	matrix = []
	for j in range(0, len(vector),2):
		matrix.append([vector[j],vector[j+1]])
			
	return matrix

###############################################################################

def printing_results(new_all_results):
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

def find_new_states(tree, num_states):
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

#Keeping track of how long the program takes to run. 
start_time = time.time()

#Executing the script. 
compute(mat,num_range)

print("pMatrix_main_draft3.py took ", time.time() - start_time, "seconds to run.")