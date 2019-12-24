from item import *
from stock import *
from order import *
from system import *
import pytest


  
#########################################################################################
#----------------------------------------pytests----------------------------------------#
#########################################################################################

@pytest.fixture
def fixture():
    system = System()
    
    #buns
    system.add_ingredient(Ingredient("sesame seed bun", 3, 2,ingredient_type.bun), 10)
    system.add_ingredient(Ingredient("kaiser roll", 5, 2,ingredient_type.bun), 11)
    system.add_ingredient(Ingredient("potato roll", 5, 2,ingredient_type.bun), 13)

    #patties
    system.add_ingredient(Ingredient("beef patty", 3, 2,ingredient_type.patty), 70)
    system.add_ingredient(Ingredient("chickpea patty", 4.5, 2,ingredient_type.patty), 70)
    system.add_ingredient(Ingredient("chicken patty", 3, 2,ingredient_type.patty), 70)
    system.add_ingredient(Ingredient("veggie patty", 3, 2,ingredient_type.patty), 70)

    #other ingredients
    system.add_ingredient(Ingredient("tomato", 1, 10, ingredient_type.other), 10)
    system.add_ingredient(Ingredient("lettuce", 1, 10, ingredient_type.other), 10)
    system.add_ingredient(Ingredient("cheese", 1.5, 10, ingredient_type.other), 10)
    system.add_ingredient(Ingredient("pickles", 2, 10, ingredient_type.other), 10)
    system.add_ingredient(Ingredient("onion", 2, 10, ingredient_type.other), 10)
        
    #drinks
    
    system.add_ingredient(Drink("Bottled sprite", 3, 600), 1)
    system.add_ingredient(Drink("Bottled coke", 4, 600), 3)
    system.add_ingredient(Drink("Canned coke", 4, 375), 3)
    system.add_ingredient(Drink("Canned sprite", 3, 375), 4)
    system.add_ingredient(Drink("Bottled water", 3.75, 150), 8)

    #sides
    system.add_ingredient(Side("fries", 2, 3, 4, 75, 125, 200), 10000)
    system.add_ingredient(Side ("nuggets", 2, 4, 6, 3, 6, 12), 500)

    return system


def test_initial_state (fixture):
    served_list = fixture.get_served_orders ()
    current_list = fixture.get_current_orders ()
    assert len(served_list) == 0
    assert len(current_list) == 0

def test_search_item (fixture):
    item = fixture.search_item ("sesame seed bun")
    assert(item.get_name() == "sesame seed bun")
    assert (item.get_max_allowed() == 2)
    assert (item.get_price() == 3)
    assert (item.get_ingredient_type() == ingredient_type.bun)

def test_get_buns (fixture):
    buns = fixture.get_buns()
    assert (len(buns) == 3)
    for i in buns:
        assert (i.get_name() in ["sesame seed bun", "kaiser roll", "potato roll"])

def test_get_drinks (fixture):
    drinks = fixture.get_drinks()
    assert(len(drinks) == 5)
    for i in drinks:
        assert (i.get_name() in ["Bottled sprite", "Bottled coke", "Canned coke", "Canned sprite", "Bottled water"])
    
def test_get_ingredients (fixture):
    ingredients = fixture.get_other_ingredients()
    assert(len(ingredients) == 5)
    for i in ingredients:
        assert (i.get_name() in ["tomato", "lettuce", "cheese", "onion", "pickles"])
        
def test_get_sides(fixture):
    sides = fixture.get_sides()
    assert(len(sides) == 2)
    for i in sides:
        assert (i.get_name() in ["nuggets", "fries"])
       
#creates and returns valid main of type double 
def create_double_burger (fixture):
    main = mainDish(main_type.double)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("beef patty"), 2)
    main.add_ingredient(fixture.search_item ("lettuce"), 1)
 
    return main

