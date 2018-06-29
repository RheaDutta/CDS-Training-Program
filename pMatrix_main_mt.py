#Produces P-Matrix using Multithreading. 

"""
Program to generate a P-Matrix.

Functions in the program -
	a) compute()
	b) first_iteration()
	c) iterations()
	d) calculate_num_states()
	e) add_first_iteration()
	f) make_matrix()
	g) printing_results()
	h) find_new_states()
	i) return_all_states()
	j) reorder()
	k) reorder_helper()

Written by - Rhea Dutta. Date - 06/16/2018.
"""

"""pMatrix script computes the probabilities associated with one state (one tree).
It essentially gives one row in the pMatrix."""

###############################################################################

import pMatrix
import threading 
import time

#---------------Global lists---------------#

mega_list = []
#It is a list of tuples. Each tuple contains elements in the format (state,result,
#num_states,tree). Each tuple corresponds to a state that has been explored and
#each element of the tuple represents some aspect of the computations done on the
#respective state.

all_states_explored = []
#This list will contain all states to be explored.

#---------------Test Cases---------------#

#mat = [[2,0],[0,0]] #10 states
#num_range = [0,2]

#mat = [[3,1],[0,0]] #35 states
#num_range = [0,4]

#mat = [[2,3],[0,0]] #56 states
#num_range = [0,5]

#mat = [[0,10],[0,0]] #0 states
#num_range = [0,1]

#mat = [[0,10],[0,0],[0,0]]
#num_range = [0,10]

#mat = [[0,6],[0,0]] #84 states
#num_range = [0,6]

#mat = [[0,7],[0,0]] # states
#num_range = [0,7]

mat = [[0,9],[0,0]] # states
num_range = [0,9]

#mat = [[0,10],[0,0]] # states
#num_range = [0,10]

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
	t1 = time.time()
	#First Iteration
	first_iteration(mat, num_range)
	print("first_iteration() took: ", time.time() - t1, "seconds.")
	
	t2 = time.time()
	#Next iterations
	iterations(num_range)
	print("iterations() took: ", time.time() - t2, "seconds." )
		
	t3 = time.time()
	#Making sure that all threads are done before moving on.
	for thread in threading.enumerate():  
		if thread.name != 'MainThread':
			thread.join()
	print("Joining threads took: ", time.time() - t3, "seconds.")
	
	t4 = time.time()
	#Reordering results. 
	all_results = reorder()
	print("reorder() took: ", time.time() - t4, "seconds.")
	
	#t5 = time.time()
	#Printing results
	#printing_results(all_results)
	#print("printing_results() took: ", time.time() - t5, "seconds.")
	
	print("Total number of states: ", len(all_results))
	
	#return all_results
	
###############################################################################

def first_iteration(mat, num_range):
	"""
	Functions -
	-> Creates tree for the first iteration, calculates the total number of states
		in the first iteration, finds the probability row matrix for the given matrix,
		and converts the given matrix to a vector.
	-> All of the above information is then stored in a tuple and appended to the
		mega_list.
	-> Finds all states that must be explored in the first iteration (by calling
		add_first_iteration) and adds it to the global list all_states_explored.
	
	PARAMETERS: mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	#Converting the matrix into a vector.
	state = pMatrix.matrix_to_vector(mat)
	
	#Finding the probability row matrix for this state. 
	result = pMatrix.main(mat, num_range)
	
	#Creating the tree for the first iteration. 
	tree = pMatrix.create_tree(mat, num_range)
	
	#Calculating the total number of states in the first iteration.
	num_states = calculate_num_states(tree)
	
	#Making a tuple out of the above elements.
	tup = (state,result,num_states,tree)
	
	#Adding the tuple to the mega_list.
	mega_list.append(tup)
	
	#Finding all states to be explored in the first iteration
	#and adding to all_states_explored list.
	add_first_iteration(tree, num_states)
	
###############################################################################

def add_first_iteration(tree, num_states):
	"""
	Appends all states to be explored in first iteration to all_states_explored list.
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
				iteration of the program.
				num_states [int]: The total number of states present in the given
				tree.
	
	"""
	l = return_all_states(tree, num_states)
	for ele in l:
		all_states_explored.append(ele)
	
###############################################################################

def iterations(num_range):
	"""
	Finds probability row matrix for all the vectors (i.e. states) in the all_states_explored
	list and builds the all_results P-Matrix. 
	
	PARAMETERS: num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	t6 = time.time()
	print("		-> Creating threads.")
	
	#First iteration has been computed in first_iteration function. Thus, iterations
	#begin at the second element. 
	i=1
	
	while i<len(all_states_explored):
		
		#Creating thread. 
		t = threading.Thread(target = do, args = (num_range,i))
		
		#Starting the thread. 
		t.start()
		
		#Incrementing iterator. 	
		i+=1
	
	print("		-> Creating threads took: ", time.time() - t6, "seconds.")
