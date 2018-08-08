"""
DOCUMENTATION:

This script computes the bound on the mixing time for a Probability Matrix.

Functions in the program -
	-> calculate_bound()
	-> convert_matrix()
	-> convert_to_pari()
	-> printing_bound()
	-> printing_matrix()
	-> printing_summary()
	-> execute_script()
	
Two scripts - generate_matrix and pMatrix_main_mp - are imported to generate the
P-Matrix and the reduced P-Matrix. (generate_matrix is sequentially computed,
while pMatrix_main_mp is optimized using multiprocessing. Use either one.)

Output of both scripts is in the format - (P-Matrix, Reduced Matrix)
	-> Format of P-Matrix -
			-> 3D list with inner most elements: [numerator, denominator]
			-> The element is simplified this way - numerator//denominator
	-> Format of reduced P-Matrix
			-> 2D list with inner most elements that are tuples in the form:
				(n, numerator, denominator)
			-> The element is simplified this way - (numerator//denominator)//n

calculate_bound() originally written by Kimia Tajik in Pari/GP.
Script written and implemented by Rhea Dutta in Python.

07/26/2018
"""
#______________________________________________________________________________________________#

#Scripts that generate the P-Matrix and the reduced P-Matrix. Use either one.
import generate_matrix as M #Sequentially computed.
#import pMatrix_main_mp as M #Uses multiprocessing.

#Importing Pari to perform computations to guarantee greatest possible accuracy.
import cypari2 as CP
pari = CP.Pari() #Pari object.

import math

#______________________________________________________________________________________________#

def calculate_bound(matrix, is_p_matrix, super_states = None):

	"""
	
	RETURNS: The bound on mixing time for the given matrix. 

	PARAMETERS: matrix: The matrix for which the bound on the mixing time must be calculated.
						(The input is the output of the generate_matrix / pMatrix_main_mp script)
				is_p_matrix [bool]: True if given matrix is a P-Matrix, False otherwise.
				super_states [3D list]: List of super states (each super state is a list of 
										sub states.)
	"""
	
	if is_p_matrix:
	  	P = convert_matrix(matrix, True)
	else:
	  	P = convert_matrix(matrix, False)
		l = [] #List of number of substates in every super state.
		for sp in super_states:
			l.append(len(sp))

	epsilon = pari('80')

	Size = pari.matsize(P)
	N = pari(Size[1])

	if is_p_matrix:
		D = pari(1/N)*pari.matid(N)
	else:
		s = pari(sum(l))
		new_l = []
		for n in l:
			n_ = pari(n)
			new_l.append(n_/s)
		x = convert_to_pari([new_l])
		D = pari.matid(N)
		for i in range(len(x)):
			D[i][i]= x[i]
	
	T = pari.mattranspose(P)
	X = pari.matinverseimage(D,T)
	B = pari(X*D)
	M = pari(P*B)

	[L,H] = pari.mateigen(M,1,100)

	sle = pari(L[N-2])

	print("sle: ", sle)
	
	bound = -2 * (math.log(2)/math.log(sle)) * (epsilon + math.log(N-1)/math.log(2))
	
	bound = math.ceil(bound)
	
	return bound
#______________________________________________________________________________________________#

def convert_matrix(matrix, is_p_matrix):

	"""
	RETURNS: The Pari.t_MAT form of the P-Matrix.

	PARAMETERS: matrix [3D list]: The matrix for which the bound on mixing time must be found.
									(Basically, it is the output of the aforementioned scripts.)
				is_p_matrix [bool]: True if given matrix is a P-Matrix, False otherwise.

	EXAMPLE: input = [[[1,2], [3,4]], [[5,6],[7,8]]]
			output = [1/2,3/4;5/6,7/8] wherein the output is a t_MAT and each element is a t_FRAC.

	"""

	#Conversion for P-Matrix.
	if is_p_matrix:
		new_matrix = []
		for row in matrix:
			new_row = []
			for prob in row:
				if prob[0]!=0:
					num = pari(prob[0])
					den = pari(prob[1])
					new_prob = num/den
					new_row.append(new_prob)
				else:
					new_row.append(pari('0'))
			new_matrix.append(new_row)

		result = convert_to_pari(new_matrix)
		return result

	#Conversion for reduced P-Matrix. 
	else:
		new_matrix = []
		for row in matrix:
			new_row = []
			for prob in row:
				if prob[1]!=0:
					n = pari(prob[0])
					num = pari(prob[1])
					den = pari(prob[2])
					new_prob = num/(den*n)
					new_row.append(new_prob)
				else:
					new_row.append(pari('0'))
			new_matrix.append(new_row)

		result = convert_to_pari(new_matrix)
		return result
