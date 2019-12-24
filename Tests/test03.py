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

def test_buns (fixture):
    buns = fixture.get_buns()
    assert (len(buns) == 3)
    for i in buns:
        assert (i.get_name() in ["sesame seed bun", "kaiser roll", "potato roll"])


def test_ingredients (fixture):
    ingredients = fixture.get_other_ingredients()
    assert(len(ingredients) == 5)
    for i in ingredients:
        assert (i.get_name() in ["tomato", "lettuce", "cheese", "onion", "pickles"])

def test_patties(fixture):

    patties = fixture.get_patties()
    assert(len(patties) == 3)
    for i in patties:
        assert(i.get_name() in ["beef patty", "chicken patty", "chickpea patty"])

def test_drinks (fixture):
    drinks = fixture.get_drinks()
    assert(len(drinks) == 5)
    for i in drinks:
        assert (i.get_name() in ["Bottled sprite", "Bottled coke", "Canned coke", "Canned sprite", "Bottled water"])

def test_sides(fixture):
    sides = fixture.get_sides()
    assert(len(sides) == 2)
    for i in sides:
        assert (i.get_name() in ["nuggets", "fries"])

def test_sides_size(fixture):

    fries = fixture.search_item("fries")

    assert(fries.get_weight(size.small) == 75)
    assert(fries.get_weight(size.medium) == 125)
    assert(fries.get_weight(size.large) == 200)

    nuggets = fixture.search_item("nuggets")

    assert(nuggets.get_weight(size.small) == 3)
    assert(nuggets.get_weight(size.medium) == 6)
    assert(nuggets.get_weight(size.large) == 12)

def test_sides_price(fixture):

    fries = fixture.search_item("fries")
    assert(fries.get_price(size.small) == 2)
    assert(fries.get_price(size.medium) == 3)
    assert(fries.get_price(size.large) == 4)

    nuggets = fixture.search_item("nuggets")
    assert(nuggets.get_price(size.small) == 2)
    assert(nuggets.get_price(size.medium) == 4)
    assert(nuggets.get_price(size.large) == 6)
    

def test_main_price(fixture):

    single = mainDish(main_type.single)
    assert(single.total_cost() == 5)
    
    double = mainDish(main_type.double)
    assert(double.total_cost() == 7)
    
    wrap = mainDish(main_type.wrap)
    assert(wrap.total_cost() == 5)
    
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

def create_main_with_invalid_buns(fixture):

    main = mainDish(main_type.single)
    try:
        main.add_ingredient(search_item("sesame seed bun"), 3)
    except Exception as e:
        message = e.__str__()

    assert (message == "exceeded max allowed quantity: max for (sesame seed bun) is 2")


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

