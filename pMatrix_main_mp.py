#Find P-Matrix using Multiprocessing and Queues. Very slow as compared to sequential version. 

#__________________________________________________________________________________________#

import pMatrix
import multiprocessing as mp 
import time

#---------------Global lists---------------#

mega_list = []
#It is a list of tuples. Each tuple contains elements in the format (state,result,
#num_states,tree). Each tuple corresponds to a state that has been explored and
#each element of the tuple represents some aspect of the computations done on the
#respective state.

all_states_explored = []
#This list will contain all states to be explored.

super_states = []
#Contains all the superstates. 2D list.
	
#---------------Test Cases---------------#


mat = [[2,3],[0,0]] #56 states
num_range = [0,5]

#mat = [[0,6],[0,0]] #84 states
#num_range = [0,6]

#mat = [[2,0],[0,0]] #10 states
#num_range = [0,2]

#mat = [[2,1],[0,0]] #20 states
#num_range = [0,3]

#_____________________________________________________________________________#

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
	#First Iteration
	first_iteration(mat, num_range)
	#print("first_iteration() took: ", time.time()-t1, "seconds.")
	
	#t2 = time.time()
	#Next iterations
	next_iterations(num_range)
	#print("next_iterations() took: ", time.time()-t2, "seconds.")
	
	for i in range(len(mega_list)):
		t = mega_list[i][3]
		update_super_states(t)
	
	#t3 = time.time()
	#Reordering results. 
	p_matrix = reorder()
	#print("reorder() took: ", time.time()-t3, "seconds.")
	
	#t4 = time.time()
	#Generating the reduced probability matrix. 
	r_matrix = reduced_matrix(p_matrix)
	#print("reduced_matrix() took: ", time.time()-t4, "seconds.")
	
	#t5 = time.time()
	#Printing results
	#printing_p_matrix(p_matrix)
	#printing_r_matrix(r_matrix)
	print_summary(p_matrix, r_matrix)
	#print("printing results took: ", time.time()-t5, "seconds.")
	
	#return (p_matrix, r_matrix)
	
#_________________________PROBABILITY MATRIX FUNCTIONS________________________#

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
	num_states = tree.get_num_states()
	
	#Making a tuple out of the above elements.
	tup = (state,result,num_states,tree)
	
	#Adding the tuple to the mega_list.
	mega_list.append(tup)
	
	#Adding all states to be explored in the first iteration to all_states_explored.
	for st in tree.get_all_states():
		all_states_explored.append(st)
		
	#Adding super states from first tree to super_states.
	for sp in tree.get_super_states():
		super_states.append(sp)
	
#-----------------------------------------------------------------------------#