def test_double_burger (fixture): 
    main = create_double_burger (fixture)

    assert(main.get_type() == main_type.double)

    ingredients = main.get_mainList()
    assert (ingredients[0].get_name() == "sesame seed bun")
    assert (ingredients[1].get_name() == "beef patty")
    assert (ingredients[2].get_name() == "lettuce")

    #check the quantities
    quantities = main.get_quantities ()
    assert (quantities[fixture.search_item("sesame seed bun")] == 2)
    assert (quantities[fixture.search_item("beef patty")] == 2)
    assert (quantities[fixture.search_item("lettuce")] == 1)

    
#creates and returns main of type single 
def create_single_burger (fixture):
    main = mainDish(main_type.single)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("beef patty"), 1)
    main.add_ingredient(fixture.search_item ("lettuce"), 1)
 
    return main

def test_single_burger (fixture):
    main = create_single_burger (fixture)

    assert(main.get_type() == main_type.single)

    ingredients = main.get_mainList()
    assert (ingredients[0].get_name() == "sesame seed bun")
    assert (ingredients[1].get_name() == "beef patty")
    assert (ingredients[2].get_name() == "lettuce")

    #check the quantities
    quantities = main.get_quantities ()
    assert (quantities[fixture.search_item("sesame seed bun")] == 2)
    assert (quantities[fixture.search_item("beef patty")] == 1)
    assert (quantities[fixture.search_item("lettuce")] == 1)


#creating a single with  2 patties
def test_invalid_single_burger (fixture):
    main = mainDish(main_type.single)
    message = ""
    try:
        main.add_ingredient(fixture.search_item ("beef patty"), 2)
    except Exception as e:
        message = e.__str__()

    assert (message == "exceeded max allowed quantity: max for (beef patty) is 1")
   
#creating double with 3 patties     
def test_invalid_double_burger (fixture):
    main = mainDish(main_type.double)
    message = ""
    try:
        main.add_ingredient(fixture.search_item ("beef patty"), 3)
    except Exception as e:
        message = e.__str__()

    assert (message == "exceeded max allowed quantity: max for (beef patty) is 2")
        
#order that contains quantity more than allowed
def test_max_allowed (fixture):
    main = mainDish(main_type.double)
    main.add_ingredient(fixture.search_item("beef patty"), 2)
   
    message = ""
    try:
        main.add_ingredient(fixture.search_item("Tomato"), 11)
    except Exception as e:
        message = e.__str__()

    assert(message == "exceeded max allowed quantity: max for (tomato) is 10")
    
#create a valid order with single burger and a side and a drink
def create_order (fixture):
    order = Order()
    main = create_single_burger(fixture)

    # adding things to order
    order.add_side(fixture.search_item("fries"), size.small)
    order.add_side(fixture.search_item("nuggets"), size.medium)
    order.add_main(main)
  

    return order 

def create_order2 (fixture):
    order = Order()
    main = create_single_burger(fixture)

    # adding things to order
    order.add_side(fixture.search_item("fries"), size.large)
    order.add_side(fixture.search_item("nuggets"), size.small)
    order.add_main(main)
  
    return order 

def test_create_order (fixture):
    order = create_order (fixture)
    #checking the items in order
    assert(order.get_sides()[0] == fixture.search_item("fries"))
    assert(order.get_sides()[1] == fixture.search_item("nuggets"))

    #checking the total price 
    #assert (order.total_cost() == 15)
    
def test_order_sides (fixture):
    order = create_order (fixture)
    #the weight should be 75 g since we've ordered small fries
    fries_weight = order.get_quantities()[fixture.search_item("fries")]
    assert (fries_weight == 75)
    nuggets_quantity = order.get_quantities()[fixture.search_item("nuggets")]
    assert (nuggets_quantity == 6)

    order2 = create_order2 (fixture)

    fries_weight2 = order2.get_quantities()[fixture.search_item("fries")]
    assert (fries_weight2 == 200)
    nuggets_quantity2 = order2.get_quantities()[fixture.search_item("nuggets")]
    assert (nuggets_quantity2 == 3)

def checkout_order (fixture):
    order = create_order(fixture)
    fixture.checkout_order(order)

    return order

def test_checkout_order(fixture):
    order = checkout_order(fixture)
    # next order is the same as the first order in list 
    assert(order == fixture.get_current_orders()[0])
    #number of current/served orders before order is served to customer
    assert(len(fixture.get_current_orders()) == 1)
    assert (fixture.get_next_order() == order)
    #assert(len(fixture.get_served_orders()) == 0)
    
