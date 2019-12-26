from models.Branch import Branch
# from models.Driver import Driver
# from models.Truck import Truck
# from math import inf
from utils.utils import final_problem_objectif_matrix

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
# distance_matrix_np = np.array(distance_matrix(branchs_array= branchs))

# print(len(vehicle_number_matrix_np))
# print(len(distance_matrix_np))

fobj = final_problem_objectif_matrix(branchs_array=branchs)

print(fobj)