# Crash Course Coding Command-line CRUD Project

## About

This project will ultimately be used in the "Crash Course Coding" curriculum to expose beginner developers to the following:

    - Fundamentals of Python and SQL
    - Database design, database relationships, and data modeling
    - Object Relational Mapping (ORM)
    - Command-line interface (CLI) input/output
    - Basic data validation and error handling for CRUD operations
    - Reading and parsing data files

In this project the developer will use Python with SQLAlchemy to create a command line interface tool to perform create, read, update, and delete operations on a coffee shop's database. This includes a database installer which will parse the coffee shop's current customer, product, and transaction data files into objects and upload them to the database.

## Installation

1. Install [XAMPP](https://www.apachefriends.org/download.html) and [Python](https://www.python.org/downloads/) if you do not already have them.
2. Open a terminal and navigate to the directory where you would like the project installed. 
3. Clone this repository: 
```
git clone https://github.com/adobrusky/store-crud.git
```
4. Run the following command to install dependencies:
```
pip install Flask SQLAlchemy mysql-connector
```
5. Make sure the SQL server is turned on in XAMPP. Take note of the port (it should be 3306 by default).
6. Open the shell of the SQL server and connect to it with `mysql -u root`
7. Create a new database: `CREATE DATABASE store`
8. Depending on how you set up the database's connection information, you may have to modify line 45 in `installer\installer.py` and line 11 in `main.py`. 
    - By default: authority="localhost", port=3306, database_name="store", username="root", password=""
9. To run the database installer (this will parse the files in the `data` directory and upload them to the database):
```
cd .\installer\
python .\installer.py
```
10. Enter your username (default is "root") and password (default is ""). If the database installs successfuly you should see
```
Please enter a username:
root
Please enter a password:

Tables successfully created.
Records successfully parsed and uploaded to database.
```
11. To run the command-line interface tool for CRUD capabilities:
```
python .\main.py
```
12. If the tool starts successfully you should see something like this:
```
Please enter a username:
root
Please enter a password:

Would you like to create, read, update, or delete?
(Type exit to leave)
```

## Product CRUD Examples

Reading products:
```
Would you like to create, read, update, or delete?
(Type exit to leave)
read

Would you like to read customers, products, or transactions?
(Type exit to leave)
products
  Product ID  Name                         Price
------------  ---------------------------  -------
           1  Large Chocolate Chip Cookie  $ 3.99
           2  Large M&M Cookie             $ 3.99
           3  Large Peanut Butter Cookie   $ 3.99
           4  12-oz Frappuccino            $ 6.50
           5  8-oz Frappuccino             $ 5.99
           6  12-oz Cappuccino             $ 6.50
           7  8-oz Cappuccino              $ 5.99
           8  12-oz Iced Latte             $ 6.50
           9  8-oz Iced Latte              $ 5.99
          10  Croissant                    $ 1.99
          11  Bagel                        $ 1.99
          12  Banana Bread Muffin          $ 1.99
          13  Breakfast Sandwich           $ 4.99
          14  Glazed Donut                 $ 1.99
          15  Large Oatmeal Raisin Cookie  $ 3.99
          16  Apple Fritter                $ 2.99
          17  Large Sugar Cookie           $ 3.99
          18  Chocolate Cupcake            $ 2.99
          19  Strawberry Cupcake           $ 2.99
```

Creating a new product:
```
Would you like to create, read, update, or delete?
(Type exit to leave)
create

Would you like to create a customer, product, or transaction?
(Type exit to leave)
product
Enter a product name
Dark Chocolate Cookie
Enter a product price
3.99
Addition successful.
```
Reading products again shows the newly added product:
```
Would you like to read customers, products, or transactions?
(Type exit to leave)
products
  Product ID  Name                         Price
------------  ---------------------------  -------
           1  Large Chocolate Chip Cookie  $ 3.99
           2  Large M&M Cookie             $ 3.99
           3  Large Peanut Butter Cookie   $ 3.99
           4  12-oz Frappuccino            $ 6.50
           5  8-oz Frappuccino             $ 5.99
           6  12-oz Cappuccino             $ 6.50
           7  8-oz Cappuccino              $ 5.99
           8  12-oz Iced Latte             $ 6.50
           9  8-oz Iced Latte              $ 5.99
          10  Croissant                    $ 1.99
          11  Bagel                        $ 1.99
          12  Banana Bread Muffin          $ 1.99
          13  Breakfast Sandwich           $ 4.99
          14  Glazed Donut                 $ 1.99
          15  Large Oatmeal Raisin Cookie  $ 3.99
          16  Apple Fritter                $ 2.99
          17  Large Sugar Cookie           $ 3.99
          18  Chocolate Cupcake            $ 2.99
          19  Strawberry Cupcake           $ 2.99
          20  Dark Chocolate Cookie        $ 3.99
```
Updating the price on the new product:
```
Would you like to create, read, update, or delete?
(Type exit to leave)
update

Would you like to update a customer, product, or transaction?
(Type exit to leave)
product

Enter the id of the product you would like to update
20

Enter a product name
(Press enter to skip)


Enter a product price
(Press enter to skip)
2.99
Update successful.
```
The product's price was successfully updated:
```
  Product ID  Name                         Price
------------  ---------------------------  -------
           1  Large Chocolate Chip Cookie  $ 3.99
           2  Large M&M Cookie             $ 3.99
           3  Large Peanut Butter Cookie   $ 3.99
           4  12-oz Frappuccino            $ 6.50
           5  8-oz Frappuccino             $ 5.99
           6  12-oz Cappuccino             $ 6.50
           7  8-oz Cappuccino              $ 5.99
           8  12-oz Iced Latte             $ 6.50
           9  8-oz Iced Latte              $ 5.99
          10  Croissant                    $ 1.99
          11  Bagel                        $ 1.99
          12  Banana Bread Muffin          $ 1.99
          13  Breakfast Sandwich           $ 4.99
          14  Glazed Donut                 $ 1.99
          15  Large Oatmeal Raisin Cookie  $ 3.99
          16  Apple Fritter                $ 2.99
          17  Large Sugar Cookie           $ 3.99
          18  Chocolate Cupcake            $ 2.99
          19  Strawberry Cupcake           $ 2.99
          20  Dark Chocolate Cookie        $ 2.99
```
Deleting the new product:
```
Would you like to create, read, update, or delete?
(Type exit to leave)
delete

Would you like to delete a customer, product, or transaction?
(Type exit to leave)
product
Enter the id of the product you would like to delete
20
Deletion successful.
```
The product was successfully deleted:
```
  Product ID  Name                         Price
------------  ---------------------------  -------
           1  Large Chocolate Chip Cookie  $ 3.99
           2  Large M&M Cookie             $ 3.99
           3  Large Peanut Butter Cookie   $ 3.99
           4  12-oz Frappuccino            $ 6.50
           5  8-oz Frappuccino             $ 5.99
           6  12-oz Cappuccino             $ 6.50
           7  8-oz Cappuccino              $ 5.99
           8  12-oz Iced Latte             $ 6.50
           9  8-oz Iced Latte              $ 5.99
          10  Croissant                    $ 1.99
          11  Bagel                        $ 1.99
          12  Banana Bread Muffin          $ 1.99
          13  Breakfast Sandwich           $ 4.99
          14  Glazed Donut                 $ 1.99
          15  Large Oatmeal Raisin Cookie  $ 3.99
          16  Apple Fritter                $ 2.99
          17  Large Sugar Cookie           $ 3.99
          18  Chocolate Cupcake            $ 2.99
          19  Strawberry Cupcake           $ 2.99
```