def test_checkout_empty_order (fixture):
    message = ""
    order = Order()
    try :
        fixture.checkout_order(order)
    except Exception as e:
        message = e.__str__()

    #if message is empty it means that exception was not raised
    assert (message  == "can not checkout empty order")
 
def test_serve_order (fixture):
    order = checkout_order (fixture)
    #next order returns one order not a list
    assert(fixture.get_next_order() == order)

    assert (len(fixture.get_current_orders()) == 1)
    fixture.serve_order(order)
    assert(len(fixture.get_current_orders()) == 0)
    assert(len(fixture.get_served_orders()) == 1)


#checks out 4 orders and serve them
def test_serve_many_orders(fixture):
    orders = []
    for i in range(0, 4):
        orders.append(checkout_order (fixture))
    assert (len(fixture.get_current_orders()) == 4)

    #checking that each order has distinct id
    assert (orders[0].get_ID  != orders[1].get_ID)
    assert (orders[0].get_ID  != orders[2].get_ID)
    assert (orders[0].get_ID  != orders[3].get_ID)
    assert (orders[1].get_ID  != orders[2].get_ID)  
    assert (orders[1].get_ID  != orders[3].get_ID)
    assert (orders[3].get_ID  != orders[2].get_ID)
    
    for i in range (0, 3):
        fixture.serve_order(orders[i])

    i = fixture.get_next_order()
    fixture.serve_order(i)

    assert(len(fixture.get_current_orders()) == 0)
    assert(len(fixture.get_served_orders()) == 4)


#test order that contains items not in stock
def test_invalid_order (fixture):

    invalid_order = Order()
    invalid_order.add_drink(fixture.search_item("Bottled sprite"), 2)

    message = ""

    try:
        fixture.checkout_order (invalid_order)
    except Exception as e:
        message = e.__str__()

    assert (message == "order contains items which are not in stock: Bottled sprite")
        
    
def test_invalid_negative_quantity(fixture):
    invalid_order = Order()
    message = ""
    try:
        invalid_order.add_drink(fixture.search_item("Bottled coke"), -3)
    except Exception as e:
        message = e.__str__()

    assert (message == "negative quantities are not allowed for Bottled coke")

    invalid_order2 = Order()
    try:
        invalid_order2.add_side(fixture.search_item("fries"), size.small, -1)
    except Exception as e:
        message = e.__str__()

    assert (message == "negative quantities are not allowed for fries")

    invalid_order3 = Order()
    try:
        invalid_order3.add_side(fixture.search_item("nuggets"),size.small, -1.6)
    except Exception as e:
        message = e.__str__()

    assert (message == "negative quantities are not allowed for nuggets")

#test the inventory status after checking out order
def test_checkout_inventory (fixture):
    patty = fixture.search_item("beef patty")
    num_patties_instock = fixture.get_stock_status()[patty]

    bun = fixture.search_item("sesame seed bun")
    num_buns_instock = fixture.get_stock_status()[bun]

    lettuce = fixture.search_item("lettuce")
    num_lettuce_instock = fixture.get_stock_status()[lettuce]
    
    order = Order()
    main = create_double_burger(fixture)
    order.add_main (main)
    fixture.checkout_order(order)

    assert (fixture.get_stock_status()[patty] == num_patties_instock - 2)
    assert (fixture.get_stock_status()[bun] == num_buns_instock - 2)    
    assert (fixture.get_stock_status()[lettuce] == num_lettuce_instock - 1) 

def test_refill_inventory(fixture):
    
    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    
    fixture.refill_ingredient(ingredient_list[0], 5)
    fixture.refill_ingredient(ingredient_list[1], 10)
    fixture.refill_ingredient(ingredient_list[2], 10)


    assert(ingredients_dic[ingredient_list[0]] == 15)
    assert(ingredients_dic[ingredient_list[1]] == 21)
    assert(ingredients_dic[ingredient_list[2]] == 23)
    
