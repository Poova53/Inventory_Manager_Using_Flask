from core import app, db
from flask import request, render_template, flash
from core.models import Product, Location, ProductMovement
from sqlalchemy import func


@app.route("/Add/Edit/ViewProduct/", methods=["GET", "POST"])
def product():
    if request.method == "POST":
        add_data(Product, "product_name")   # adding new product to database
    
    products = Product.query.all()
    return render_template("product.html", products=products)


@app.route("/Add/Edit/ViewLocation/", methods=['GET', 'POST'])
def location():
    if request.method == "POST":
        add_data(Location, "location_name") # adding new location to database
        
    locations = Location.query.all()
    return render_template("location.html", locations=locations)

# Helper function to add data in Product or Location table
def add_data(model, key):
    name = request.form.get(key).strip()
    
    if not name:
        flash("Please enter valid name", "text-danger")
        return
        
    query = model.query.filter(model.name.ilike(f"%{name}%")).first()
    
    # if data exist in db
    if query and query.name.lower() == name.lower():
        flash("Name already exist!", "text-danger")
        return
    
    # else create and add data to db
    new = model(name=name.capitalize())
    db.session.add(new)
    db.session.commit()
    flash("Data added!", "text-success")  


@app.route("/Add/Edit/ViewProductMovement/", methods=["GET", "POST"])
def movement():
    if request.method == "POST":

        # getting all data from form to process the movement
        product = Product.query.filter(Product.name==request.form.get("product")).first()
        quantity = int(request.form.get("quantity"))
        from_location_name = request.form.get("from_location")
        to_location_name = request.form.get("to_location")
        
        # if want to move new product into a location
        if from_location_name == "import":
            # create new movement and add it to db
            to_location = Location.query.filter(Location.name==to_location_name).first()
            
            new_movement = ProductMovement(product=product, quantity=quantity, to_location=to_location)
            db.session.add(new_movement)
            db.session.commit()
            
            flash(f"{quantity} {product.name}(s) imported to {to_location.name}", "text-success")
        
        # above if condition fails means we want to move product from a location
        else:
            # collecting all given product from the from_location
            from_location = Location.query.filter(Location.name==from_location_name).first()
            product_movement_list = ProductMovement.query.\
                                        filter(ProductMovement.to_location==from_location, ProductMovement.product==product).\
                                        order_by(ProductMovement.quantity.desc()).all()
            
            # if the product is not in that location
            if not product_movement_list:
                flash(f"{product.name} not available in {from_location.name}", "text-danger")
            
            else:
                # getting the total stock of the product in that location
                total_quantity = db.session.query(func.sum(ProductMovement.quantity)).filter(
                    ProductMovement.to_location==from_location, ProductMovement.product==product
                ).scalar()
                
                # if the required quantity is greater than the stock available
                if quantity > total_quantity:
                    flash(f"{from_location.name} has only {total_quantity} {product.name}(s)", "text-danger")
                
                else:
                    # getting required quantity from stock
                    added_quantity = 0
                    for product_movement in product_movement_list:
                        added_quantity += product_movement.quantity
                        
                        if added_quantity >= quantity:
                            if added_quantity > quantity:
                                product_movement.quantity = added_quantity - quantity
                                
                            else:
                                product_movement.quantity = 0
                                
                            db.session.commit()
                            break
                        product_movement.quantity = 0

                    # if we want to move product out(export)
                    if to_location_name == "export":
                        # make the movement without to location
                        new_movement = ProductMovement(quantity=quantity, from_location=from_location, product=product)
                        flash(f"{quantity} {product.name}(s) exported successfully from {from_location.name}", "text-success")
                    
                    # else we want to move product to another location
                    else:
                        # make the movement
                        to_location = Location.query.filter(Location.name==to_location_name).first()
                        new_movement = ProductMovement(quantity=quantity, from_location=from_location, to_location=to_location, product=product)
                        flash(f"{quantity} {product.name}(s) moved from {from_location.name} to {to_location.name}", "text-success")
                    
                    db.session.add(new_movement)
                    db.session.commit()

    # querying all product movements, products and locations
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.asc()).all()
    products = Product.query.order_by(Product.name).all()
    locations = Location.query.order_by(Location.name).all()
    
    context = {"movements": movements, "products": products, "locations": locations}
    return render_template("movement.html", context=context)


# to get reports in each location
@app.route("/Warehouse/", methods=['GET'])
def warehouse():
    location = request.args.get("location")
    inventory = []
    
    if location:
        location_db = Location.query.filter(Location.name==location.capitalize()).first()
        
        if location_db:
            inventory = db.session.query(Product.name, func.sum(ProductMovement.quantity)).\
                            join(ProductMovement, Product.product_id==ProductMovement.product_id).\
                            join(Location, Location.location_id==ProductMovement.to_location_id).\
                            filter(ProductMovement.to_location_id==location_db.location_id).\
                            group_by(Product.name).\
                            order_by(Product.name.asc()).all()
    
    return render_template("warehouse.html", location=location, inventory=inventory)