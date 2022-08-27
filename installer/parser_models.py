class Customer:
  def __init__(self, id, first_name, last_name, address, city, state, postal_code, country, email):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.address = address
    self.city = city
    self.state = state
    self.postal_code = postal_code
    self.country = country
    self.email = email

  def __str__(self):
    return "Customer " + self.id + " " + self.first_name + " " + self.last_name + " " + self.address + " " + self.city + " " + self.state + " " + self.postal_code + " " + self.country + " " + self.email

  def compare(self, customer):
    if self.last_name > customer.last_name:
      return 1
    elif self.last_name < customer.last_name:
      return -1
    else:
      return 0


class Product:
  def __init__(self, id, name, price):
    self.id = id
    self.name = name
    self.price = price
  
  def __str__(self):
    return "Product " + self.id + " " + self.name + " " + self.price

  def compare(self, product):
    if self.name > product.name:
      return 1
    elif self.name < product.name:
      return -1
    else:
      return 0


class Transaction:
  def __init__(self, id, customer, lst_products, date):
    self.id = id
    self.customer = customer
    self.lst_products = lst_products
    self.date = date
