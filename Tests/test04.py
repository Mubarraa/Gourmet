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

    return system

def create_base_single_order (fixture):

    main = mainDish(main_type.single)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("beef patty"), 1)

    order = Order()
    order.add_main(main)
    
    return order

def create_base_double_order (fixture):

    main = mainDish(main_type.double)
    main.add_ingredient(fixture.search_item ("sesame seed bun"), 2)
    main.add_ingredient(fixture.search_item ("chickpea patty"), 2)

    order = Order()
    order.add_main(main)
    
    return order

def create_base_wrap_order (fixture):

    main = mainDish(main_type.single)
    main.add_ingredient(fixture.search_item ("chicken patty"), 1)

    order = Order()
    order.add_main(main)
    
    return order


def decrement_base_checkout(fixture):
        
    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    

    order = create_base_order(fixture)
    fixture.checkout_order(order)

    assert(ingredients_dic[ingredient_list[0]] == 8)
    assert(ingredients_dic[ingredient_list[3]] == 69)

def base_order_without_checkout(fixture):

    order = create_base_order(fixture)
    
    # Inventory does not change
    assert(ingredients_dic[ingredient_list[0]] == 10)
    assert(ingredients_dic[ingredient_list[3]] == 70)    

def test_stock_baseSingle(fixture):
    
    order = create_base_single_order(fixture)
    
    patty = fixture.search_item("beef patty")
    num_patties_instock = fixture.get_stock_status()[patty]

    bun = fixture.search_item("sesame seed bun")
    num_buns_instock = fixture.get_stock_status()[bun]

    fixture.checkout_order(order)
    
    assert (fixture.get_stock_status()[patty] == num_patties_instock - 1)
    assert (fixture.get_stock_status()[bun] == num_buns_instock - 2)


def test_stock_baseDouble(fixture):

    order  = create_base_double_order(fixture)

    patty = fixture.search_item("chickpea patty")
    num_patties_instock = fixture.get_stock_status()[patty]
 
    bun = fixture.search_item("sesame seed bun")
    num_buns_instock = fixture.get_stock_status()[bun]

    fixture.checkout_order(order)

    assert (fixture.get_stock_status()[patty] == num_patties_instock - 2)
    assert (fixture.get_stock_status()[bun] == num_buns_instock - 2)


def test_stock_baseWrap(fixture):

    order  = create_base_wrap_order(fixture)

    patty = fixture.search_item("chicken patty")
    num_patties_instock = fixture.get_stock_status()[patty]
 
    fixture.checkout_order(order)

    assert (fixture.get_stock_status()[patty] == num_patties_instock - 1)

