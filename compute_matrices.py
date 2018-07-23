import generate_matrix

#Test case
mat = [[2,0],[0,0]] #10 states
num_range = [0,2]

#Generating the P-Matrix and the Reduced Matrix.
result = generate_matrix.compute(mat, num_range)
p_matrix = result[0]
r_matrix = result[1]

##################################################################

def compute_probability_matrix(p_matrix):
	
	#Computes the P-Matrix.
	
	prob_matrix = []
	for result in p_matrix:
		p = 0
		for prob in result:
			for i in range(len(prob)):
				if prob[i]!=0:
					p = p + (1/prob[i])
		prob_matrix.append(p)

	return prob_matrix

##################################################################

def compute_reduced_matrix(r_matrix):
	
	#Computes the reduced_matrix.
	
	result = []
	
	#Compressing sum.
	for element in r_matrix:
		n = element[0]
		prob = element[1]
		sum = 0
		for l in prob:
			for i in range(len(l)):
				if l[i]!=0:
					sum+=(1/l[i])	
		result.append((n,sum))
	
	reduced_matrix = []
	
	#Compressing further.
	for element in result:
		reduced_matrix.append(element[1]/element[0])
		
	return reduced_matrix

##################################################################

def printing(l):

	pass
















##################################################################
#Computing the P-Matrix.
probability_matrix = compute_probability_matrix(p_matrix)
print("P-Matrix: ", probability_matrix)
#Computing the reduced matrix.
reduced_matrix = compute_reduced_matrix(r_matrix)
print("Reduced Matrix: ", reduced_matrix)


		