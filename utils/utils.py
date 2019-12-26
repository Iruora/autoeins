from numpy import inf
import numpy as np
import geopy.distance as geopy_distance
from models.Branch import Branch

# Adjecency matrix for the 6 first "arrondissement" in Paris
# M[i, j] takes 1 if the (i + 1) "arrondissement" is adjacent to (j + 1) "arrondissement"
# it takes -1 otherwise
adjacency_matrix = [
    [-1, 1, 1, 1, 1, 1],
    [1, -1, 1, -1, -1, -1],
    [1, 1, -1, 1, -1, -1],
    [1, -1, 1, -1, 1, 1],
    [1, -1, -1, 1, -1, 1],
    [1, -1, -1, 1, 1, -1]
]
# takes two branchs to calculate the distance between them using vincenty formula
def distance_between_branchs(from_branch, destination_branch):
    # verify whether we have got Branch instances as args
    if not (isinstance(from_branch, Branch) and isinstance(destination_branch, Branch)):
        raise Exception('Argument(s) not of type Branch')
    from_branch_position = from_branch.getPosition()
    destination_branch_position = destination_branch.getPosition()
    # verify whether we do have not none 2 coordinates for each branch
    if not ((
                        (len(destination_branch_position) + len(from_branch_position) == 4 and (
                        destination_branch_position[0])) and (
                            destination_branch_position[1])) and (from_branch_position[0])) or not (from_branch_position[1]):
        raise Exception('Missing postion on destination')

    # distance calculated using vincenty in Km see : https://en.wikipedia.org/wiki/Vincenty%27s_formulae
    return geopy_distance.vincenty(
        from_branch.getPosition(),
        destination_branch.getPosition()
    ).km


def distance_matrix(branchs_array):
    if not branchs_array:
        raise Exception('Missing 1 argument : branchs array')
    N = len(branchs_array)
    if not len(branchs_array):
        raise Exception('Empty array')
    matrix = [[0 for i in range(N)] for j in range(N)]

    for i in range(N - 1):
        for j in range(i + 1, N):
            if adjacency_matrix[i][j] == 1:
                matrix[i][j] = distance_between_branchs(branchs_array[i], branchs_array[j])
                matrix[j][i] = matrix[i][j]
            else:
                matrix[i][j] = inf
                matrix[j][i] = matrix[i][j]


    return matrix

# second objectif matrix
# we illustrate here the cost of path as the sum of the cars number between the two edges
def vehicle_number_matrix(branchs_array):
    if not branchs_array:
        raise Exception('Missing 1 argument : branchs array')
    N = len(branchs_array)
    if not len(branchs_array):
        raise Exception('Empty array')
    matrix = [[0 for i in range(N)] for j in range(N)]

    for i in range(N - 1):
        for j in range(i + 1, N):
            if adjacency_matrix[i][j] == 1:
                matrix[i][j] = branchs_array[i].getCarsToPickupNumber() + branchs_array[j].getCarsToPickupNumber()
                matrix[j][i] = matrix[i][j]
            else:
                matrix[i][j] = inf
                matrix[j][i] = matrix[i][j]


    return matrix

# F = w0 f0 + w1 f1
# where F : the final objectif
# where wi : the weight of su-objectif i
# This process is called scalarization which used to transform multi-objectif optimization problem to a single objectif
# one
# in our case we are facing two objectifs :
#   1st objectif : maximize number of taken cars
#   2nd objectif : minimize path time
#  to bring the above two objectifs into a single one we have applied scalarization
#  w've also transformed the problem into a maximization
# NB : Min() = - Max()
def final_objectif_matrix(first_objectif, second_objectif, first_objectif_weight=1, second_objectif_weight=1):
    # the two matrix needs to have the same size
    if len(first_objectif) != len(second_objectif):
        raise Exception('Matrix not of the same size')
    # Scalarization
    first_objectif = float(first_objectif_weight) * np.array(first_objectif)
    second_objectif = -1 * float(second_objectif_weight) * np.array(second_objectif)
    return np.add(
        first_objectif,
        second_objectif
    )

# def final_problem_objectif_matrix(branchs_array):
#