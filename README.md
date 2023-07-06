# **Inventory Manager**

This app helps to manage the inventory of warehouses located in different locations. It allow users to add products and locations and as well as move products from one location to another. I utilized Python's **Flask** framework along with SQLite for the database and HTML, CSS, Bootstrap and Javascript for the project.

## [**Database Tables**](https://github.com/Poova53/Inventory_Manager_Using_Flask/tree/main/instance)

In this project SQLite was used as the database engine for the warehouse management system. SQLite is a lightweight, serverless and self contained database engine that offers a simple and efficient way to store and retrieve data, making it suitable for managing the inventory of warehouses.

By utilizing SQLite as database engine, I developed a warehouse database that includes tables for products, locations and product movements. Flask SQLAlchemy is used as the database ORM(Object Relational Mapping). The models for the database are stored in models.py file.

### Product Table

This table consist of two columns product_id which serves as the primary key and name column which is unique, stores the name of the product.

![product_table](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/867691af-1138-4779-939c-23a793a5c7d9)


### Location Table

The location table consists of two columns location_id which is the primary key and location column which is unique and stores the name of each warehouse location.

![location_table](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/a715610b-7595-4d29-bc8c-8c22ef9c30b4)


### Product Movement Table

The product movement table consists of six columns:
1. movement_id: primary key
2. timestamp: It records the date and time of the product movement.
3. from_location_id: It stores the identifier of the location from which the product is being moved. It references the location_id in the location table, indicating the source location of the product.
4. to_location_id: It stores the identifier of the destination for the product movement. It references the corresponding location_id in the location table, indicating the target location where the product is being moved.
5. product_id: It stores the identifier of the specific product being moved. It references the product_id in the product table, linking the movements to the relevant product.
6. quantity: It records the quantity or amount of the product being moved.

![product_movement_table](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/828d7c70-5f54-4ec6-81d7-a8f47c4936dd)


---

## **Views**

In Flask, views are the functions or methods that handle HTTP requests from clients and generate HTTP responses. Views define the routes of the application, which determines the URL that trigger specific views. Flasks views and routing system provide a straightforward way to map URL routes to specific functions and handle incoming requests from clients in a clear and organized manner.

This project has three views:
- Add/Edit/ViewProduct
- Add/Edit/ViewLocation
- Add/Edit/ViewProductMovement

### Add/Edit/ViewProduct

In this view, users can view a list of existing products including their IDs and names. It shows the available products stored in the database. By filling the form provided in the page, user can able to add new product to the database.

![view_product](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/d2296af1-5577-4d93-8346-c02afe0539e7)


### Add/Edit/ViewLocation

In this view, users can view a list of existing warehouse locations including their IDs and name. User can utilize this page to add new warehouse location to the database by filling out the form.

![view_location](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/84b4c24f-8b70-41f4-b2f6-8334f934fc02)


### Add/Edit/ViewProductMovement

This view is a key component of this web application that allow users to track and perform movements of products within the warehouses. In this view, user are presented with a list of product movements. Each movement in the list includes details such as source location(from location), destination location(to location), product name, timestamp of the movement and the quantity of the product moved. It allow users to see all the historical movements of the products. User can alse perform new movements. User can initiate a new movement by specifying the source location, destination location, product name and the quantity being moved.

![view_product_movement](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/7f88cce3-6bc4-4ec2-b33c-1e5f165f80f8)


In the form, the import option in the source input is used move new products into our warehouse and the export option in the destination is used to move products out from our warehouses. The form submission has client side validation checks using JavaScript. When user submits the form, the JavaScript validation checks triggered. It verifies the input value and validate them. The validation fails on anyone of the below conditions:
- if anyone of the field was not filled.
- if the source and destination were same.
- if source selected as import and destionation as export.

![pm_source_and_destination_same](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/77c94d84-8c4b-4036-ba59-679064fb3cdc)

![pm_import_and_export](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/b3896802-2522-4e93-9ac1-f57f31c82c71)


If any above conditions met, javascript generates and present the error message to the user. This validation checks prevents unnecessary form submissions and reduce server side validation. if if passes the validation, form data is submitted to the server side for further processing.

