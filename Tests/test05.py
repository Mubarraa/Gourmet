from item import *
from stock import *
from order import *
from system import *
import pytest


@pytest.fixture
def fixture():
    system = System()

    #sundaes 
    system.add_ingredient(Sundae("Chocolate Sundae", 3, 5, 6, 100, 150, 200), 1000)
    system.add_ingredient(Sundae ("Strawberry Sundae", 3, 5, 6, 100, 150, 200), 1000)

    return system

def test_sundaes (fixture):
    sundae = fixture.get_sundaes()

    assert(len(sundae) == 2)
    for i in sundae:
        assert (i.get_name() in ["Chocolate Sundae", "Strawberry Sundae"])

def test_sundae_price(fixture):

    choc = fixture.search_item("Chocolate Sundae")
    assert(choc.get_price(size.small) == 3)
    assert(choc.get_price(size.medium) == 5)
    assert(choc.get_price(size.large) == 6)

    strawb = fixture.search_item("Strawberry Sundae")
    assert(strawb.get_price(size.small) == 3)
    assert(strawb.get_price(size.medium) == 5)
    assert(strawb.get_price(size.large) == 6)

def test_sundae_size(fixture):

    choc = fixture.search_item("Chocolate Sundae")
    assert(choc.get_weight(size.small) == 100)
    assert(choc.get_weight(size.medium) == 150)
    assert(choc.get_weight(size.large) ==200)

    strawb = fixture.search_item("Strawberry Sundae")
    assert(strawb.get_weight(size.small) == 100)
    assert(strawb.get_weight(size.medium) == 150)
    assert(strawb.get_weight(size.large) == 200)
    
def decrement_small_sundae(fixture):

    small_order = Order()
    small_order.add_sundae(fixture.search_item("Chocolate Sundae"), size.small)
    fixture.checkout(small_order)

    assert(ingredients_dic[ingredient_list[0]] == 900)

def decrement_medium_sundae(fixture):

    medium_order = Order()
    medium_order.add_sundae(fixture.search_item("Strawberry Sundae"), size.medium)
    fixture.checkout(medium_order)
    assert(ingredients_dic[ingredient_list[1]] == 850)

def decrement_large_sundae(fixture):

    large_order = Order()
    large_order.add_side(fixture.search_item("Strawberry Sundae"), size.large)
    fixture.checkout(large_order)
    assert(ingredients_dic[ingredient_list[0]] == 800)


def test_decrement_inventory(fixture):

    print("---test decrement Sundae inventory---")

    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()
    fixture.decrement_ingredient(ingredient_list[0], 100)
    fixture.decrement_ingredient(ingredient_list[1], 100)

    assert(ingredients_dic[ingredient_list[0]] == 900)
    assert(ingredients_dic[ingredient_list[1]] == 900)

def test_refill_inventory(fixture):

    print("---test refill Sundae inventory---")
    
    ingredients_dic = fixture.get_stock_status()
    ingredient_list = fixture.get_ingredients()

    fixture.refill_ingredient(ingredient_list[0], 500)
    fixture.refill_ingredient(ingredient_list[1], 500)

    assert(ingredients_dic[ingredient_list[0]] == 1500)
    assert(ingredients_dic[ingredient_list[1]] == 1500)


