from classes import Person, Address, Customer, Product, Transaction
from datetime import datetime, date

def find_person(lst_persons, person_id):
  for person in lst_persons:
    if person.id == person_id:
      return person

def find_customer(lst_customers, customer_id):
  for customer in lst_customers:
    if customer.id == customer_id:
      return customer

def find_product(lst_products, product_id):
  for product in lst_products:
    if product.id == product_id:
      return product

def parse_address(full_address):
  address = full_address[0]
  city = full_address[1]
  state = full_address[2]
  zip = full_address[3] if full_address[3] is not None else ""
  country = full_address[4]
  return Address(address, city, state, zip, country)

def parse_persons(file_name):
  """Parses file and returns list of Person objects"""
  persons = open(file_name, "r")
  lst_persons = []
  for line in persons:
    split_line = line.split(";")
    id = split_line[0]
    full_name = split_line[1].split(",")
    first_name = full_name[1].strip()
    last_name = full_name[0].strip()
    full_address = split_line[2].split(",")
    address = full_address[0]
    city = full_address[1]
    state = full_address[2]
    zip = full_address[3] if full_address[3] is not None else ""
    country = full_address[4]
    emails = []
    if len(split_line) == 4:
      for email in split_line[3].split(","):
            emails.append(email)
    lst_persons.append(Person(id, first_name, last_name, Address(address, city, state, zip, country), emails))
  return lst_persons

def parse_customers(file_name):
  """Parses file and returns list of Customer objects"""
  customers = open(file_name, "r")
  lst_customers = []
  for line in customers:
    split_line = line.split(";")
    id = split_line[0]
    type = split_line[1]
    company = split_line[2]
    person_id = split_line[3]
    full_address = split_line[4].split(",")
    address = full_address[0]
    city = full_address[1]
    state = full_address[2]
    zip = full_address[3] if full_address[3] is not None else ""
    country = full_address[4]
    lst_customers.append(Customer(id, type, company, person_id, Address(address, city, state, zip, country)))
  return lst_customers

def parse_products(file_name):
  """Parses file and returns list of Product objects"""
  products = open(file_name, "r")
  lst_products = []
  for line in products:
    split_line = line.split(";")
    id = split_line[0]
    name = split_line[1]
    price = split_line[2]
    lst_products.append(Product(id, name, price))
  return lst_products

def parse_transactions(file_name):
  """Parses file and returns list of Transaction objects"""
  transactions = open(file_name, "r")
  lst_transactions = []
  for line in transactions:
    split_line = line.split(";")
    id = split_line[0]
    customer_id = split_line[1]
    lst_products = []
    for product in split_line[2].split(","):
      lst_products.append(product)
    transaction_date = datetime.strptime(split_line[3][0:len(split_line[3]) - 1], '%Y-%m-%d')
    lst_transactions.append(Transaction(id, customer_id, lst_products, transaction_date))
  return lst_transactions 

# done = False
# lst_persons = parse_persons("Persons.dat")
# lst_customers = parse_customers("Customers.dat")
# lst_products = parse_products("Products.dat")

# while not done:
#   entry = input("Would you like to view Persons, Customers, or Products?\n(Type exit to leave)\n")
#   if entry != "Persons" and entry != "Customers" and entry != "Products" and entry != "exit":
#     print("Invalid input. Enter Persons, Customers, Products, or exit\n")
#     continue
#   elif entry == "exit":
#     done = True
#     continue
#   else:
#     print("")
#     if entry == "Persons":
#       persons_table = []
#       for person in lst_persons:
#         emails = ""
#         for email in person.email:
#           emails += email + ", "
#         emails = emails[0:len(emails) - 3]
#         persons_table.append([person.id, person.last_name + ", " + person.first_name, person.address.address, person.address.city, person.address.state, person.address.zip, person.address.country, emails])
#       columns = ["Person ID", "Full name", "Street address", "City", "State", "Zip", "Country", "Email"]
#       print(tabulate(persons_table, headers=columns))
#     elif entry == "Customers":
#       customers_table = []
#       for customer in lst_customers:
#         person = find_person(lst_persons, customer.person_id)
#         customers_table.append([customer.id, customer.type, customer.company, person.last_name + ", " + person.first_name, customer.address.address, customer.address.city, customer.address.state, customer.address.zip, customer.address.country])
#       columns = ["Customer ID", "Type", "Company", "Full name", "Street address", "City", "State", "Zip", "Country"]
#       print(tabulate(customers_table, headers=columns))
#     else:
#       products_table = []
#       for product in lst_products:
#         products_table.append([product.id, product.name, "$ {:,.2f}".format(float(product.price))])
#       columns = ["Product ID", "Name", "Price"]
#       print(tabulate(products_table, headers=columns))
#     print("")