def next_iterations(num_range):
	"""
	Finds probability row matrix for all the vectors (i.e. states) in the all_states_explored
	list and builds the all_results P-Matrix. 
	
	PARAMETERS: num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	#First iteration has been computed in first_iteration function. Thus, iterations
	#begin at the second element. 
	i=1
	
	#List of processes.
	process_list = []
	
	while i<len(all_states_explored):
		
		#Will contain a copy of all_states_explored at this point.
		states_q = all_states_explored
		
		#Vector for current iteration.
		vector = all_states_explored[i]
		
		#Creating a queue to store results from the process.
		q = mp.Queue()
		
		#Creating process. 
		p = mp.Process(target = add_next_iterations, args = (num_range,vector,q,states_q))
		
		#Adding process to process_list. 
		process_list.append(p)
		
		#Starting the process. 
		p.start()
		
		#Extracting results. 
		result = q.get()
		
		#Adding the tuple to mega_list.
		mega_list.append(result[0])
		
		#Adding new states to all_states_explored. 
		if len(result[1])!=0:
			for s in result[1]:
				all_states_explored.append(s)
		
		#Incrementing iterator. 	
		i+=1
	
	#Making sure that all processes are done before moving on.
	for p in process_list:  
		p.join()
	
#-----------------------------------------------------------------------------#

def add_next_iterations(num_range,vector,q,states_q):
	
	#Converting the vector in all_states_explored to a matrix. 
	matrix = pMatrix.make_matrix(vector)
	
	#Tree for currrent iteration.
	tree = pMatrix.create_tree(matrix, num_range)
	
	#Calculating the number of states in current iteration.
	num_states = tree.get_num_states()
	
	#Finding results for each iteration.
	result = pMatrix.main(matrix, num_range)
	
	#Adding all the above information to a tuple.
	tup = (vector, result, num_states, tree)
	
	#Finding any new, previously unseen state and adding to new_states.
	new_states = find_new_states(tree, num_states, states_q)
	
	#Adding the results to the Queue q. 
	q.put([tup, new_states])#, new_super_states])
	
#-----------------------------------------------------------------------------#

def reorder():
	"""
	RETURNS: A reordered form of matrix all_results such that the order of rows is
	the same as the order of columns.
	
	"""
	#This is the required P-Matrix.
	all_results = []*len(mega_list)
	
	process_list = []
	
	for i in range(0, len(mega_list)):
		new_result = [[0]]*len(mega_list) #The reordered result for each iteration.
		q = mp.Queue()
		p = mp.Process(target = reorder_helper, args = (mega_list[i],i,new_result, mega_list,q))
		process_list.append(p)
		p.start()
		all_results.insert(i, q.get())
		
	#Making sure that all processes are done before moving on.
	for p in process_list:  
		p.join()
	
	return all_results

#-----------------------------------------------------------------------------#

def reorder_helper(tup,i,new_result, mega_list,q):
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
	states = tree.get_all_states()
	
	for i in range(len(mega_list)):
		for state in states:
			for existing_state in mega_list[i]:
				if state == existing_state:
					pos = states.index(state)
					new_result[i]=result[pos]
	
	q.put(new_result)
	
#-----------------------------------------------------------------------------#

def printing_p_matrix(p_matrix):
	"""
	Prints the P-Matrix in iterations. 
	
	PARAMETERS: new_all_results [list] - The P-Matrix required in the form of a 3D list.
	
	"""
	print("________________________________PROBABILITY MATRIX__________________________________ ")
	for i in range(len(p_matrix)):
		print("Row Number: ", i+1)
		print("Vector: ", mega_list[i][0])
		print("Number of columns: ", len(p_matrix[i]))
		print("Result: ", p_matrix[i])
		print("-------------------------------------------------------------------------------------")
	print("____________________________________________________________________________________")

#-----------------------------------------------------------------------------#
		
def find_new_states(tree, num_states, states_q):
	"""
	Adds any new, previously unseen states in the current tree to be explored
	to all_states_explored.
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
				iteration of the program.
				num_states [int]: The total number of states present in the given
				tree.
	
	"""
	row = tree.get_all_states()
	
	new_states = []
	
	for state in row:
		if state not in states_q:
				new_states.append(state)

	return new_states

#-----------------------------------------------------------------------------#

#__________________________REDUCED MATRIX FUNCTIONS___________________________#

#-----------------------------------------------------------------------------#

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
			result = reduced_matrix_helper1(p_matrix, super_state, other_super_state)
			new_result = reduced_matrix_helper2((n, result))
			row.append(new_result)
		reduced_matrix.append(row)
	
	return reduced_matrix

#-----------------------------------------------------------------------------#

def reduced_matrix_helper1(p_matrix, super_state, other_super_state):
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

def reduced_matrix_helper2(tup):
	
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
	
	return new_tup

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

#__________________________MISCELLANEOUS FUNCTIONS____________________________#

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

#Executing the script.
start_time = time.time()
if __name__ == '__main__':
		p = mp.Process(target=compute, args = (mat,num_range))
		p.start()
		p.join()
		print("pMatrix_main_mp.py (multiprocessing with queues) took : ", time.time()-start_time, " seconds")
		print("____________________________________________________________________________________")
		
#_____________________________________________________________________________#







