from item import *
from stock import *
import pickle

#exception: when quantity of ingredient is more that the allowed amount per meal
class invalid_quantity (Exception):
    def __init__(self, item, max_allowed):
        self._item_name = item
        self._max_allowed = max_allowed

    def __str__(self):
        return "exceeded max allowed quantity: max for ({}) is {}".format(self._item_name, self._max_allowed)

#exception: when quantity given is negative
class negative_quantity (Exception):

    def __str__(self):
        return "negative quantities are not allowed"

class main_type(Enum):
    single = 'single'
    double = 'double'
    wrap = 'wrap'


class mainDish:
    def __init__(self,t = main_type.single):
        self._type = t # single, double or wrap
        self._ingredient_list = []
        self._quantities = {} #stores item as key and quantity as value

    #if no quantity is given, the quantity will be 1
    #if the same ingredients is added twice with different quantities
    #only the last quantity will be considered
    #also if quantity is greater that the allowed one for that ingredient ->raise exception
    def add_ingredient(self, ingredient, quantity = 1):
        if quantity < 0 :
            raise negative_quantity()
        if self._type == main_type.single:
            if ingredient.get_ingredient_type() == ingredient_type.patty and quantity > 1:
                raise invalid_quantity(ingredient, 1)
        if self._type == main_type.double:
            if ingredient.get_ingredient_type() == ingredient_type.patty and quantity > 2:
                raise invalid_quantity(ingredient, 2)
        if self._type == main_type.wrap:
            if ingredient.get_ingredient_type() == ingredient_type.patty and quantity > 1:
                raise invalid_quantity(ingredient, 1)

        if quantity > ingredient.get_max_allowed():
            #print ("raise exception here")
            raise invalid_quantity(ingredient, ingredient.get_max_allowed())
        if ingredient not in self._ingredient_list:
            self._ingredient_list.append(ingredient)
        self._quantities[ingredient] = quantity

    def get_type(self):
        return self._type

    def get_mainList(self):
        return self._ingredient_list

    def set_type(self,type):
        self._type = type

    def total_cost(self):
        total = 0
        if self._type == main_type.double:

            total += 7
        elif self._type == main_type.single:

            total += 5

        elif self._type == main_type.wrap:

            total += 5

        for i in self._ingredient_list:
            total = total + i.get_price() * self._quantities[i]

        return total

    def get_quantities (self):
        return self._quantities

    def __str__(self):
        s = "type is {}\n ingredients are: \n".format(str(self._type))
        for i in self._ingredient_list:
            s += " "+ str(self._quantities[i]) + " {}\n".format(i)
        return s

class Order:
    #class variable
    num_orders = 0

    #this should not take main as parameter because we could have an order without a main
    #just sides or drinks
    def __init__(self):
        #getting the order count from the file
        pickle_in = open ("orders_count.pickle", "rb")
        Order.num_orders = pickle.load (pickle_in)
        pickle_in.close()

        self._ID = Order.num_orders
        self._all_items = []
        self._main = mainDish()
        self._sides = []
        self._sides_sizes= []
        self._drinks = []
        self._drink_sizes = []
        self._sundaes = []
        self._sundae_sizes = []
        self._quantities = {}
        Order.num_orders += 1

        #pickle the new count
        pickle_out= open("orders_count.pickle", "wb")
        pickle.dump(Order.num_orders, pickle_out)
        pickle_out.close()


    def add_main (self, main):
        self._main = main
        q = main.get_quantities()
        for i in main.get_mainList():
            self._all_items.append(i)
            self._quantities[i] = q[i]

    #takes a side from the user and append it to the list
    def add_side (self, side, size = size.small, quantity = 1,):
        if quantity < 0:
            raise negative_quantity(side)
        self._side_quantity = quantity
        self._sides.append(side)
        self._all_items.append(side)
        #for a side quantity is quantity* the weight
        self._quantities[side] = quantity * side.get_weight(size)
        self._sides_sizes.append (size)

    #takes a drink and append it to the drink list
    def add_drink (self, drink, quantity = 1):
        self._drink_quantity = quantity
        if quantity < 0:
            raise negative_quantity(drink)
        self._drinks.append(drink)
        self._all_items.append(drink)
        self._quantities [drink] = quantity
        #self._drink_sizes.append (size)

    def add_sundae(self, sundae, size = size.small, quantity = 1):
        if quantity < 0:
            raise negative_quantity(sundae)
        self._sundae_quantity = quantity
        self._sundaes.append(sundae)
        self._all_items.append(sundae)
        self._quantities [sundae] = quantity * sundae.get_weight(size)
        self._sundae_sizes.append (size)


    def get_ID(self):
        return self._ID


    def get_type(self):
        return self._main.get_type()

    def get_main(self):

        return self._main

    def get_sides(self):
        return self._sides

    def get_drinks(self):
        return self._drinks

    def get_sundaes(self):
        return self._sundaes

    def set_type(self, main):
        self._main = main.get_type()

    #returns all the items included in the order
    #including the ingredients in the main..
    #this will be helpful when trying to decrement the order items from the stock
    def get_all_items(self):
        return self._all_items

    def total_cost(self):
        total = 0

        if self._main != None:
            total = self._main.total_cost()

        for i in range(0, len(self._sides)) :
            total += self._sides[i].get_price(self._sides_sizes[i]) * self._side_quantity

        for j in self._drinks:
            total += j.get_price() * self._drink_quantity

        for m in range(0, len(self._sundaes)):
            total += self._sundaes[m].get_price(self._sundae_sizes[m]) * self._sundae_quantity

        return total

    def get_quantities (self):
        return self._quantities

    def __str__(self):
        s = ""
        s += self._main.__str__() + "\n"

        s += ". sides and drinks: "
        i = 0
        s += "\n"
        for d in self._drinks:
            s += str(self._quantities[d]) + d.__str__() + " "

        i = 0
        for d in self._sides:
            s += d.side_str(self._sides_sizes[i]) + " " + str(self._quantities[d])
            i += 1

        i = 0
        s += "\n"
        for m in self._sundaes:
            s += m.sundae_str(self._sundae_sizes[i]) + " " + str(self._quantities[m])
            i += 1

        return s


class OrderLog:
    def __init__(self):
        self._current_orders = []
        self._past_orders = []

    #remove the given order from the current_orders list
    def cancel_order (self, order):
        self._current_orders.remove(order)

    def get_served_orders (self):
        return self._past_orders

    def get_current_orders (self):
        return self._current_orders

    #returns the order that should be served next(first one in the current list)
    def get_next_order (self):
        return self._current_orders[0]

    def serve_order(self, order):
        self._past_orders.append(order);
        self._current_orders.remove(order);

    def checkout_order(self, order):
        #only when checked out the order will be added to the list
        self._current_orders.append(order);

