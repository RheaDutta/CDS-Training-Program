#Find P-Matrix using Multiprocessing and Queues. Very slow as compared to sequential version. WORKS. 




###############################################################################

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
	
#---------------Test Cases---------------#


#mat = [[2,3],[0,0]] #56 states
#num_range = [0,5]

#mat = [[0,5],[0,0]] #84 states
#num_range = [0,6]

#mat = [[15,3],[2,0]]
# num_range = [0,10]

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
	print("first_iteration() took: ", time.time()-t1, "seconds.")
	
	t2 = time.time()
	#Next iterations
	iterations(num_range)
	print("iterations() took: ", time.time()-t2, "seconds.") 
	
	t3 = time.time()
	#Reordering results. 
	all_results = reorder()
	print("reorder() took: ", time.time()-t3, "seconds.") 
	
	#Printing results
	#printing_results(all_results)
	
	print("Total number of states: ", len(all_results))
	
	return all_results
	
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
	#First iteration has been computed in first_iteration function. Thus, iterations
	#begin at the second element. 
	i=1
	
	#List of processes.
	process_list = []
	
	while i<len(all_states_explored):
		#print("process number: ", i)
		
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
	
	t = time.time()
	#Making sure that all processes are done before moving on.
	for p in process_list:  
		p.join()
	#print("time taken to join: ", time.time()-t)
	
###############################################################################

def add_next_iterations(num_range,vector,q,states_q):
	
	#print("working")
	
	#Converting the vector in all_states_explored to a matrix. 
	matrix = make_matrix(vector)
	
	#Tree for currrent iteration.
	tree = pMatrix.create_tree(matrix, num_range)	
	
	#Calculating the number of states in current iteration.
	num_states = calculate_num_states(tree)
	
	#Finding results for each iteration.
	result = pMatrix.main(matrix, num_range)
	
	#Adding all the above information to a tuple.
	tup = (vector, result, num_states, tree)
	
	#Finding any new, previously unseen state and adding to new_states.
	new_states = find_new_states(tree, num_states, states_q)
	
	#Adding the results to the Queue q. 
	q.put([tup, new_states])
	#print("done")
	
###############################################################################

def reorder():
	"""
	RETURNS: A reordered form of matrix all_results such that the order of rows is
	the same as the order of columns.
	
	"""
	#This is the required P-Matrix.
	all_results = []*len(mega_list)
	
	process_list = []
	
	for i in range(0, len(mega_list)):
		new_result = [0]*len(mega_list) #The reordered result for each iteration.
		q = mp.Queue()
		p = mp.Process(target = reorder_helper, args = (mega_list[i],i,new_result, mega_list,q))
		process_list.append(p)
		p.start()
		all_results.insert(i, q.get())
		
	#Making sure that all processes are done before moving on.
	for p in process_list:  
		p.join()
	
	return all_results

###############################################################################

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
	states = return_all_states(tree,num_states)
	
	for i in range(len(mega_list)):
		for state in states:
			for existing_state in mega_list[i]:
				if state == existing_state:
					pos = states.index(state)
					new_result[i]=result[pos]
	
	q.put(new_result)
	
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

#------------------------- HELPER FUNCTIONS ----------------------------------#

###############################################################################

def make_matrix(vector):
	"""
	Makes matrix out of the current vector being processed in all_states_explored.
	
	PARAMETERS: vector [list]: The 1D list that must be converted to a 2D list.  
	
	"""
	matrix = []
	for j in range(0, len(vector),2):
		matrix.append([vector[j],vector[j+1]])
			
	return matrix

###############################################################################
		
def find_new_states(tree, num_states, states_q):
	"""
	Adds any new, previously unseen states in the current tree to be explored
	to all_states_explored.
	
	PARAMETERS: tree [pMatrix.Tree object]: The tree object generated in the present
				iteration of the program.
				num_states [int]: The total number of states present in the given
				tree.
	
	"""
	row = return_all_states(tree, num_states)
	
	new_states = []
	
	for state in row:
		if state not in states_q:
				new_states.append(state)

	return new_states
	
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




###############################################################################

#Executing the script.
start_time = time.time()
if __name__ == '__main__':
		p = mp.Process(target=compute, args = (mat,num_range))
		p.start()
		p.join()
		print("pMatrix_main.py (with multiprocessing) took : ", time.time()-start_time, " seconds")

###############################################################################






