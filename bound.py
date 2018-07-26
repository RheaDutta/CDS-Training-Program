"""
DOCUMENTATION:

This script computes the bound on the mixing time for a Probability Matrix.

Functions in the program -
	->
	->
	
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

bound() originally written by Kimia Tajik in Pari/GP.
Script written and implemented by Rhea Dutta.

07/26/2018
"""
#______________________________________________________________________________________________#

#Scripts that generate the P-Matrix and the reduced P-Matrix. Use either one.
import generate_matrix as GM #Sequentially computed.
#import pMatrix_main_mp as PM #Uses multiprocessing.

#Importing Pari to perform computations to guarantee greatest possible accuracy.
import cypari

#Input
mat = [[2,0],[0,0]]
num_range = [0,2]

#Comment out whichever one is not being used.
matrices = GM.compute(mat, num_range)
#matrices = PM.compute(mat, num_range)

#The required matrices. 
P_MATRIX = matrices[0]
R_MATRIX = matrices[1]

#______________________________________________________________________________________________#

def calculate_bound(p_matrix):
	
	"""
	
	RETURNS: The bound on mixing time for the given P-Matrix. 
	
	PARAMETERS: p_matrix [3D list]: The Probability Matrix for which the bound on mixing time must be
				found.
	
	"""
	
	P=[1/6,1/18,1/18,1/18,1/6,1/18,1/18,1/6,1/18,1/6;1/6,1/18,1/18,1/18,1/6,1/18,1/18,1/6,1/18,1/6;0,1/6,1/6,1/6,0,1/6,1/6,0,1/6,0;0,1/6,1/6,1/6,0,1/6,1/6,0,1/6,0; 1/6,1/18,1/18,1/18,1/6,1/18,1/18,1/6,1/18,1/6;0,1/6,1/6,1/6,0,1/6,1/6,0,1/6,0;0,1/6,1/6,1/6,0,1/6,1/6,0,1/6,0;1/6,1/18,1/18,1/18,1/6,1/18,1/18,1/6,1/18,1/6;1/6,1/18,1/18,1/18,1/6,1/18,1/18,1/6,1/18,1/6; 1/6,1/18,1/18,1/18,1/6,1/18,1/18,1/6,1/18,1/6];
	
	[L,H] = mateigen(P,1);
	D = L[2] * matid(10);
	
	N = NumStates(P);
	
	T = mattranspose(P);
	
	res = D^(-1);
	res2 = res*D;
	res3 = D*res;
	
	Pbar = res * T * D;
	M = P * Pbar;
	
	bound = -2 * (log(2)/1) * (80 + log(9)/log(2));
	
	print(bound)
#______________________________________________________________________________________________#





