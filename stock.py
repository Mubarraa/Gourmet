from item import *

class negative_quantity_for_stock (Exception):
    def __init__(self, quantity, item):
        self._item_name = item
        self._quantity = quantity
        
    def __str__(self):
        return "Negative quantity of {} inputted for {}".format(self._quantity, self._item_name)
        
class unavailable_item (Exception):
    def __init__(self, item, quantity_to_decrease, quantity):
        self._item_name = item
        self._quantity_to_decrease = quantity_to_decrease
        self._quantity = quantity
        
    def __str__(self):
        return "Cannot decrement {} by {}. Currently have {} in stock".format(self._item_name, self._quantity_to_decrease, self._quantity)
        
class Stock:
    def __init__(self):
        #a dictionary which stores item (as key) and quantities avaiable (as value)
        self._ingredients = {}
        #a list which stores the ingredients pointers only
        self._ingredients_list = []

    
    def add_new_ingredient (self, ingredient, quantity):
        self._ingredients[ingredient] = quantity
        self._ingredients_list.append (ingredient)

    #if the quantity_to_decrease is less than the quantity in stock, 
    #the stock status will not change and it will raise an exception
    def decrement_inventory(self, ingredient, quantity_to_decrease):
        if quantity_to_decrease < 0:
            raise negative_quantity_for_stock(quantity_to_decrease, ingredient)
        available = self.is_inStock(ingredient, quantity_to_decrease)
        if available == False:
            raise unavailable_item(ingredient, quantity_to_decrease, self._ingredients[ingredient])

        self._ingredients[ingredient] = self._ingredients[ingredient] - quantity_to_decrease
        

    # is this necessary if we have view inventory? should we jsut remove one
    def get_status(self):
        return self._ingredients

    def refill(self, ingredient, quantity): 
        if quantity < 0: 
           raise negative_quantity_for_stock(quantity, ingredient)
        self._ingredients[ingredient] += quantity

    #returns the quantity in stock of the given item... returns 0 if item is not in the stock
    def get_item_quantity(self, item):
        return self._ingredients[item]

    def view_inventory(self):
        return self._ingredients

    def get_ingredients (self):
        return self._ingredients_list

    def is_inStock(self, ingredient, quantity):
        
        if (self._ingredients[ingredient] >= quantity):
            return True
        else:
            return False

