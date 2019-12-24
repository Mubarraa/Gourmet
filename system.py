from item import *
from stock import *
from order import *


#exception: when item is not instock
class invalid_order (Exception):
    def __init__(self, errors_list):
        self._list = errors_list

    def __str__(self):
        s= "order contains items which are not in stock: "
        for i in self._list:
            s += i.__str__()
        return s

#exception: when order is empty
class empty_order (Exception):
    def __str__(self):
        return "can not checkout empty order"

class InvalidID (Exception):
    def __init__(self, order_ID):
        self._order_ID = order_ID

    def __str__(self):
        return "Order ID " + str(self._order_ID) + " does not exist"

class System:
    def __init__(self):
        self._orderLog = OrderLog()
        self._stock = Stock()

    #adding ingredient to the stock
    def add_ingredient (self, ingredient, quantity):
        self._stock.add_new_ingredient (ingredient, quantity)

    def refill_ingredient (self, ingredient, quantity):
        self._stock.refill (ingredient, quantity)

    def decrement_ingredient (self, ingredient, quantity):
        self._stock.decrement_inventory (ingredient, quantity)

    def get_stock_status (self):
        return self._stock.get_status()

    def search_item (self, name):
        for i in self._stock.get_ingredients ():
            if i.get_name().lower() == name.lower():
                return i
        return None

    #returns ALL items in stock (ingredients, drinks and sides)
    def get_ingredients (self):
        return self._stock.get_ingredients ()

    def get_buns (self):
        all_ingredients = self._stock.get_ingredients ()
        buns = []
        for i in all_ingredients:
            if isinstance(i, Ingredient) and i.get_ingredient_type() == ingredient_type.bun:
                buns.append(i)

        return buns

    def get_patties (self):
        all_ingredients = self._stock.get_ingredients ()
        patties = []
        for i in all_ingredients:
            if isinstance(i, Ingredient) and i.get_ingredient_type() == ingredient_type.patty:
                patties.append(i)
        return patties

    #returns ingredients which are not patties not buns... for example, lettuce, tomato, cheese
    def get_other_ingredients (self):
        all_ingredients = self._stock.get_ingredients ()
        others = []
        for i in all_ingredients:
            if isinstance(i, Ingredient) and i.get_ingredient_type() == ingredient_type.other:
                others.append(i)
        return others

    #returns all drinks
    def get_drinks(self):
        all_ingredients = self._stock.get_ingredients ()
        drinks = []
        for i in all_ingredients:
            if isinstance(i, Drink):
                drinks.append(i)
        return drinks

    def get_sides(self):
        all_ingredients = self._stock.get_ingredients ()
        sides = []
        for i in all_ingredients:
            if isinstance(i, Side):
                sides.append(i)
        return sides

    def get_sundaes(self):
        all_ingredients = self._stock.get_ingredients ()
        sundaes = []
        for i in all_ingredients:
            if isinstance(i, Sundae):
                sundaes.append(i)
        return sundaes


    #takes a list of items objects and returns list of names
    def get_items_names (self, items):
        names = []
        for i in items:
            names.append(i.get_name())
        return names

    #takes a list of items and returns a dictionary of their prices
    def get_items_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price()
        return prices

    def get_small_side_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price(size.small)
        return prices

    def get_medium_side_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price(size.medium)
        return prices

    def get_large_side_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price(size.large)
        return prices

    def get_small_sundae_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price(size.small)
        return prices

    def get_medium_sundae_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price(size.medium)
        return prices

    def get_large_sundae_prices (self, items):
        prices = {}
        for i in items:
            prices[i.get_name()] = i.get_price(size.large)
        return prices

    #takes a list of items and returns a dictionary of their quantities
    def get_items_quantities (self, items):
        quantities = {}
        stock = self._stock.get_status()
        for i in items:
            quantities[i.get_name()] = stock[i]
        return quantities

    def get_order (self, order_ID):
        for i in self._orderLog.get_current_orders():
            if i.get_ID() == order_ID:
                return i
        for i in self._orderLog.get_served_orders():
            if i.get_ID() == order_ID:
                return i
        return None

    #returns true if order is surved (is in the served list) false otherwise
    def is_ready (self, order_ID):
        for i in self._orderLog.get_current_orders():
            if i.get_ID() == order_ID:
                return False
        for i in self._orderLog.get_served_orders():
            if i.get_ID() == order_ID:
                return True
        raise InvalidID(order_ID)

    def get_current_orders (self):
        return self._orderLog.get_current_orders ()

    def get_served_orders (self):
        return self._orderLog.get_served_orders()

    def get_next_order (self):
        return self._orderLog.get_next_order()

    def serve_order (self, order):
        self._orderLog.serve_order(order)

    #if one or more igredients in the order are not in stock
    #returns an array of all the ingredients unavailable and the quananty remaining
    #otherwise, returns empty list
    def is_valid_order(self, order):
        unavailable_items = []
        items = order.get_all_items() #this returns a list
        quantities = order.get_quantities () #this returns a dictionary of {item: quantity}
        for item in items:
            if (self._stock.is_inStock(item, quantities[item]) == False):
                unavailable_items.append(item)
        return unavailable_items


    def checkout_order (self, order):
        if (len(order.get_all_items()) == 0):
            raise empty_order ()

        unavailable_items = self.is_valid_order(order)
        if (len(unavailable_items) == 0):
            self._orderLog.checkout_order(order)
            #decrementing the order's ingredients from the stock:
            items = order.get_all_items()
            quantities = order.get_quantities()
            for item in items:
                self._stock.decrement_inventory(item, quantities[item])
        else:
            raise invalid_order(unavailable_items)

    def cancel_order (self, order):
        self._orderLog.cancel_order(order)

    #for the frontend
    def load_data(self):
        #buns
        self.add_ingredient(Ingredient("Sesame seed bun", 0, 2,ingredient_type.bun), 10)
        self.add_ingredient(Ingredient("Kaiser roll", 0, 2,ingredient_type.bun), 10)
        self.add_ingredient(Ingredient("Potato roll", 0, 2,ingredient_type.bun), 10)

        #patties
        self.add_ingredient(Ingredient("Beef patty", 0, 2,ingredient_type.patty), 10)
        self.add_ingredient(Ingredient("Chickpea patty", 0, 2,ingredient_type.patty), 10)
        self.add_ingredient(Ingredient("Chicken patty", 0, 2,ingredient_type.patty), 10)

        #other ingredients
        self.add_ingredient(Ingredient("Tomato", 1, 10, ingredient_type.other), 10)
        self.add_ingredient(Ingredient("Lettuce", 1, 10, ingredient_type.other), 10)
        self.add_ingredient(Ingredient("Cheese", 1.5, 10, ingredient_type.other), 10)
        self.add_ingredient(Ingredient("Pickles", 2, 10, ingredient_type.other), 10)
        self.add_ingredient(Ingredient("Onion", 2, 10, ingredient_type.other), 10)

        #drinks
        self.add_ingredient(Drink("Bottled sprite", 3, 600), 1)
        self.add_ingredient(Drink("Bottled coke", 5, 600), 3)
        self.add_ingredient(Drink("Canned coke", 3, 375), 3)
        self.add_ingredient(Drink("Canned sprite", 2, 375), 4)
        self.add_ingredient(Drink("Bottled water", 2.50, 150), 8)

        #sides
        self.add_ingredient(Side("Fries", 2, 3, 4, 75, 125, 200), 10000)
        self.add_ingredient(Side ("Nuggets", 2, 4, 6, 3, 6, 12), 500)

        #sundaes

        self.add_ingredient(Sundae("Chocolate Sundae", 3, 5, 6, 100, 150, 200), 1000)
        self.add_ingredient(Sundae ("Strawberry Sundae", 3, 5, 6, 100, 150, 200), 1000)

