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
    
def create_main_order (fixture):
    main = mainDish(main_type.double)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("beef patty"), 2)
    main.add_ingredient(fixture.search_item ("lettuce"), 1)

    order = Order()
    order.add_main(main)

    return order

def decrement_after_checkout(fixture):

    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    

    order = create_main_order(fixture)
    fixture.checkout_order(order)
    #Inventory decreases as order is checked out
    assert(ingredients_dic[ingredient_list[0]] == 8)
    assert(ingredients_dic[ingredient_list[3]] == 68)
    assert(ingredients_dic[ingredient_list[7]] == 9)

def make_order_without_checkout(fixture):

    order = create_main_order(fixture)
    # Inventory does not change
    assert(ingredients_dic[ingredient_list[0]] == 10)
    assert(ingredients_dic[ingredient_list[3]] == 70)
    assert(ingredients_dic[ingredient_list[7]] == 10)

def test_stock(fixture):
    
    order = create_main_order(fixture)
    
    patty = fixture.search_item("beef patty")
    num_patties_instock = fixture.get_stock_status()[patty]

    bun = fixture.search_item("sesame seed bun")
    num_buns_instock = fixture.get_stock_status()[bun]

    lettuce = fixture.search_item("lettuce")
    num_lettuce_instock = fixture.get_stock_status()[lettuce]
    
    fixture.checkout_order(order)
    
    assert (fixture.get_stock_status()[patty] == num_patties_instock - 2)
    assert (fixture.get_stock_status()[bun] == num_buns_instock - 2)
    assert (fixture.get_stock_status()[lettuce] == num_lettuce_instock - 1)
    
def decrement_small_fries(fixture):

    small_order = Order()
    small_order.add_side(fixture.search_item("fries"), size.small)
    fixture.checkout(small_order)
    assert(ingredients_dic[ingredient_list[16]] == 9925)


def decrement_medium_fries(fixture):

    medium_order = Order()
    medium_order.add_side(fixture.search_item("fries"), size.medium)
    fixture.checkout(medium_order)
    assert(ingredients_dic[ingredient_list[16]] == 9875)

def decrement_large_fries(fixture):

    large_order = Order()
    large_order.add_side(fixture.search_item("fries"), size.large)
    fixture.checkout(large_order)
    assert(ingredients_dic[ingredient_list[16]] == 9800)

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

def test_decrement_inventory_with_negative_value(fixture):

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
        fixture.decrement_ingredient(ingredient_list[5], -250)
    except Exception as e:
        message = e.__str__()

    try:
        fixture.decrement_ingredient(ingredient_list[5], -10.4)
    except Exception as e:
        message = e.__str__()

def test_decrement_greater_than_in_stock(fixture):

    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    message = ""

    try:
        fixture.decrement_ingredient(ingredient_list[3], 100)
    except Exception as e:
        message = e.__str__()

    assert (message == "Cannot decrement beef patty by 100. Currently have 70 in stock")

    try:
        fixture.decrement_ingredient(ingredient_list[4], 80)
    except Exception as e:
        message = e.__str__()

    assert (message == "Cannot decrement chickpea patty by 80. Currently have 70 in stock")

