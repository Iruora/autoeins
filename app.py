from models.Driver import Driver
from models.Truck import Truck

d = Driver("ccccc", "dddddd")
c = Truck("eeeee", d)

print(c.getDriver().getFullname())