from models.Branch import Branch
# from models.Driver import Driver
# from models.Truck import Truck
# from math import inf
from models.Truck import Truck
from utils.utils import final_problem_objectif_matrix, distance_matrix, find_optimized_path, select_max_profit

truck = Truck("NYC10D9")

o = Branch(name="1er arr", longitude=48.864031, latitude=2.330943)
o.setAsLogisticPark()
a = Branch(name="2eme arr", longitude=48.867705, latitude=2.343533)
a.setCarsToPickupNumber(3)
b = Branch(name="3eme arr", longitude=48.863499, latitude=2.358317)
b.setCarsToPickupNumber(3)
c = Branch(name="4eme arr", longitude=48.853431, latitude=2.357847)
c.setCarsToPickupNumber(2)
d = Branch(name="5eme arr", longitude=48.843409, latitude=2.349478)
d.setCarsToPickupNumber(6)
e = Branch(name="6eme arr", longitude=48.847520, latitude=2.331174)
e.setCarsToPickupNumber(1)

branchs = [o, a, b, c, d, e]
# print(distance_matrix(branchs_array= branchs))
import numpy as np
# vehicle_number_matrix_np = np.array(vehicle_number_matrix(branchs_array= branchs))
distance_matrix_np = np.array(distance_matrix(branchs_array= branchs))

# print(len(vehicle_number_matrix_np))
# print(np.array(distance_matrix(branchs_array= branchs)))

fobj = final_problem_objectif_matrix(branchs_array=branchs)
fobj[np.isnan(fobj)] = -1 * np.inf
# print(fobj)
find_optimized_path(branchs, truck)
# current_branch = 2
# selected_branchs = [0, 4, 3, 0, 1, 2]
# time = 7
# max = select_max_profit(fobj, current_branch, selected_branchs, branchs, time)