In the server side, many checks and processes need to be done. At first the product model is queried using the product name from the form. Now we need to check the source location(from location).

1.If the "from location" is marked as "import," the system creates a new product movement model using the product, destination location (to location), and quantity provided through the form. In this case, the "from location" is set as null or left blank. Then the model is added to the database, and a confirmation message is sent to the client using Flask's flash functionality, confirming that the product has been successfully moved to the specified destination.

![pm_imported](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/e11a7caa-c5ae-4fb1-9921-a657194c680d)


2. If the source location (from location) is specified, we proceed to check if the requested product is available at that location. If the product is not available, an error message is sent to the client, notifying them that the product is not available at the specified source location and the request could not be processed.

![pm_not_available](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/7fef6109-a434-479b-8d84-0a3eda8e7136)


3. If the product is available, we need to query all product movements with the to location as the specified source location in order to determine the total quantity available. If the available quantity is less than the required quantity, an error message is sent to the client indicating the limited quantity available at that location. The error message informs the client about the specific quantity available for that product in the given location.

![pm_less_quantity_available](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/6c762bc7-ed57-46e1-a605-8f9d35f16f4d)


4. If the required quantity is available, we take the list of all models in descending order based on their quantity. We assign a variable called "added_quantity" with a value of 0. Then, we iterate through the list, subtracting the quantity from each model and adding it to "added_quantity" until "added_quantity" becomes greater than or equal to the requested quantity. If the condition is satisfied and "added_quantity" is greater than the requested quantity, we assign the difference to the current model in the loop. If "added_quantity" is equal to the requested quantity, we assign the current model a value of zero. Finally, we break out of the loop.

5. Now that we have obtained the required quantity from the source location, our next step is to make the movement of the product to the designated destination location. If the destination is marked as "export," we create a new Product Movement model using the from location, product, and required quantity. In this case, the to location is set as null or left blank. However, if the destination is not marked as "export," we create a model using the source location as the from location, the destination location as the to location, the product, and the quantity. After creating the appropriate model, we save the changes to the database and send a success message to the client, confirming the successful movement of the product.

![pm_exported](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/ac12a2ca-9698-4f28-8d44-2d584dda9849)

![pm_movement_success](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/9905a548-2008-4350-bdd3-44982807c8ce)


---

## **Use Case**

- Created 4 products.
![view_product](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/d2296af1-5577-4d93-8346-c02afe0539e7)


- Created 4 locations.
![view_location](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/84b4c24f-8b70-41f4-b2f6-8334f934fc02)


- Make Product Movements.
- At first Moved all products to a different locations with a quantity of 100.


![four_products_added](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/06033bb0-bcfb-4232-a5aa-286a14b52cea)

- Moved all the products with random quantity from one location to another.
- More than 20 moves were made across these warehouses.
- After making many number of moves, the total quantity of all products remains unchanged. This ensures the consistency of the inventory system, as the sum of the quantities before and after the movements remains the same. Products in each location were shown in below reports.

**In product movement view**
![after_moved](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/3be77a64-4718-4f84-abb6-f4b8cc1f6763)


**In database**
![database_after_moved](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/a8036925-b591-4f8c-a839-0a15ef760eec)


---

## **Report**

Created an warehouse view to present the products and its quantity in each location. This view takes location as query parameter in URL(http://127.0.0.1:5000/Warehouse/?location=<location name>). User can enter this report of a specific location by click the the location name in View Product Movement view. It is important to note that **some products are moved out** (exported). So considering the exported products in the quantity summation, the total quantity of all products remains balanced.

- In Chennai
![report_in_chennai](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/fd578455-0173-445f-a9c8-a8988c1f2d2b)


- In Bangalore
![report_in_bangalore](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/12506119-69b6-467d-bcaa-b81b68cc82a0)


- In Kochi
![report_in_kochi](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/7fd00e32-9c40-4456-a2e6-147957170e23)


- In Hyderabad
![report_in_hyderabad](https://github.com/Poova53/Inventory_Manager_Using_Flask/assets/75072789/a679db0e-b9fe-4015-8d21-6ebb8699428d)
