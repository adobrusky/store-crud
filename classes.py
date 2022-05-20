class Person:
  def __init__(self, id, first_name, last_name, address, email):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.address = address
    self.email = email

  def __str__(self):
    emails = "Email: "
    for email in self.email:
      emails += email + ", "
    emails = emails[0:len(emails) - 3]
    return "Person " + self.id + " " + self.first_name + " " + self.last_name + " " + str(self.address) + " " + emails

  def compare(self, person):
    if self.last_name > person.last_name:
      return 1
    elif self.last_name < person.last_name:
      return -1
    else:
      return 0


class Address:
  def __init__(self, address, city, state, zip, country):
    self.address = address
    self.city = city
    self.state = state
    self.zip = zip
    self.country = country

  def __str__(self):
    return "Address " + self.address + " " + self.city + " " + self.state + " " + self.zip + " " + self.country


class Customer:
  def __init__(self, id, type, company, person_id, address):
    self.id = id
    self.type = type
    self.company = company
    self.person_id = person_id
    self.address = address

  def __str__(self):
    return "Customer " + self.id + " " + self.type + " " + self.company + " " + self.person_id + " " + str(self.address)

  def compare(self, customer):
    if self.company > customer.company:
      return 1
    elif self.company < customer.company:
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