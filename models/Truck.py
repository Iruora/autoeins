class Truck:

    def __init__(self, registration_number, driver, capacity = 8):
        self.__registration_number = registration_number
        self.__capacity = capacity
        self.__loaded_cars = 0
        self.__driver = driver



    def getRegistrationNumber(self):
        return self.__registration_number


    def getCapacity(self):
        return self.__capacity


    def getLoadedCars(self):
        return self.__loaded_cars


    def getDriver(self):
        return self.__driver


    def setRegistrationNumber(self, registration_number):
        self.__registration_number = registration_number

    def setCapacity(self, capacity):
        self.__capacity = capacity

    def setLoadedCars(self, loaded_cars):
        self.__loaded_cars = loaded_cars


    def setDriver(self, driver):
        self.__driver = driver
