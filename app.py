from models.Branch import Branch
from models.Driver import Driver
from models.Truck import Truck

d = Driver("ccccc", "dddddd")
c = Truck("eeeee")
o = Branch(name="1er arr", longitude=48.864031, latitude=2.330943)
a = Branch(name="2er arr", longitude=48.867705, latitude=2.343533)


e = (1,1)
f = (2, 1)

print(o.getDistanceTo(a))