###############################################################################

def do(num_range,i):
	
	t0 = time.time()
	
	t1 = time.time()
	#Converting the vector in all_states_explored to a matrix. 
	matrix = make_matrix(i)
	#print("				=> Converting to matrix took: ", time.time() - t1, "seconds.")
			
	t2 = time.time()
	#Tree for currrent iteration.
	tree = pMatrix.create_tree(matrix, num_range)
	#print("				=> Creating the tree took: ", time.time() - t2, "seconds.")
		
	t3 = time.time()
	#Calculating the number of states in current iteration.
	num_states = calculate_num_states(tree)
	#print("				=> Calculating num_states took: ", time.time() - t3, "seconds.")
	
	#t4 = time.time()
	#Finding results for each iteration.
	result = pMatrix.main(matrix, num_range)
	#print("				=> Finding results took: ", time.time() - t4, "seconds.")
	
	#t6 = time.time()
	#Adding all the above information to a tuple.
	tup = (all_states_explored[i], result, num_states, tree)
	
	#Adding the tuple to mega_list.
	mega_list.append(tup)
	#print("				=> Appending stuff took: ", time.time() - t6, "seconds.")
	
	t5 = time.time()
	#Finding any new, previously unseen state and adding to
	#all_states_explored.
	find_new_states(tree, num_states)
	#print("				=> Finding new states took: ", time.time() - t5, "seconds.")
	
	#print("				=> Thread # ", i, "done: ", time.time() - t0, "seconds.")
	
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
	row = return_all_states(tree, num_states)
	
	for state in row:
		if state not in all_states_explored:
				all_states_explored.append(state)
	
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

def return_all_states(tree, num_states):
	"""
	Returns all states in the tree.
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
				iteration of the program.
				num_states [int]: The total number of states present in the given
				tree.
	
	""" 

	l = []
	
	for k in range(1, num_states+1):
		for i in tree.get_children():
			for j in i.get_children():
				if j.get_state_number()==k:
					l.append(j.get_state())
					break
			if j.get_state_number()==k:
				break
			
	return l

###############################################################################

def reorder():
	"""
	RETURNS: A reordered form of matrix all_results such that the order of rows is
	the same as the order of columns.
	
	"""
	all_results = []*len(mega_list)
	#This is the required P-Matrix.
	
	for i in range(0, len(mega_list)):
		t = threading.Thread(target = reorder_helper, args = (mega_list[i],i,all_results))
		t.start()
		
	#Making sure that all threads are done before moving on.
	for thread in threading.enumerate():  
		if thread.name != 'MainThread':
			thread.join()
			
	return all_results

###############################################################################

def reorder_helper(tup,i,all_results):
	"""
	RETURNS: The reordered form of the probability row matrix corresponding to the
			given tree and result such that the order of the rows is the same as the
			order of the columns.
	
	PARAMETERS: tup [tuple]: Tuple that contains the elements in the following format -
				(state, result num_states, tree)
				i [int]: The position of the tuple in mega_list. 
	
	"""
	
	#All information in tup.
	state = tup[0]
	result = tup[1]
	num_states = tup[2]
	tree = tup[3]
	
	#All states that are in the tree.
	states = return_all_states(tree,num_states)
	
	#The reordered result. 
	new_result = [0]*len(mega_list)
	
	for i in range(len(mega_list)):	
		for state in states:
			for existing_state in mega_list[i]:
				#print(existing_state)
				if state == existing_state:
						pos = states.index(state)
						new_result[i]=result[pos]
					
	all_results.insert(i, new_result)
	
###############################################################################

def calculate_num_states(tree):
	"""
	Calculates the total number of states in the given tree. 
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
				iteration of the program. 
	
	"""
	
	#Calculating num_states - the number of states in first iteration. 
	num_states = 0
	for i in tree.get_children():
		for j in i.get_children():
			if j.get_state_number()>num_states:
				num_states = j.get_state_number()
	
	return num_states

###############################################################################

def printing_results(all_results):
	"""
	Prints the P-Matrix in iterations. 
	
	PARAMETERS: new_all_results [list] - The P-Matrix required in the form of a 3D list.
	
	"""
	for i in range(len(all_results)):
		print("Row Number: ", i+1)
		print("Vector: ", mega_list[i][0])
		print("Number of columns: ", len(all_results[i]))
		print("Result: ", all_results[i])
		print("-------------------------------------------------------------------------------------")

###############################################################################

#Keeping track of how long the program takes to run. 
start_time = time.time()

#Executing the script. 
compute(mat,num_range)

print("pMatrix_main.py took ", time.time() - start_time, "seconds to run.")

###############################################################################