def test_refill_inventory_with_invalid_value(fixture):
    
    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    
    message = ""

    try:
        fixture.refill_ingredient(ingredient_list[0], -1)
    except Exception as e:
        message = e.__str__()
        
    assert (message == "Negative quantity of -1 inputted for sesame seed bun")

    try:
        fixture.refill_ingredient(ingredient_list[1], -5)
    except Exception as e:
        message = e.__str__()
       
    assert (message == "Negative quantity of -5 inputted for kaiser roll")

    try:
        fixture.refill_ingredient(ingredient_list[2], -10)
    except Exception as e:
        message = e.__str__()

    assert (message == "Negative quantity of -10 inputted for potato roll")

    try:
        fixture.refill_ingredient(ingredient_list[0], -100)
    except Exception as e:
        message = e.__str__()

    assert (message == "Negative quantity of -100 inputted for sesame seed bun")

    try:
        fixture.refill_ingredient(ingredient_list[1], -5.4)
    except Exception as e:
        message = e.__str__()

    assert (message == "Negative quantity of -5.4 inputted for kaiser roll")

    try:
        fixture.refill_ingredient(ingredient_list[2], 0)
    except Exception as e:
        message = e.__str__()

    assert (message == "Negative quantity of -5.4 inputted for kaiser roll")
    
    #invalid values (values less than zero) will not change value of inventory
    assert(ingredients_dic[ingredient_list[0]] == 10)
    assert(ingredients_dic[ingredient_list[1]] == 11)
    assert(ingredients_dic[ingredient_list[2]] == 13)
    
def test_decrement_inventory(fixture): 
    print("---test decrement inventory---")
    
    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    fixture.decrement_ingredient(ingredient_list[3], 10)
    fixture.decrement_ingredient(ingredient_list[4], 15)
    fixture.decrement_ingredient(ingredient_list[5], 15)

    assert(ingredients_dic[ingredient_list[3]] == 60)
    assert(ingredients_dic[ingredient_list[4]] == 55)
    assert(ingredients_dic[ingredient_list[5]] == 55)
    
def test_decrement_inventory_with_invalid_value(fixture):
    
    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    
    message = ""

    try:
        fixture.decrement_ingredient(ingredient_list[3], -1)
    except Exception as e:
        message = e.__str__()

    assert (message == "Negative quantity of -1 inputted for beef patty")
        
    try:
        fixture.decrement_ingredient(ingredient_list[4], -5)
    except Exception as e:
        message = e.__str__()
        
    assert (message == "Negative quantity of -5 inputted for chickpea patty")

    try:
        fixture.decrement_ingredient(ingredient_list[5], -5)
    except Exception as e:
        message = e.__str__()

    assert (message == "Negative quantity of -5 inputted for chicken patty")

    try:
        fixture.decrement_ingredient(ingredient_list[3], 100)
    except Exception as e:
        message = e.__str__()

    #there are only 70 in stock
    assert (message == "Cannot decrement beef patty by 100. Currently have 70 in stock")

    try:
        fixture.decrement_ingredient(ingredient_list[4], 80)
    except Exception as e:
        message = e.__str__()
    
    assert (message == "Cannot decrement chickpea patty by 80. Currently have 70 in stock")

    try:
        fixture.decrement_ingredient(ingredient_list[5], -250)
    except Exception as e:
        message = e.__str__()

    try:
        fixture.decrement_ingredient(ingredient_list[5], -10.4)
    except Exception as e:
        message = e.__str__()




##########################################################################
#--------------simple print tests (just for checking)--------------------#
##########################################################################

system = System()
system.add_ingredient (Ingredient("ingredient1", 2, 3), 10)
system.add_ingredient (Ingredient("ingredient2", 1.5), 11)
system.add_ingredient (Ingredient("ingredient3", 3), 13)
system.add_ingredient(Ingredient("Lettuce", 2), 10)
#let's say max allowed quntity for tomato  is 2 (the third parameter is the max_allowed)
#Ingredient(name, price, max_allowed, ingredient_type)
system.add_ingredient(Ingredient("Tomato", 5, 2), 10)
system.add_ingredient(Ingredient("Lettuce", 5, 2), 10)
system.add_ingredient(Ingredient("Onion", 5, 2), 10)
system.add_ingredient(Ingredient("Cheddar cheese", 5, 2), 10)
system.add_ingredient(Ingredient("Swiss cheese", 5, 2), 10)

