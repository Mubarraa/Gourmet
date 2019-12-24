from flask import Flask, render_template, url_for, redirect, request
from system import *
from item import *
from order import *
import pickle

app = Flask(__name__)

#system = System()
#system.load_data()

pickle_in = open("data.pickle", "rb")
system = pickle.load (pickle_in)

curr_order = []


################################################################################

@app.route("/", methods = ["GET", "POST"])
def order_first_page():
    pickle_out = open("data.pickle", "wb")
    pickle.dump(system, pickle_out)
    pickle_out.close()

    if request.method == "POST":
        return redirect (url_for('order_status', ID = request.form.get("id")))

    return render_template ("order_first_page.html")

#------------------------------------------------------------------#
############################# custom ##############################
#------------------------------------------------------------------#

#1-type
@app.route("/CustomOrder/type", methods = ["GET", "POST"])
def Custom_type_selection():
    if request.method == "POST":
        mainType = request.form.get("type")
        if mainType == 'single':
            mainType = main_type.single
        if mainType == 'double':
            mainType = main_type.double
        if mainType == 'wrap':
            mainType = main_type.wrap

        main = mainDish (mainType)
        if (len(curr_order) > 0):
            curr_order.pop(0)
        curr_order.append(Order())
        curr_order[0].add_main(main)

        return redirect (url_for ('burger_selection'))

    return render_template ("type_selection.html")

#2-burger selection
@app.route("/order/Custom", methods = ["GET", "POST"])
def burger_selection():
    buns =system.get_items_names(system.get_buns())
    patties = system.get_items_names(system.get_patties())
    ingredients = system.get_items_names(system.get_other_ingredients())

    buns_prices =system.get_items_prices(system.get_buns())
    patties_prices = system.get_items_prices(system.get_patties())
    ingredients_prices = system.get_items_prices(system.get_other_ingredients())


    mainType = curr_order[0].get_main().get_type()

    #converting the enum value to a string so that we can use it in the html template
    if mainType == main_type.single:
        mainType = 'single'
    if mainType == main_type.double:
        mainType = 'double'
    if mainType == main_type.wrap:
        mainType = 'wrap'

    if request.method == "POST":
        if mainType:

            main = curr_order[0].get_main()
            #i've just realized that when doing value = {{item}} if the item name is more than one word
            #then the value would be just the first wrord ... if it is sesame seed bun, value = sesame
            #and therefor search_time willn not find the item


            #updates: i've searched online and found that if we do value = '{{item}}' it will take all the words
           # print("bun is " + request.form["bun"])

            try:
                if mainType != 'wrap':
                    bun_name = request.form["bun"]
                    quantity = request.form[bun_name]
                    #if user choose bun but doesn't specify quantity, quantity will be 2 by default
                    if (quantity == ""):
                        quantity = "2"
                    main.add_ingredient(system.search_item(bun_name), int(quantity))


                # Base ingredients automatically added
                #main.add_ingredient(system.search_item ("lettuce"), 1)
                #main.add_ingredient(system.search_item ("tomato"), 1)

                order_patties = request.form.getlist('patty')

                for p in order_patties:
                    quantity = request.form[p]
                    if (quantity == ""):
                        quantity = "1"
                    main.add_ingredient(system.search_item(p), int(quantity))

                order_ingredients = request.form.getlist('ingredient')

                for i in order_ingredients:
                    quantity = request.form[i]
                    if (quantity == ""):
                        quantity = "1"
                    main.add_ingredient(system.search_item(i), int(quantity))

                curr_order[0].add_main(main)
                return redirect (url_for('sides_drinks'))
            except Exception as e:
                return render_template("burger_selection.html",buns= buns, patties = patties, ingredients = ingredients, bun_price = buns_prices, patty_price = patties_prices,ingredients_prices =ingredients_prices, main_type = mainType, error = e.__str__())
        else:
            return redirect (url_for('sides_drinks'))



    return render_template("burger_selection.html",buns= buns, patties = patties, ingredients = ingredients, bun_price = buns_prices, patty_price = patties_prices,ingredients_prices =ingredients_prices, main_type = mainType)


