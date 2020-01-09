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
# takes float number to convert it into human readable time
def from_float_to_time(float_time):
    time = float(float_time)
    hour = np.floor(time)
    minutes = np.floor((time - hour) * 60)
    if minutes < 10:
        return f"{int(hour)}h0{int(minutes)}"

    return f"{int(hour)}h{int(minutes)}"

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

# Takes branchs array to calculate distance matrix
def distance_matrix(branchs_array):
    if not branchs_array:
        raise Exception('Missing 1 argument : branchs array')
    N = len(branchs_array)
    if not len(branchs_array):
        raise Exception('Empty array')
    # initialize matrix with zero
    matrix = np.zeros((N, N))
    # if branch i and branch j are adjacent matrix takes the distance between them
    # otherwise it takes infinity
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
    matrix = np.zeros((N, N))
    # if branch i and branch j are adjacent matrix takes the sum of vehicles to pick up between them
    # otherwise it takes infinity
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

# select the branch with maximum gain
def select_max_profit(final_objectif_matrix_res, current_branch, selected_branchs, not_today):
    # current branch row in objective matrix
    current_branch_neighbors_profit = final_objectif_matrix_res[current_branch][:]
    # not selected takes elements not in selected list
    not_selected = [x for x in range(len(current_branch_neighbors_profit)) if x not in selected_branchs and x not in not_today]

    # if all branchs are selected return none
    if not len(not_selected):
        return
    # initialize maximum to the first branch index not selected
    maximum =  not_selected[0]
    # if we end up with a single element not selected and we can't reach from the current branch
    # return to the logistic park
    if (current_branch_neighbors_profit[maximum] in [np.nan, inf, -1 * inf] and len(not_selected) == 1):
        return 0
    # select the maximum gain from the not selected reachable neighbors
    for j in not_selected:
        is_greater = current_branch_neighbors_profit[j] > current_branch_neighbors_profit[maximum]
        is_not_selected = j not in selected_branchs
        value_is_not_inf_or_nan = current_branch_neighbors_profit[j] not in [np.nan, inf, -1 * inf]

        if is_greater and is_not_selected and value_is_not_inf_or_nan:
            maximum = j
    return maximum

# this method handel the best paths selection
def find_optimized_path(branchs, truck, starting_time = 7, closing_time = 17):
    # the origin is passed as the first element in branchs list
    origin = branchs[0]
    if not origin.getIsLogisticPark():
        raise Exception("First element in the branchs list should be the logistic park")
    # clock
    time = starting_time
    selected_branchs = [] # Selected branchs as parts of the path
    not_selected = list(range(len(branchs)))
    # vehicles impossible to deliver today
    not_today = []
    # path time table
    time_table = [starting_time]
    # We suppose here that distance is equivalent to the path time between branchs
    distance_matrix_res = distance_matrix(branchs)
    final_problem_objective_matrix_res = final_problem_objectif_matrix(branchs)

    # while we still have elements not selected and closing time not reached yet
    while len(not_selected) > 0 and time < closing_time:
        #  start from the origin of index 0
        current_branch_index = 0
        # add the origin as selected
        selected_branchs.append(current_branch_index)
        # if we have at least two selected branchs increment time and add to the time table
        if (len(selected_branchs) > 1):
            time += distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
            time_table.append(time)
        # exploration depth
        deep = 0
        # if we are in the logistic parc we free the truck's load
        truck.freeLoad()
        cars_number = 0
        # exploration depth mustn't exceed 3 branchs
        while deep < 3 and not truck.is_full():
            # select the most profitable branch index
            current_branch_index = select_max_profit(final_problem_objective_matrix_res, current_branch_index, selected_branchs, not_today)
            # if none we break
            if not current_branch_index:
                break
            current_branch = branchs[current_branch_index]
            # whether the truck is full
            is_full = truck.is_full()
            # Reachable if we can reach and back to the logistic park before closing time
            can_i_reach_and_back_before_closing_time = distance_matrix_res[selected_branchs[-1]][current_branch_index] + time + distance_matrix_res[0][current_branch_index] < closing_time

            if not is_full and can_i_reach_and_back_before_closing_time:
                # as the truck can load and the branch is reachabke we select it
                selected_branchs.append(current_branch_index)
                if current_branch.getCarsToPickupNumber() > truck.getFreeSpace():
                    # As the branch dispose more than the truck capacity
                    # fill the free space in the truck
                    cars_number += truck.getFreeSpace()
                    # decrement the branch's cars number
                    current_branch.setCarsToPickupNumber(current_branch.getCarsToPickupNumber() - truck.getFreeSpace())
                    # update objective matrix to update the second objective matrix
                    final_problem_objective_matrix_res = final_problem_objectif_matrix(branchs)
                    # keep the branch available to selection
                    not_selected.append(current_branch_index)
                else:
                    # else get all branch's cars
                    cars_number += current_branch.getCarsToPickupNumber()
                # load the truck
                truck.setLoadedCars(cars_number)
                # increment time by adding the path cost
                time += distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
                time_table.append(time)
            elif not can_i_reach_and_back_before_closing_time:
                # unreachable append to not today
                not_today.append(current_branch_index)
            # update not selected branchs list
            not_selected = [x for x in range(len(branchs)) if x not in selected_branchs and x not in not_today]
            # increment depth
            deep += 1
        # incrment the delivered cars number to the origin
        origin.setCarsDeliveredNumber(cars_number + origin.getCarsDeliveredNumber())

    #  if we ends with some thing other then the origin in the selection we add it and we calculate the path cost
    if selected_branchs[-1] != 0:
        selected_branchs.append(0)
        time += distance_matrix_res[selected_branchs[-2]][selected_branchs[-1]]
    # Showing results
    print("==============================")
    print(f"we started from logistic park in : {branchs[0].name} at {from_float_to_time(time_table[0])}")
    print("==============================")
    print(f"{branchs[0].name} --- delivered cars : 0 -- time {from_float_to_time(time_table[0])}")

    for index in range(1, len(selected_branchs)):
        if selected_branchs[index] == 0:
            print(f"{branchs[selected_branchs[index]].name} --- delivered cars : {branchs[selected_branchs[index]].getCarsDeliveredNumber()} -- time {from_float_to_time(time_table[index])}")
        else:
            print(f"{branchs[selected_branchs[index]].name} --- taken cars : {branchs[selected_branchs[index]].getCarsToPickupNumber()} -- time {from_float_to_time(time_table[index])}")


    print("==============================")
    print(f"{branchs[selected_branchs[0]].getCarsDeliveredNumber()} delivered cars")

