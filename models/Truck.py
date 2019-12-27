# Truck:
#   attributes:
#       - __registration_number: Truck unique identifier
#       - __capacity: the maximum number of cars the truck can load
#       - __loaded_cars: current number of loaded cars
#       - __driver: the Truck driver
from models.Driver import Driver


class Truck:

    def __init__(self, registration_number, capacity = 8):
        self.__registration_number = str(registration_number)
        self.__capacity = int(capacity)
        self.__loaded_cars = 0
        self.__driver = None



    def getRegistrationNumber(self):
        return self.__registration_number


    def getCapacity(self):
        return self.__capacity


    def getLoadedCars(self):
        return self.__loaded_cars


    def getDriver(self):
        return self.__driver

    def isAffected(self):
        return self.getDriver() != None


    def getFreeSpace(self):
        return self.__capacity - self.__loaded_cars

    def freeLoad(self):
        self.setLoadedCars(0)

    def setRegistrationNumber(self, registration_number):
        self.__registration_number = str(registration_number)

    def setCapacity(self, capacity):
        self.__capacity = int(capacity)

    def setLoadedCars(self, loaded_cars):
        if loaded_cars > self.__capacity:
            raise ValueError('Cannot load more than the capacit, capacit = {}', self.__capacity)
        self.__loaded_cars = int(loaded_cars)


    def setDriver(self, driver):
        if not isinstance(driver, Driver):
            raise Exception('Argument not of type Driver')
        self.__driver = driver


    def is_full(self):
        return self.__capacity == self.__loaded_cars