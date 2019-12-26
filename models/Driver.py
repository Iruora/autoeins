# Driver:
#   attributes:
#       - fullname
#       - registration_number: unique identifier
class Driver:

    def __init__(self, fullname, registration_number):
        self.__fullname = str(fullname)
        self.__registration_number = str(registration_number)


    def getRegistrationNumber(self):
        return self.__registration_number


    def getFullname(self):
        return self.__fullname


    def setRegistrationNumber(self, registration_number):
        self.__registration_number = str(registration_number)


    def setFullname(self, fullname):
        self.__fullname = str(fullname)
