"""

DOCUMENTATION:

This script has multiple functions - 
    -> It can generate the probability matrix for the given input.
    -> It can generate the reduced probability matrix for the given input.
        (This is essentially a condensed version of the probability matrix)
    -> It can find the bounds on the mixing time for each of the aforementioned matrices.

THe program has the following functions - 
    -> run_experiments()
    -> only_matrices()
    -> matrices_and_bounds()
    -> only_bounds()
    -> find_input()
    -> store_output()

Instructions for running the script -

    1. Right under this documentation, a few scripts have been imported. 
        -> Choose one of generate_matrix and pMatrix_main_mp.
        -> They have the same output.
        -> generate_matrix runs sequentially.
        -> pMatrix_main_mp uses multiprocessing.

    2. Edit run_experiments() to choose which experiment to run.

    3. Scroll to the bottom of the script. If you would like your results to be printed to the screen,
        change must_print to True. Otherwise, change it to False. In either case, the results 
        will be stored.

    4. Change the input in find_input().


Written by Rhea Dutta

07/26/2018

"""
#___________________________________________________________________________________________

#To find matrices + bounds.
import bound 

#To find only matrices. Use either one.
import generate_matrix as M 
#import pMatrix_main_mp as M

#___________________________________________________________________________________________

def run_experiments(must_print):

    """
    
    Runs experiments. Use whichever one is required.

    PARAMETERS: must_print[bool]: True if result should be printed, False otherwise.

    """

    #Only generate matrices.
    only_matrices(must_print)
    
    #Both matrices and bounds.
    #matrices_and_bounds(must_print)

    #Only bounds
    #only_bounds(must_print)
#___________________________________________________________________________________________

def only_matrices(must_print):

    """
    Generates P-Matrix and reduced P-Matrix.
    Output in format - [p_matrix, reduced p_matrix].

    PARAMETERS: must_print[bool]: True if result should be printed, False otherwise.

    """

    #Extracting input.
    input = find_input()

    #Generates matrices. matrices = [p_matrix, reduced p_matrix]
    matrices = M.compute(input, must_print)
    
    #Storing output.
    store_output(matrices)
#___________________________________________________________________________________________

def matrices_and_bounds(must_print):

    """
    Generates P-Matrix, reduced P-Matrix, and bounds on mixing time for both.
    Output in format - [P_MATRIX, R_MATRIX, P_BOUND, R_BOUND]

    PARAMETERS: must_print[bool]: True if result should be printed, False otherwise.

    """

    #Extracting input.
    input = find_input()

    #Running the experiment.
    result = bound.execute_script(input, must_print, False)
    
    #Storing output.
    store_output(result) #result = [P_MATRIX, R_MATRIX, P_BOUND, R_BOUND]
#___________________________________________________________________________________________

def only_bounds(must_print):

    """
    Generates the bounds on mixing time for the P-matrix and the reduced P-Matrix.
    Output in format - [P_BOUND, R_BOUND].

    PARAMETERS: must_print[bool]: True if result should be printed, False otherwise.

    """

    #Extracting input.
    input = find_input()

    #Running the experiment.
    result = bound.execute_script(input, must_print, True)[2:]
    
    #Storing output.
    store_output(result) #result = [P_BOUND, R_BOUND]
#___________________________________________________________________________________________

def find_input():

    """
    Extract input from some file.



    """

    mat = [[2,0],[0,0]] #7 states
    num_range = [0,1]

    #mat = [[2,3],[0,0]] #56 states
    #num_range = [0,5]

    #mat = [[5,0],[0,0]] #41 states
    #num_range = [0,3]

    #mat = [[3,0],[0,0]] #17 states
    #num_range = [0,2]

    #mat = [[2,0],[0,0]] #10 states
    #num_range = [0,2]

    #mat = [[2,1],[0,0]] #20 states
    #num_range = [0,3]

    #mat = [[7,7],[0,0]]
    #num_range = [0,7]
    
    #mat = [[2,3],[1,0]] #44 states
    #num_range = [0,3]

    #mat = [[0,6],[0,0]] #84 states
    #num_range = [0,6]

    #mat = [[3,0],[0,0]] #17 states
    #num_range = [0,2]

    input = [mat, num_range]

    return input
#___________________________________________________________________________________________

def store_output(output):

    """
    Store output in some file.



    """

    pass
#___________________________________________________________________________________________

#If results should be printed, must_print = True. False otherwise.
must_print = True

#Running the experiment. Open the function to pick which one to run. 
run_experiments(must_print)
