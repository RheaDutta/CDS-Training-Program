import generate_matrix

##################################################################

def compute_probability_matrix(p_matrix):
	
	#Computes the P-Matrix.
	
	prob_matrix = []
	for result in p_matrix:
		row = []
		for prob in result:
			p = 0
			for i in range(len(prob)):
				if prob[i]!=0:
					p = p + (1/prob[i])
			row.append(p)
		prob_matrix.append(row)

	return prob_matrix

##################################################################

def compute_reduced_matrix(r_matrix):
	
	#Computes the reduced_matrix.
	
	result = []
	
	#Compressing sum.
	for list in r_matrix:
		new_list = []
		for tup in list:
			new_tup = compute_reduced_matrix_helper(tup)
			new_list.append(new_tup)
		result.append(new_list)
	
	reduced_matrix = []
	
	#Compressing further.
	for list in result:
		row = []
		for tup in list:
			row.append(tup[1]/tup[0])
		reduced_matrix.append(row)
		
	return reduced_matrix

##################################################################

def compute_reduced_matrix_helper(tup):

	n = tup[0]
	p = tup[1]
	sum = 0
	for p_list in p:
		for m in p_list:
			if m!=0:
				sum+=(1/m)
	
	return (n,sum)

##################################################################

def printing(l):

	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	for list in l:
		print(list)
		print("----------------------------------------")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	
##################################################################

def do():
	
	#Test case
	#mat = [[2,0],[0,0]] #10 states
	#num_range = [0,2]
	
	mat = [[2,3],[0,0]] #56 states
	num_range = [0,5]
	
	#Generating the P-Matrix and the Reduced Matrix.
	result = generate_matrix.compute(mat, num_range)
	p_matrix = result[0]
	r_matrix = result[1]
	
	#Computing the P-Matrix.
	probability_matrix = compute_probability_matrix(p_matrix)
	
	#Computing the reduced matrix.
	reduced_matrix = compute_reduced_matrix(r_matrix)
	
	#Printing both matrices.
	#print("PROBABILITY MATRIX: ")
	#printing(probability_matrix)
	print("REDUCED PROBABILITY MATRIX: ")
	printing(reduced_matrix)
	
##################################################################

#Executing the script.
do()
		