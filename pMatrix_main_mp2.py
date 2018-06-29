#Produces P-Matrix using Multiprocessing - DOES NOT WORK. 


import pMatrix
import multiprocessing as mp
import time 

mega_list_ = []
all_states_ = []

#mat = [[2,0],[0,0]]
#num_range = [0,2]

#mat = [[2,3],[0,0]] #56 states
#num_range = [0,5]

#mat = [[0,9],[0,0]] # states
#num_range = [0,9]

#mat = [[3,1],[0,0]] #35 states
#num_range = [0,4]


####################################################################################

#----------------------------------------------------------------------------------#
def compute(mat, num_range):
	
	#First iteration.
	first_iteration(mat, num_range)
	
	#Next iterations
	next_iterations(num_range)
	
#----------------------------------------------------------------------------------#
	
def first_iteration(mat, num_range):
	
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
	
	global mega_list_
	global all_states_
	
	manager = mp.Manager()
	mega_list = manager.list() #Format: [(state,result)]
	all_states = manager.list() #Contains all states to be explored.
	
	for m in mega_list_:
	 	mega_list.append(m)
	for a in all_states_:
	 	all_states.append(a)
	
	i = 1
	p_list = []
	count = 10
	current_proc = []
	
	while i<len(all_states):
		print("i = ", i, "len(mega_list): ", len(mega_list), "len(all_states): ", len(all_states))
		if count>0:
			print("count>0")
			vec = all_states[i]
			p = mp.Process(target = next_iterations_helper, args = (i,vec, num_range, mega_list,all_states))
			count-=1
			p_list.append(p)
			current_proc.append(p)
			p.start()
			update = update_count(current_proc,count)
			if update is not None:
				print("updating")
				count = update[0]
				current_proc.remove(update[1])
			print("count = ", count)
			print("current_proc: ", current_proc)
			
		elif count == 0:
			print("count = 0 and no process is finished")
			joining(current_proc)
			current_proc = []
			count = 10
			print("count = ", count)
			print("current_proc: ", current_proc)
		i+=1

		# if i % 10 == 0:
		# 	time.sleep(0.5)
		
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
			print("found new state")
			all_states.append(st)
	
	#print("length of all_states: ", len(all_states))
			
#----------------------------------------------------------------------------------#

def joining(p_list):
	
	for p in p_list:
		p.join()
		  
#----------------------------------------------------------------------------------#

def update_count(proc_list,count):
	
	for p in proc_list:
		if p.is_alive() == False:
			print("		process is done")
			count+=1
			print("		process is done and count = ", count)
			return([count,p])
		else:
			pass
		
#----------------------------------------------------------------------------------#

if __name__ == '__main__':
	#freeze_support()
	st = time.time()
	p = mp.Process(target=compute, args = (mat,num_range))
	p.start()
	p.join()
	print(time.time() - st)
		
#----------------------------------------------------------------------------------#