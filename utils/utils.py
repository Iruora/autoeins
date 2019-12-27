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

def final_problem_objectif_matrix(branchs_array):
    # second objecif : maximize vehicles' number
    first_objectif_matrix = vehicle_number_matrix(branchs_array=branchs_array)
    # first objecif : minimize paths time
    second_objectif_matrix = distance_matrix(branchs_array=branchs_array)

    matrix = final_objectif_matrix(
        first_objectif = first_objectif_matrix,
        second_objectif = second_objectif_matrix
    )
    matrix[np.isnan(matrix)] = -1 * np.inf
    return matrix


def select_max_profit(final_objectif_matrix_res, current_branch, selected_branchs, branchs, time):
    print(f"current inside function is : {current_branch}")
    current_branch_neighbors_profit = final_objectif_matrix_res[current_branch][:]
    print(current_branch_neighbors_profit)
    not_selected = [x for x in range(len(current_branch_neighbors_profit)) if x not in selected_branchs]
    print(f"not_selected : {not_selected}")
    if not len(not_selected):
        return
    maximum =  not_selected[0]
    print(f"maximum before for loop : {current_branch_neighbors_profit[maximum]} of index {maximum}")
    if (current_branch_neighbors_profit[maximum] in [np.nan, inf, -1 * inf] and len(not_selected) == 1):
        return 0
    for j in not_selected:
        is_greater = current_branch_neighbors_profit[j] > current_branch_neighbors_profit[maximum]
        is_not_selected = j not in selected_branchs
        value_is_not_inf_or_nan = current_branch_neighbors_profit[j] not in [np.nan, inf, -1 * inf]
        print(f"{j} is greater : {is_greater} /  is_not_selected : {is_not_selected} /   value_is_not_inf_or_nan : {value_is_not_inf_or_nan}")
        if is_greater and is_not_selected and value_is_not_inf_or_nan:
            maximum = j
            # print(f"nearest : {branchs[maximum]}")
    return maximum


def find_optimized_path(branchs, truck):
    time = 7
    selected_branchs = []
    not_selected = range(5)

    distance_matrix_res = distance_matrix(branchs)
    final_problem_objectif_matrix_res = final_problem_objectif_matrix(branchs)

    debugger_ = 0
    while len(not_selected) > 0 and time < 17:
        current_branch = 0
        selected_branchs.append(current_branch);
        if (len(selected_branchs) > 1):
            time += distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
        deep = 0
        cars_number = 0

        debugger_ += 1

        while deep < 3:
            current_branch = select_max_profit(final_problem_objectif_matrix_res, current_branch, selected_branchs, branchs, time)

            if not current_branch:
                break
            # if distance_matrix_res[selected_branchs[-1]][current_branch] + time + distance_matrix_res[0][current_branch] < 17:
            selected_branchs.append(current_branch)
            cars_number += branchs[current_branch].getCarsToPickupNumber()
            branchs[0].setCarsDeliveredNumber(cars_number)

            if cars_number > 8:
                print(f"delete : {selected_branchs.pop()}")
            else:
                time += distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
            if time > 17:
                time -= distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
                branchs[selected_branchs[-1]].setIsSelected(False)
                selected_branchs.pop()
                # break
                # not_today.append(selected_branchs[-1])

            not_selected = [x for x in range(len(branchs)) if x not in selected_branchs]
            # print(f"cars_number : {cars_number}")
            deep += 1
            # print(f"selected_branchs : {selected_branchs}")
            # print("-----------------------------------------")
    # selected_branchs.append(current_branch)
    print(f"time just before returning to center : {time}")
    if selected_branchs[-1] != 0:
        selected_branchs.append(0)
        print(f"len(not_selected) = {len(not_selected)}")
        time += distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
    print(f"time just after returning to center : {time}")
    # selected_branchs = [x for x in selected_branchs if x not in not_today]
    print(f"selected_branchs {selected_branchs}")
    # for index in selected_branchs:
    #     print(f"{branchs[index].name} --- status : {branchs[index].getIsSelected()}")
    print(f"time {time}")
    # print(f"not_selected ! {not_selected}")