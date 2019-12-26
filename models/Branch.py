import geopy.distance as distance

# Branch :
#   attributes :
#       - __name = branch name
#       - __cars_number : cars' number contained
#       - __longitude: branch Geographical longitude
#       - __latitude: branch Geographical latitude
#       - __is_logistic_park:
#           takes True if the branch is the logistic park (starting point) where cars needs to be delivered
#           takes False if the branch is a point where cars needs to be picked up
class Branch:


    def __init__(self, name, longitude, latitude):
        self.__name = str(name)
        self.__cars_number = 1
        self.__longitude = float(longitude)
        self.__latitude = float(latitude)
        self.__is_logistic_park = False

    def setCarsNumber(self, cars_number):
        if cars_number < 0 or cars_number > 10:
            raise Exception('cars number in a branch should be in [0,10]')
        self.__cars_number = cars_number


    def setIsLogisticPark(self, value):
        self.__is_logistic_park = bool(value)


    def setAsLogisticPark(self):
        self.setIsLogisticPark(True)


    def getPosition(self):
        return (self.__longitude, self.__latitude)


    def getDistanceTo(self, destination_branch):
        # verify whether we have got a Branch instance
        if not isinstance(destination_branch, Branch):
            raise Exception('Argument not of type Branch')
        destination_branch_position = destination_branch.getPosition()
        # verify whether we do have not none 2 coordinates for destination branch
        if len(destination_branch_position) != 2 or not (destination_branch_position[0]) or not (destination_branch_position[1]):
            raise Exception('Missing postion on destination')
        # distance calculated using vincenty see in Km : https://en.wikipedia.org/wiki/Vincenty%27s_formulae
        return distance.vincenty(
            self.getPosition(),
            destination_branch_position
        ).km