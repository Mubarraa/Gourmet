from item import *
from stock import *
from order import *
from system import *
import pytest


@pytest.fixture
def fixture():
    system = System()
    
    #buns
    system.add_ingredient(Ingredient("sesame seed bun", 0, 2,ingredient_type.bun), 10)
    system.add_ingredient(Ingredient("kaiser roll", 0, 2,ingredient_type.bun), 11)
    system.add_ingredient(Ingredient("potato roll", 0, 2,ingredient_type.bun), 13)

    #patties
    system.add_ingredient(Ingredient("beef patty", 0, 2,ingredient_type.patty), 70)
    system.add_ingredient(Ingredient("chickpea patty", 0, 2,ingredient_type.patty), 70)
    system.add_ingredient(Ingredient("chicken patty", 0, 2,ingredient_type.patty), 70)

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

#Once order is complete, total number of customers served will increase

def doubleBurger_order (fixture):

    main = mainDish(main_type.double)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("beef patty"), 2)
    main.add_ingredient(fixture.search_item ("lettuce"), 1)

    order = Order()
    order.add_main(main)
    fixture.checkout_order(order)
    
    return order

def test_quantity_order (fixture):
    
    main = doubleBurger_order (fixture)
    quantities = main.get_quantities ()
    assert (quantities[fixture.search_item("sesame seed bun")] == 2)
    assert (quantities[fixture.search_item("beef patty")] == 2)
    assert (quantities[fixture.search_item("lettuce")] == 1)
    
def test_serve_order (fixture):

    order = doubleBurger_order (fixture)

    assert(fixture.get_next_order() == order)

    assert (len(fixture.get_current_orders()) == 1)
    fixture.serve_order(order)
    assert(len(fixture.get_current_orders()) == 0)
    assert(len(fixture.get_served_orders()) == 1)

def test_total_for_double_burger (fixture):
    
    order = doubleBurger_order(fixture)
    total_cost = order.total_cost()
    
    assert(total_cost == 7 + 1)   

def singleBurger_order (fixture):
    
    main = mainDish(main_type.single)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("beef patty"), 1)
    main.add_ingredient(fixture.search_item ("lettuce"), 1)
    
    order = Order()
    order.add_main(main)
    fixture.checkout_order(order)
    
    return order
def wrap_order (fixture):
    
    main = mainDish(main_type.wrap)
    main.add_ingredient(fixture.search_item ("beef patty"), 1)
    main.add_ingredient(fixture.search_item ("lettuce"), 1)
    
    order = Order()
    order.add_main(main)
    fixture.checkout_order(order)
    
    return order
    
def test_total_for_single_burger (fixture):

    order = singleBurger_order(fixture)
    total_cost = order.total_cost()
    
    assert(total_cost == 5 + 1)
    
def test_total_for_wrap (fixture):
    
    order = wrap_order(fixture)
    total_cost = order.total_cost()
    
    assert(total_cost == 5 + 1)
    
def test_order_id (fixture):
    
    order = singleBurger_order(fixture)
    single_ID = order.get_ID()
    
    order = doubleBurger_order(fixture)
    double_ID = order.get_ID()
    
    order = wrap_order(fixture)
    wrap_ID = order.get_ID()
    
    assert(single_ID != double_ID)
    assert(double_ID != wrap_ID)
    assert(single_ID != wrap_ID)

def test_invalid_ID(fixture):

    try:
        fixture.is_ready(200)
    except Exception as e:
        message = e.__str__()

    assert(message == "Order ID 200 does not exist")
    
def test_orderID_message(fixture):

    order = doubleBurger_order(fixture)
    ID = order.get_ID()
    
    #frontend will display "Preparing" if is_ready() is false
    message = fixture.is_ready(ID)
    assert(message == False)

    #frontend will display "Order to be collected!" if is_ready() is true
    fixture.serve_order(order)
    message = fixture.is_ready(ID)
    assert(message == True)
    