#3-sides and drinks
@app.route("/order/sidesAndDrinks", methods = ["GET", "POST"])
def sides_drinks():

    sides = system.get_items_names(system.get_sides())
    drinks = system.get_items_names(system.get_drinks())
    drinks_prices = system.get_items_prices(system.get_drinks())
    ingredients_prices = system.get_items_prices(system.get_other_ingredients())
    small_sides_price = system.get_small_side_prices(system.get_sides())
    medium_sides_price = system.get_medium_side_prices(system.get_sides())
    large_sides_price = system.get_large_side_prices(system.get_sides())

    if request.method == "POST":

        try:
            for d in drinks:
                if request.form[d] != "":
                    curr_order[0].add_drink(system.search_item(d), int(request.form[d]))


            if request.form["frinum"] != "":
                quantity = request.form["frinum"]
                amount = request.form["friessize"]

                if amount == "Small":
                    curr_order[0].add_side(system.search_item("Fries"), size.small, int(quantity))
                elif amount == "Medium":
                    curr_order[0].add_side(system.search_item("Fries"), size.medium, int(quantity))
                elif amount == "Large":
                    curr_order[0].add_side(system.search_item("Fries"), size.large, int(quantity))

            if request.form["nugnum"] != "":
                quantity = request.form["nugnum"]
                amount = request.form["nugsize"]

                if amount == "Small":
                    curr_order[0].add_side(system.search_item("Nuggets"), size.small, int(quantity))
                elif amount == "Medium":
                    curr_order[0].add_side(system.search_item("Nuggets"), size.medium, int(quantity))
                elif amount == "Large":
                    curr_order[0].add_side(system.search_item("Nuggets"), size.large, int(quantity))

            if request.form["chocnum"] != "":
                quantity = request.form["chocnum"]
                amount = request.form["chocsize"]

                if amount == "Small":
                    curr_order[0].add_sundae(system.search_item("Chocolate Sundae"), size.small, int(quantity))
                elif amount == "Medium":
                    curr_order[0].add_sundae(system.search_item("Chocolate Sundae"), size.medium, int(quantity))
                elif amount == "Large":
                    curr_order[0].add_sundae(system.search_item("Chocolate Sundae"), size.large, int(quantity))

            if request.form["strawnum"] != "":
                quantity = request.form["strawnum"]
                amount = request.form["strawsize"]

                if amount == "Small":
                    curr_order[0].add_sundae(system.search_item("Strawberry Sundae"), size.small, int(quantity))
                elif amount == "Medium":
                    curr_order[0].add_sundae(system.search_item("Strawberry Sundae"), size.medium, int(quantity))
                elif amount == "Large":
                    curr_order[0].add_sundae(system.search_item("Strawberry Sundae"), size.large, int(quantity))


            return redirect(url_for('Checkout'))

        except Exception as e:
            return render_template("sides_drinks.html", sides = sides, drinks = drinks, drinks_prices = drinks_prices, small_sides_price = small_sides_price, medium_sides_price = medium_sides_price, large_sides_price = large_sides_price, error = e.__str__())


    return render_template("sides_drinks.html", sides = sides, drinks = drinks, drinks_prices = drinks_prices, small_sides_price = small_sides_price, medium_sides_price = medium_sides_price, large_sides_price = large_sides_price)

#------------------------------------------------------------------#
############################# base #################################
#------------------------------------------------------------------#

@app.route("/BaseOrder/type", methods = ["GET", "POST"])
def Base_type_selection():

    #converting the enum value to a string so that we can use it in the html template

    if request.method == "POST":
        mainType = request.form.get("type")

        if mainType == 'single':
            mainType = main_type.single
        if mainType == 'double':
            mainType = main_type.double
        if mainType == 'wrap':
            mainType = main_type.wrap

        main = mainDish (mainType)
        if (len(curr_order) > 0):
            curr_order.pop(0)
        curr_order.append(Order())
        curr_order[0].add_main(main)
        return redirect (url_for ('base_selection'))

    return render_template ("type_selection.html")

       

@app.route("/order/Base", methods = ["GET", "POST"])
def base_selection():

    patties = system.get_items_names(system.get_patties())
    patties_prices = system.get_items_prices(system.get_patties())

    mainType = curr_order[0].get_main().get_type()
    if mainType == main_type.single:
        mainType = 'single'
    if mainType == main_type.double:
        mainType = 'double'
    if mainType == main_type.wrap:
        mainType = 'wrap'

    if request.method == "POST":
        main = curr_order[0].get_main()

        if mainType:    
            try:
                if mainType != 'wrap':
                    main.add_ingredient(system.search_item ("sesame seed bun"), 2)

                #main.add_ingredient(system.search_item ("lettuce"), 1)
                #main.add_ingredient(system.search_item ("tomato"), 1)

                order_patties = request.form.getlist('patty')

                for p in order_patties:
                    if mainType == 'double':
                        main.add_ingredient(system.search_item(p), 2)
                    else:
                        main.add_ingredient(system.search_item(p), 1)

                curr_order[0].add_main(main)
                return redirect (url_for('sides_drinks'))
            except Exception as e:
                return render_template("base_selection.html", patties = patties, patties_prices = patties_prices, main_type = mainType)

        else:
            return redirect (url_for('sides_drinks'))
        
            
    return render_template("base_selection.html", patties = patties, patties_prices = patties_prices, main_type = mainType)