system.add_ingredient(Ingredient("bun1", 5, 2, ingredient_type.bun), 10)
system.add_ingredient(Ingredient("bun2", 3, 2,ingredient_type.bun), 10)
system.add_ingredient(Ingredient("bun3", 5, 2,ingredient_type.bun), 10)
system.add_ingredient(Ingredient("patty1", 5, 2,ingredient_type.patty), 10)
system.add_ingredient(Ingredient("patty2", 5, 2,ingredient_type.patty), 10)


print("*********items in stock************\n")
ingredients_dic = system.get_stock_status()
all_ingredients = system.get_ingredients ()

for i in all_ingredients:
    print("ingredient name:{} quantity: {}".format(i.get_name(), ingredients_dic[i]))
print("\n")

print ("=====buns in stock:")
for i in system.get_buns():
    print(i)
print ("=====patties in stock:")
for i in system.get_patties():
    print(i)
print ("=====other ingredients in stock:")
for i in system.get_other_ingredients ():
    print(i)
print ("=====drinks in stock:")
for i in system.get_drinks():
    print(i)
print ("\n************test refilling the stock***********")
ingredient_list = system.get_ingredients ()
system.refill_ingredient(ingredient_list[0], 10)
system.refill_ingredient(ingredient_list[1], 10)
system.refill_ingredient(ingredient_list[2], 10)
system.refill_ingredient(ingredient_list[3], 10)
system.refill_ingredient(ingredient_list[4], 10)
system.refill_ingredient(ingredient_list[5], 10)

print ("items after refilling")
all_ingredients = system.get_ingredients ()
for i in all_ingredients:
    print("ingredient name:{} quantity: {}".format(i.get_name(), ingredients_dic[i]))

print ("\n*********test decrementing the stock*********")
system.decrement_ingredient(ingredient_list[0], 5)
system.decrement_ingredient(ingredient_list[1], 5)
system.decrement_ingredient(ingredient_list[2], 5)
system.decrement_ingredient(ingredient_list[3], 5)
system.decrement_ingredient(ingredient_list[4], 5)
system.decrement_ingredient(ingredient_list[5], 5)


print ("items after decrementing")
all_ingredients = system.get_ingredients ()
for i in all_ingredients:
    print("ingredient name:{} quantity: {}".format(i.get_name(), ingredients_dic[i]))

print("\n*********test refilling stock with invalid values********")
try:
    system.refill_ingredient(ingredient_list[3], -3)
except Exception as e:
    print(e)

try:
    system.refill_ingredient(ingredient_list[4], -3.5)
except Exception as e:
    print(e)

try:
    system.refill_ingredient(ingredient_list[4], -100)
except Exception as e:
    print(e)

print("\n*********test decrementing stock with invalid values********")
try:
    system.decrement_ingredient(ingredient_list[3], -3)
except Exception as e:
    print(e)

try:
    system.decrement_ingredient(ingredient_list[3], 11)
except Exception as e:
    print(e)

try:
    system.decrement_ingredient(ingredient_list[4], -5)
except Exception as e:
    print(e)

try:
    system.decrement_ingredient(ingredient_list[5], 100)
except Exception as e:
    print(e)
    
print("\n***********Creating a valid main***********")
main = mainDish(main_type.double)
ingredients_in_stock = system.get_ingredients()
main.add_ingredient(all_ingredients[0], 2)
main.add_ingredient(all_ingredients[1])
main.add_ingredient(all_ingredients[2])
main.add_ingredient(all_ingredients[3])
main.add_ingredient(all_ingredients[4])
main.add_ingredient(all_ingredients[5])

main.add_ingredient(system.search_item("Tomato"))

print(main)
print("*******")
for items in main.get_mainList():
    print(items, "quantity: ", main._quantities[items])

