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


class Product:
  def __init__(self, id, name, price):
    self.id = id
    self.name = name
    self.price = price
  
  def __str__(self):
    return "Product " + self.id + " " + self.name + " " + self.price


def parseAddress(full_address):
  address = full_address[0]
  city = full_address[1]
  state = full_address[2]
  zip = full_address[3] if full_address[3] is not None else ""
  country = full_address[4]
  return Address(address, city, state, zip, country)

def parsePersons(file_name):
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

def parseCustomers(file_name):
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

def parseProducts(file_name):
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

done = False
while not done:
  entry = input("Would you like to view Persons, Customers, or Products?\n(Type exit to leave)\n")
  if entry != "Persons" and entry != "Customers" and entry != "Products" and entry != "exit":
    print("Invalid input. Enter Persons, Customers, Products, or exit\n")
    continue
  elif entry == "exit":
    done = True
    continue
  else:
    print("")
    if entry == "Persons":
      for person in parsePersons("Persons.dat"):
        print(person)
    elif entry == "Customers":
      for customer in parseCustomers("Customers.dat"):
        print(customer)
    else:
      for product in parseProducts("Products.dat"):
        print(product)
    print("")