#----------------------------------------------------------------------#
############################# checkout #################################
#----------------------------------------------------------------------#

@app.route("/order/checkout", methods = ["GET", "POST"])
def Checkout():

    if (request.method == "POST"):
        return redirect (url_for('order_status', ID = curr_order[0].get_ID()))

    try:
        system.checkout_order(curr_order[0])

        order = curr_order[0]

        #whenever an order is placed, picke the system object again
        pickle_out = open("data.pickle", "wb")
        pickle.dump(system, pickle_out)
        pickle_out.close()

        order = curr_order[0]
        items = curr_order[0].get_all_items()
        quantity = curr_order[0].get_quantities()
        mainType = curr_order[0].get_main().get_type()

        if mainType == main_type.single:
            mainType = 'Single'
        if mainType == main_type.double:
            mainType = 'Double'
        if mainType == main_type.wrap:
            mainType = 'Wrap'

        return render_template("checkout.html", order = order, items = items, quantity = quantity, mainType = mainType)

    except Exception as e:

        return  render_template("checkout.html", error = e.__str__())



#checking order status
@app.route("/status/<ID>", methods = ["GET", "POST"])
def order_status(ID):
    try:
        order = system.get_order (int(ID))
        #str() will assing status to 'True' if the boolean returned is true and 'False' otherwise
        status = str(system.is_ready (int(ID)))
        return render_template("order_status.html", order = order, status = status)
    except Exception as e:
        return render_template("order_status.html", error = e.__str__())

#------------------------------------------------------------------#
############################# staff #################################
#------------------------------------------------------------------#


@app.route ("/staff", methods = ["GET", "POST"])
def serve_order ():

    pickle_out = open("data.pickle", "wb")
    pickle.dump(system, pickle_out)
    pickle_out.close()

    if request.method == 'POST':
        for order in system.get_current_orders():
            if str(order.get_ID()) in request.form:
                system.serve_order(order)


    orders = system.get_current_orders()

    return render_template ("serve.html", orders = orders)

@app.route("/staff/stock", methods = ["GET", "POST"])
def stock ():

    pickle_out = open("data.pickle", "wb")
    pickle.dump(system, pickle_out)
    pickle_out.close()

    items = system.get_items_names (system.get_ingredients())
    quantities = system.get_items_quantities(system.get_stock_status())

    if (request.method == "POST"):
        try:
            for item in system.get_ingredients():
                q = request.form.get(item.get_name(), 0)
                if q != '':
                    system.refill_ingredient(item, int(q))
            #getting the new quantities after refilling :
            quantities = system.get_items_quantities(system.get_stock_status())
            return render_template("stock.html", items = items, quantities = quantities)
        except Exception as e:
            print (e.__str__())
            return render_template("stock.html", items = items, quantities = quantities, error = e.__str__())

    return render_template("stock.html", items = items, quantities = quantities)

@app.route("/staff/Side")
def Side_inventory ():

    items = system.get_items_names(system.get_sides())
    quantities = system.get_items_quantities(system.get_sides())
    return render_template("side_inventory.html", items = items, quantities = quantities)

@app.route("/staff/Main")
def Main_inventory ():

    items = system.get_items_names(system.get_buns() + system.get_patties() + system.get_other_ingredients())
    quantities = system.get_items_quantities(system.get_buns() + system.get_patties() + system.get_other_ingredients())

    return render_template("Main_inventory.html", items = items, quantities = quantities)

@app.route("/staff/Drinks")
def Drink_inventory ():

    items = system.get_items_names(system.get_drinks())
    quantities = system.get_items_quantities(system.get_drinks())

    return render_template("Drinks_inventory.html", items = items, quantities = quantities)

@app.route("/staff/Sundae")
def Sundae_inventory ():

    items = system.get_items_names(system.get_sundaes())
    quantities = system.get_items_quantities(system.get_sundaes())
    return render_template("Sundae_inventory.html", items = items, quantities = quantities)

@app.route("/staff/orders")
def All_Orders ():
    current_length = len(system.get_current_orders())
    served_length = len(system.get_served_orders())
    current_orders = system.get_current_orders()
    served_orders = system.get_served_orders()

    return render_template("all_orders.html", current_orders = current_orders, served_orders = served_orders, current_length = current_length, served_length = served_length)

app.run(debug=True, port = 5006)