print("\nCreate another main")
main2 = mainDish(main_type.double)
ingredients_in_stock = system.get_ingredients()
main2.add_ingredient(all_ingredients[2], 2)
main2.add_ingredient(all_ingredients[1])
for items in main2.get_mainList():
    print(items, "quantity: ", main2._quantities[items])
    
print("\n***********Creating invalid main***********")
print("Test 1\ntest creating main which contains 3 tomatoes")
invalid_main = mainDish('some-type')
try:
    invalid_main.add_ingredient(system.search_item("Tomato"), 3)
except Exception as e:
    print(e)
    print ("(the max number allowed for tomato in this system is 2)")
    

print("\n**********creating an order**********")
order = Order()
order.add_main(main)
print("order is: {}".format(order))
print("order id is: {}".format(order.get_ID()))
print("type is: {}".format(order.get_type()))
print("main is: {}".format(order.get_main()))
for item in order.get_all_items():
    print (item.get_name()) 

print("total cost is: ${}".format(order.total_cost()))

order2 = Order()
order2.add_main(main2)
print("\norder is: {}".format(order))
print("order id is: {}".format(order.get_ID()))
print("type is: {}".format(order.get_type()))
print("main is: {}".format(order.get_main()))

print("\n*********order list*********")
print("Item's in current order")
system.checkout_order(order)
system.checkout_order(order2)

print("Total Preparing Orders: {}".format(len(system.get_current_orders())))
for i in system.get_current_orders():
    print("Preparing...{}".format(i))
   
print("\nServe orders \n")
system.serve_order(order)
system.serve_order(order2)
print("Item's in served orders")

print("Total Served: {}".format(len(system.get_served_orders())))
for i in system.get_served_orders():
    print("Served...".format(order.get_ID()))
    print(i)

print("\n********Ingredients decremented after checkout*********")
for i in all_ingredients:
    print("ingredient name:{} quantity: {}".format(i.get_name(), ingredients_dic[i]))
    
print("\n********Cancellation of Order*********")

main3 = mainDish(main_type.double)
main3.add_ingredient(all_ingredients[1], 2)
main3.add_ingredient(all_ingredients[3])

order3 = Order()
order3.add_main(main3)
print("order is: {}".format(order3))
print("order id is: {}".format(order3.get_ID()))

print ("Cancelling order")
system.checkout_order(order3)
system.cancel_order (order3)
''' 

system.add_ingredient(Side("fries", 2, 3, 4, 75, 125, 200), 10000)
system.add_ingredient(Side ("nuggets", 2, 4, 6, 3, 6, 12), 500)
sides_quantities = system.get_items_quantities(system.get_sides())
small_sides_price = system.get_small_side_prices(system.get_sides())
medium_sides_price = system.get_medium_side_prices(system.get_sides())
large_sides_price = system.get_large_side_prices(system.get_sides())

print(sides_quantities)
print(small_sides_price)
print(medium_sides_price)
print(large_sides_price)

side_order1 = Order()
side_order1.add_side(system.search_item("fries"), size.small, 1)
print("total cost is: "+ str(side_order1.total_cost()))
system.checkout_order(side_order1)
print("after checking-out order, there are {} grams in stock".format(system.get_stock_status()[system.search_item("fries")]))

'''
print ("\n****************test sides (weight)************")
print("test fries")
# a small fires is 75g medium is 125 large is 100
#side(name, small_price, medium_price, large_price, small_weigt, medium_weight, large_weight)
fries = Side ("fries", 2, 3, 4, 75, 125, 200)
#check weights 
print ("small fries weight is " + str(fries.get_weight(size.small)))
print ("medium fries weight is " + str(fries.get_weight(size.medium)))
print ("large fries weight is " + str(fries.get_weight(size.large)))
#check prices
print ("small fries price is " + str(fries.get_price(size.small)))
print ("medium fries price is " + str(fries.get_price(size.medium)))
print ("large fries price is " + str(fries.get_price(size.large)))

# small fries added to stock 
system.add_ingredient(fries, 75)
print("there are {} grams of fries in stock".format(system.get_stock_status()[fries]))
print("creating an order of one small fries")