#______________________________________________________________________________________________#

def convert_to_pari(matrix):

	"""
	RETURNS: The Pari.t_MAT form of the P-Matrix.

	PARAMETERS: matrix [2D list]: The matrix for which the bound on mixing time must be found.

	EXAMPLE: input = [[1/2, 3/4], [5/6, 7/8]] wherein each element is a t_FRAC.
			output = [1/2,3/4;5/6,7/8] wherein the output is a t_MAT. 

	"""

	new_matrix = ''

	for i in range(len(matrix)):
		new_row = ''

		for j in range(len(matrix[i])):
			
			if j==len(matrix[i])-1:
				last = ''
			else:
				last = ','
			new_row = new_row + str(matrix[i][j]) + last
		
		if i==len(matrix)-1:
			final = ''
		else:
			final = ';'
		new_matrix = new_matrix + new_row + final
	
	r = '['+ new_matrix + ']'
	result = pari(r)
	
	return result
#______________________________________________________________________________________________#

def printing_bound(n, is_p_matrix):

	"""

	Prints the given bound.
	
	PARAMETERS: n [int/float]: The given bound.
				is_p_matrix [bool]: True if n is a bound on the mixing time for a P-Matrix, False
								otherwise.  

	"""

	print("____________________________________________________________________________________")
	if is_p_matrix:
		print("Bound on mixing time for P-Matrix: ", n)
	else:
		print("Bound on mixing time for reduced P-Matrix: ", n)
	print("____________________________________________________________________________________")
#______________________________________________________________________________________________#

def printing_matrix(matrix, is_p_matrix):

	"""

	Prints the given matrix.
	
	PARAMETERS: matrix [Pari.t_MAT]: The given matrix.
				is_p_matrix [bool]: True if matrix is a P-Matrix, False
								otherwise.  

	"""	

	#For P-Matrix.
	if is_p_matrix:
		print("________________________________PROBABILITY MATRIX__________________________________ ")

	#For reduced P-Matrix.
	else:
		print("________________________________REDUCED MATRIX______________________________________")
	
	
	for i in range(len(matrix)):
		print(matrix[i])
		print("-------------------------------------------------------------------------------------")
	print("____________________________________________________________________________________")
#______________________________________________________________________________________________#

def printing_summary(p_matrix, r_matrix):

	"""

	Prints summary of data.

	"""

	print("________________________________SUMMARY OF DATA_____________________________________")
	print(" 1. P-Matrix")
	print("		-> Number of rows: ", len(p_matrix))

	s = 0
	for p in p_matrix[0]:
		s+=1
	
	print("		-> Number of columns: ", s)


	print(" 2. Reduced P-Matrix")
	print("		-> Number of super states: ", len(r_matrix))
	
	p = 0
	for row in r_matrix:
		p+=len(row)
		
	print("		-> Total number of sub states: ", p)
	print("____________________________________________________________________________________")
#______________________________________________________________________________________________#

def execute_script(input, must_print, only_bounds):

	"""
	
	Executes the script.
	Output in the form [P_MATRIX, R_MATRIX, P_BOUND, R_BOUND].

	PARAMETER: input [list]: [matrix, range]
				must_print [bool]: True if results must be printed, False otherwise.
				only_bounds [bool]: True if only bounds required and not matrices.
									False otherwise.

	"""

	#Comment out whichever one is not being used.
	#Do not change 'False' here.
	print("starting matrices")
	matrices = M.compute(input, False)
	super_states = M.return_super_states()
	print("finished matrices")

	#The required matrices. 
	P_MATRIX = matrices[0]
	R_MATRIX = matrices[1]

	print("finding bound")
	#Executing the script.
	P_BOUND = calculate_bound(P_MATRIX, True)
	R_BOUND = calculate_bound(R_MATRIX, False, super_states)
	print("found bound")
	
	#Printing results.
	if must_print:
		if only_bounds:
			printing_bound(P_BOUND, True)
			printing_bound(R_BOUND, False)
		else:
			#printing_matrix(P_MATRIX, True)
			#printing_matrix(R_MATRIX, False)
			printing_bound(P_BOUND, True)
			printing_bound(R_BOUND, False)
			printing_summary(P_MATRIX, R_MATRIX)

	#Returning results.
	return [P_MATRIX, R_MATRIX, P_BOUND, R_BOUND]
#______________________________________________________________________________________________#

#input = [[[2,0],[0,0]], [0,2]]
#Executing the script
#execute_script(input, True, True)