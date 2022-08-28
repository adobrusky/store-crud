from parser_models import Customer, Product, Transaction
from datetime import datetime

class Parser:
  def __init__(self, customers, products, transactions):
    self.lst_customers = self.parse_customers(customers)
    self.lst_products = self.parse_products(products)
    self.lst_transactions = self.parse_transactions(transactions)

  def find_customer(self, customer_id):
    for customer in self.lst_customers:
      if customer.id == customer_id:
        return customer

  def find_product(self, product_id):
    for product in self.lst_products:
      if product.id == product_id:
        return product

  def parse_customers(self, file_name):
    """Parses file and returns list of Customer objects"""
    customers = open(file_name, "r")
    lst_customers = []
    for line in customers:
      split_line = line.split(";")
      id = split_line[0].strip()
      full_name = split_line[1].split(",")
      first_name = full_name[1].strip()
      last_name = full_name[0].strip()
      full_address = split_line[2].split(",")
      address = full_address[0].strip()
      city = full_address[1].strip()
      state = full_address[2].strip()
      postal_code = full_address[3].strip() if full_address[3] is not None else ""
      country = full_address[4].strip()
      email = ""
      if len(split_line) == 4:
        email = split_line[3]
      email = email.strip('\n')
      lst_customers.append(Customer(id, first_name, last_name, address, city, state, postal_code, country, email))
    return lst_customers

  def parse_products(self, file_name):
    """Parses file and returns list of Product objects"""
    products = open(file_name, "r")
    lst_products = []
    for line in products:
      split_line = line.split(";")
      id = split_line[0].strip()
      name = split_line[1].strip()
      price = split_line[2].strip()
      lst_products.append(Product(id, name, price))
    return lst_products

  def parse_transactions(self, file_name):
    """Parses file and returns list of Transaction objects"""
    transactions = open(file_name, "r")
    lst_transactions = []
    for line in transactions:
      split_line = line.split(";")
      id = split_line[0].strip()
      customer = self.find_customer(split_line[1].strip())
      lst_products = {}
      for product in split_line[2].split(","):
        lst_products[product.split(":")[0].strip()] = product.split(":")[1].strip()
      transaction_date = datetime.strptime(split_line[3].strip(), '%Y-%m-%d')
      lst_transactions.append(Transaction(id, customer, lst_products, transaction_date))
    return lst_transactions 