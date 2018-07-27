"""

DOCUMENTATION:

This script has multiple functions - 
    -> It generates the probability matrix for the given input.
    -> It generates the reduced probability matrix for the given input.
        (This is essentially a condensed version of the probability matrix)
    -> It finds the bounds on the mixing time for each of the aforementioned matrices.

THe program has the following functions - 
    ->
    ->

Written by Rhea Dutta

07/26/2018

"""
#___________________________________________________________________________________________

import bound
#___________________________________________________________________________________________

def run_experiments():

    """
    
    Runs all experiments and stores the output.

    """

    #Extracting input.
    input = find_input()

    #Running the experiment.
    result = bound.execute_script(input)

    #Results of the experiment.
    P_MATRIX = result[0]
    P_BOUND = result[1]
    R_MATRIX = result[2]
    R_BOUND = result[3]

    #Printing results.
    bound.printing_matrix(P_MATRIX, True)
    bound.printing_matrix(R_MATRIX, False)
    bound.printing_bound(P_BOUND, True)
    bound.printing_bound(R_BOUND, False)

    #Storing results.
    store_output(result)
#___________________________________________________________________________________________

def find_input():

    """
    Extract input from some file.



    """

    m = [[2,0],[0,0]]
    n = [0,2]
#___________________________________________________________________________________________

def store_output(output):

    """
    Store output in some file.



    """

    pass
#___________________________________________________________________________________________

#Running the experiment.
run_experiments()
