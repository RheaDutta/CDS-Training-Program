#Produces P-Matrix using Multiprocessing - EXPERIMENTAL. 

import pMatrix
import time
import multiprocessing as mp

mat = [[2,3],[0,0]] #56 states
num_range = [0,5]

# mega_list_ = []
# all_states_ = []
#----------------------------------------------------------------------------------#	

def first_iteration(mat, num_range, mega_list, all_states):
	# global mega_list_
	# global all_states_
	
	s = pMatrix.matrix_to_vector(mat) #The vector version of matrix mat. 
	t = pMatrix.create_tree(mat, num_range) #Tree for the first iteration.
	r = pMatrix.main(mat, num_range) #Results for the first iteration.
	
	for st in t.get_all_states(): #Adding all states to be explored
		all_states.append(st)     #in first iteration to all_states global list. 
	
	mega_list.append((s,r)) #Adding the tuple to the global list mega_list.
	
#----------------------------------------------------------------------------------#

def next_iterations(num_range):
	
	# global mega_list_
	# global all_states_
	# 
	# manager = mp.Manager()
	# mega_list = manager.list() 
	# all_states = manager.list() 
	
	# for m in mega_list_:
	#  	mega_list.append(m)
	# for a in all_states_:
	#  	all_states.append(a)
	
	i = 1
	p_list = []
	proc_list = []
	
	while i<len(all_states):
		
		while len(proc_list)<8:
			for proc in proc_list:
				if proc.is_alive() == False:
					proc_list.remove(proc)
			vec = all_states[i]
			p = mp.Process(target = next_iterations_helper, args = (i,vec, num_range, mega_list,all_states))
			p_list.append(p)
			proc_list.append(p)
			p.start()
			i+=1	
			
		if len(proc_list)==8:
			while len(proc_list) == 8:
				for proc in proc_list:
					if proc.is_alive() == False:
						proc_list.remove(proc)
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

def manage_proc(proc_list, count):
	pass
	
	
#----------------------------------------------------------------------------------#

if __name__ == '__main__':
	#freeze_support()
	
	#Starting Time.
	st = time.time()
	
	#Creating manager lists. 
	manager = mp.Manager()
	mega_list = manager.list() 
	all_states = manager.list()
	
	#First Iteration.
	first_iteration(mat, num_range, mega_list, all_states)
	
	#Next Iterations.
	next_iterations(num_range)
	
	print(time.time() - st)
		
#----------------------------------------------------------------------------------#



















