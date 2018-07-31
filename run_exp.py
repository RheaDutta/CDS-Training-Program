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
import sys
from datetime import datetime
# import bound
# import generate_matrix as M
import pMatrix_main_mp as M
from file_to_matrix import parse_matrix

def generate_pmatrix(inputs):
    """
    Generates P-Matrix and reduced P-Matrix.
    Output in format - [p_matrix, reduced p_matrix].
    """

    #Generates matrices. matrices = [p_matrix, reduced p_matrix]
    matrices = M.compute(inputs)
    return matrices

def generate_bounds(inputs):
    """
    Generates the bounds on mixing time for the P-matrix and the reduced P-Matrix.
    Output in format - [P_BOUND, R_BOUND].
    """

    # bounds = bound.execute_script(inputs, True)[2:]
    bounds = 0
    return bounds


def usage():
    print('Usage: ',sys.argv[0]," filename")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit(0)

    file = sys.argv[1]
    print("file:", file)

    start = datetime.now()
    for mat, num_range in parse_matrix(file):
        generate_pmatrix([mat, num_range])
        generate_bounds([mat, num_range])

    print("Total sec:", (datetime.now() - start).total_seconds())
