#Produces P-Matrix using Multiprocessing - WORKS. 

"""

This program uses the script pMatrix.py to generate every row of the P-Matrix.
The final output is the P-Matrix for the given matrix and range of numbers.

Written by - Rhea Dutta. Date - 06/29/2018. 

"""

####################################################################################

#-------------------------------- MODULES ---- -----------------------------------#

import pMatrix #Generates each row of the P-Matrix.
import time #Used to assess program performance (efficiency).
import multiprocessing as mp #Used to increase efficiency.

#-------------------------------- GLOBAL LISTS -----------------------------------#

all_states_ = [] #List will contain all the states to be explored for the P-Matrix.

mega_list_ = [] #List of tuples. Each tuple is in the format (state, result).
				#state is a vector and result is its corresponding row in the P-Matrix.
				#Thus, each tuple contains 2 lists. 

#-------------------------------- TEST CASES ------------------------------------#

mat = [[2,3],[0,0]] #56 states
num_range = [0,5]

#mat = [[3,1],[0,0]] #35 states
#num_range = [0,4]

#mat = [[0,9],[0,0]] # states
#num_range = [0,9]

#mat = [[3,0],[1,0]] # states
#num_range = [0,10]

#mat = [[5,2],[2,1]]
#num_range = [0,10]

#mat = [[5,0],[0,2],[2,1]]
#num_range = [0,10]

####################################################################################
#----------------------------------------------------------------------------------#

def compute(mat, num_range):
	"""
	RETURNS: The final P-Matrix generated for the given matrix mat and the given
			range of numbers num_range. (Final result is a 3D list). 
	PARAMETERS: PARAMETERS: mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	
	#First Iteration
	first_iteration(mat, num_range)
	
	#Next iterations
	next_iterations(num_range)
	
#----------------------------------------------------------------------------------#	

def first_iteration(mat, num_range):
	"""
	Function finds the probability row for the given matrix mat and range of
	numbers of num_range. It essentially finds the first row in the P-Matrix.
	It is a list of the probabilities that the intial state would end up in any of
	the other states that are generated.
	
	The function finds the result and stores it in the global list mega_list_.
	It also finds all the states reachable from this state (the matrix mat)
	and stores them in the global list all_states_. 
	
	PARAMETERS: PARAMETERS: mat [multi-dimensional array]: The matrix whose p-matrix must be found.
				num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	global mega_list_
	global all_states_
	
	s = pMatrix.matrix_to_vector(mat) #The vector version of matrix mat. 
	t = pMatrix.create_tree(mat, num_range) #Tree for the first iteration.
	r = pMatrix.main(mat, num_range) #Results for the first iteration.
	
	for st in t.get_all_states(): #Adding all states to be explored
		all_states_.append(st)     #in first iteration to all_states global list. 
	
	mega_list_.append((s,r)) #Adding the tuple to the global list mega_list.
	
#----------------------------------------------------------------------------------#

def next_iterations(num_range):
	"""
	Function finds the probability rows for the rest of P-Matrix by traversing the
	multiprocessing.Manager.list all_states which contains the states reachable by the
	first state contained in the global list all_states_.
	
	The function creates a process for every finding every row in the P-Matrix.
	
	PARAMETERS: num_range [list]: The range of numbers that can be substituted in the
								matrix in the format [min,max].
								Eg: [0,255] for RGB.
	
	"""
	global mega_list_ 
	global all_states_
	
	manager = mp.Manager()
	mega_list = manager.list() #Manager lists so as to exchange information with each process. 
	all_states = manager.list() 
	
	for m in mega_list_: #Adding the information from the first iteration to the lists. 
	 	mega_list.append(m)
	for a in all_states_:
	 	all_states.append(a)
	
	#Iterations start at 1 and not 0 because row 0 has already been computed in
	#first_iteration() function. 
	i = 1
	
	#p_list contains all the processes started.
	p_list = []
	
	#proc_list contains the processes that are currently being processed.
	#Must have at most 10 processes at a time.
	proc_list = []
	
	while i<len(all_states):
		
		while len(proc_list)<10: #Only allows 10 processes to run at a time. 
			
			update = update_procs(proc_list, p_list, i, all_states, mega_list)
			proc_list = update[0]
			p_list = update[1]
			i = update[2]
			all_states = update[3]
			mega_list = update[4]
				
			
		if len(proc_list)==10:
			while len(proc_list) == 10:
				for proc in proc_list:
					if proc.is_alive() == False: #If any of the processes is over, the process is removed
						proc_list.remove(proc) #from proc_list.
		vec = all_states[i]
		p = mp.Process(target = next_iterations_helper, args = (i,vec, num_range, mega_list,all_states))
		p_list.append(p)
		proc_list.append(p)
		p.start()
		i+=1	
						
			
		# if i % 10 == 0:
		#  	time.sleep(0.5)
		
	joining(p_list)
	
	print("len(all states): ", len(all_states))
	print("len(mega_list): ", len(mega_list))
		
#----------------------------------------------------------------------------------#

def update_procs(proc_list, p_list, i, all_states, mega_list):
	
	for proc in proc_list:
		if proc.is_alive() == False: #If any of the processes is over, the process is removed
			proc_list.remove(proc) #from proc_list.
	vec = all_states[i]
	p = mp.Process(target = next_iterations_helper, args = (i,vec, num_range, mega_list,all_states))
	p_list.append(p)
	proc_list.append(p)
	p.start()
	i+=1
	
	return (proc_list, p_list, i, all_states, mega_list)
	
#----------------------------------------------------------------------------------#

def next_iterations_helper(i,vec, num_range, mega_list, all_states):
	
	#global mega_list
	#global all_states
	
	mat = pMatrix.make_matrix(vec) #The vector version of matrix mat. 
	r = pMatrix.main(mat, num_range) #Results for the current iteration.
	t = pMatrix.create_tree(mat, num_range) #Tree for the current iteration.
				
	mega_list.append((vec,r)) #Adding the tuple to the global list mega_list.
	
	for st in t.get_all_states(): #Finding new states and adding to
		if st not in all_states:  #all_states. 
			all_states.append(st)
	
	#print("length of all_states: ", len(all_states))
			
#----------------------------------------------------------------------------------#

def joining(p_list):
	
	for p in p_list:
		p.join()
	
#----------------------------------------------------------------------------------#

if __name__ == '__main__':
	#freeze_support()
	st = time.time()
	p = mp.Process(target=compute, args = (mat,num_range))
	p.start()
	p.join()
	print(time.time() - st)
		
#----------------------------------------------------------------------------------#