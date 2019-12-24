from abc import ABC
from enum import Enum
class Item(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def set_name(self, name):
        self._name = name
    def set_price(self, price):
        self._price = price

    def __str__(self):
        return "{}".format(self._name)

#creating an Enum.. this will be very helpful when building the frontend
class ingredient_type(Enum):
    patty = 1
    bun = 2
    other = 3

class Ingredient (Item):
    #max_allowed is the maximum quantity of the ingredient that a customer add per meal
    #if no max_allowed is given it will be setted to 10
    #ingredient_type is either 'patty', 'bun' or 'other' if no type is given it will be'other' by defualt
    def __init__(self, name, price, max_allowed = 10, ingredient_type = ingredient_type.other):
        super().__init__(name, price)
        self._max_allowed = max_allowed
        self._ingredient_type = ingredient_type

    def get_max_allowed (self):
        return self._max_allowed

    #returns: patty, bun or other
    def get_ingredient_type (self):
        return self._ingredient_type

#creating an Enum
class size(Enum):
    small = 0, 'small'
    medium = 1, 'medium'
    large = 2, 'large'

class Side (Item):
    #p1 : small price. p2 : medium price p3 : large price
    def __init__(self, name, p1=2, p2=3, p3=4, small_weight =75, medium_weight=125, large_weight=200):
        super().__init__(name, p1)
        self._size = size
        self._small_weight = small_weight
        self._medium_weight = medium_weight
        self._large_weight = large_weight
        self._small_price = p1
        self._medium_price = p2
        self._large_price = p3


    def get_weight (self, size):
        if size == size.small:
            return self._small_weight
        if size == size.medium:
            return self._medium_weight
        if size == size.large:
            return self._large_weight

    def get_price (self, size):
        if size == size.small:
            return self._small_price
        if size == size.medium:
            return self._medium_price
        if size == size.large:
            return self._large_price

    def side_str(self, size):
        return super().get_name() + " " + str(size) + "  $" + str(self.get_price(size))

class Drink(Item):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self._size = size

    def get_size(self):
        return self._size

    def get_price (self):
        return self._price

class Sundae(Item):

    #p1 : small price. p2 : medium price p3 : large price
    def __init__(self, name, p1=2, p2=3, p3=4, small_weight =100, medium_weight=150, large_weight=200):
        super().__init__(name, p1)
        self._size = size
        self._small_price = p1
        self._medium_price = p2
        self._large_price = p3
        self._small_weight = small_weight
        self._medium_weight = medium_weight
        self._large_weight = large_weight

    def get_weight (self, size):
        if size == size.small:
            return self._small_weight
        if size == size.medium:
            return self._medium_weight
        if size == size.large:
            return self._large_weight

    def get_price (self, size):
        if size == size.small:
            return self._small_price
        if size == size.medium:
            return self._medium_price
        if size == size.large:
            return self._large_price

    def sundae_str(self, size):
        return super().get_name() + " " + str(size) + "  $" + str(self.get_price(size))

