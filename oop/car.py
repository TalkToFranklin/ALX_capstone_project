""" class Car: # mercedes, toyota
    
    def __init__ (self, car_name, car_price, car_color):
        self.car_name = car_name
        self.car_price = car_price
        self.car_color = car_color """

class Car: # mercedes, toyota
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.price = 0
        self.mileage = 0
        self.features = []