side_order1 = Order()
side_order1.add_side(fries, size.small, 1)
print("total cost is: "+ str(side_order1.total_cost()))
system.checkout_order(side_order1)
print("after checking-out order, there are {} grams in stock".format(system.get_stock_status()[fries]))

# i will add 125g (medium) to stock
system.add_ingredient(fries, 125)
print("there are {} grams of fries in stock".format(system.get_stock_status()[fries]))
print("creating an order of one medium fries")

side_order2 = Order()
side_order2.add_side(fries, size.medium, 1)
print("total cost is: "+ str(side_order2.total_cost()))
system.checkout_order(side_order2)
print("after checking-out order, there are {} grams in stock".format(system.get_stock_status()[fries]))

# large fries added to stock
system.add_ingredient(fries, 200)
print("there are {} grams of fries in stock".format(system.get_stock_status()[fries]))
print("creating an order of one large fries")

side_order3 = Order()
side_order3.add_side(fries, size.large, 1)
print("total cost is: "+ str(side_order3.total_cost()))
system.checkout_order(side_order3)
print("after checking-out order, there are {} grams in stock".format(system.get_stock_status()[fries]))


print("\ntest nuggets")
nuggets = Side ("nuggets", 2, 4, 6, 3, 6, 12)
print ("small nuggets size is " + str(nuggets.get_weight(size.small)))
print ("medium nuggets size is " + str(nuggets.get_weight(size.medium)))
print ("large nuggets size is " + str(nuggets.get_weight(size.large)))
print ("small nuggets price is " + str(nuggets.get_price(size.small)))
print ("medium nuggets price is " + str(nuggets.get_price(size.medium)))
print ("large nuggets price is " + str(nuggets.get_price(size.large)))
system.add_ingredient(nuggets, 200)
print("there are {} nuggets in stock".format(system.get_stock_status()[nuggets]))
print("creating an order of one small nuggets")
side_order2 = Order()
side_order2.add_side(nuggets, size.small, 1)
print("total cost is: "+ str(side_order2.total_cost()))
system.checkout_order(side_order2)
print("after checking-out order, there are {} nuggets in stock".format(system.get_stock_status()[nuggets]))
'''
'''
print("\n*********test drinks**********")
print("test with coke and orange juice")
coke_bottle = Drink("Bottled coke", 3, 600)
coke_can = Drink("Canned coke", 2, 375)
canned_orange_juice = Drink("Canned Orange Juice", 2, 250)
bottled_orange_juice = Drink("Bottled Orange Juice", 4, 450)
print("Coke bottle is " + str(coke_bottle.get_size()) + "mL")

print("Coke can is " + str(coke_can.get_size()) + "mL")
print("Coke bottle price is $" + str(coke_bottle.get_price()))
print("Coke can price is $" + str(coke_can.get_price()))
print("bottled orange Juice is " + str(bottled_orange_juice.get_size()) + "mL")
print("canned orange Juice is " + str(canned_orange_juice.get_size()) + "mL")
print("bottled orange Juice price is $" + str(bottled_orange_juice.get_price()))
print("canned orange Juice price is $" + str(canned_orange_juice.get_price()))

system.add_ingredient(coke_bottle, 2)
system.add_ingredient(canned_orange_juice, 10)
print("there are {} bottles in stock".format(system.get_stock_status()[coke_bottle]))
print("there are {} cans of orange juice in stock".format(system.get_stock_status()[canned_orange_juice]))
drink_order = Order()
drink_order.add_drink(coke_bottle, 1)
drink_order.add_drink(canned_orange_juice, 1)
print("total cost is: $"+ str(drink_order.total_cost()))
system.checkout_order(drink_order)
print("after checking-out order, there are {} bottles of coke in stock".format(system.get_stock_status()[coke_bottle]))
print("after checking-out order, there are {} cans of orange juice in stock".format(system.get_stock_status()[canned_orange_juice]))

print("\n******************creating invalid order**************")
invalid_order = Order()
#there's only one sprite in stock... i will add 2 to the order
invalid_order.add_drink(system.search_item("Bottled coke"), 2)
#now when checking out the order it should raise exception
try:
    system.checkout_order(invalid_order)
except Exception as e:
    print(e)

