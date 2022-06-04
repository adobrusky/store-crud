import database.datamodels
import database.database
from tabulate import tabulate

done = False
session = database.database.connect_to_database('localhost', '3306', 'store', 'root', '')
while not done:
  entry = input("Would you like to create, read, update, or delete?\n(Type exit to leave)\n").lower()
  if entry != "create" and entry != "read" and entry != "update" and entry != "delete" and entry != "exit":
    print("Invalid input. Enter create, read, update, delete, or exit\n")
    continue
  elif entry == "exit":
    done = True
    session.commit()
    continue
  else:
    print("")

    if entry == "read":
      entry = input("Would you like to read persons, products, customers, or transactions?\n(Type exit to leave)\n").lower()
      if entry == "persons":
        lst_persons = session.query(database.datamodels.Person)
        persons_table = []
        for person in lst_persons:
          emails = ""
          for email in person.email.split("|"):
              emails += email + ", "
          emails = emails[0:len(emails) - 2]
          address = session.query(database.datamodels.Address).filter(database.datamodels.Address.id == person.address_id).first()
          persons_table.append([person.id, person.last_name + ", " + person.first_name, address.address, address.city, address.state, address.zip, address.country, emails])
        columns = ["Person ID", "Full name", "Street address", "City", "State", "Zip", "Country", "Email"]
        print(tabulate(persons_table, headers=columns))
      if entry == "customers":
        lst_customers = session.query(database.datamodels.Customer)
        customers_table = []
        for customer in lst_customers:
          person = session.query(database.datamodels.Person).filter(database.datamodels.Person.id == customer.person_id).first()
          address = session.query(database.datamodels.Customer).filter(database.datamodels.Address.id == customer.address_id).first()
          customers_table.append([customer.id, customer.type, customer.company, person.last_name + ", " + person.first_name, address.address, address.city, address.state, address.zip, address.country])
        columns = ["Customer ID", "Type", "Company", "Full name", "Street address", "City", "State", "Zip", "Country"]
        print(tabulate(customers_table, headers=columns))
      if entry == "products":
        lst_products = session.query(database.datamodels.Product)
        products_table = []
        for product in lst_products:
          products_table.append([product.id, product.name, "$ {:,.2f}".format(float(product.price))])
        columns = ["Product ID", "Name", "Price"]
        print(tabulate(products_table, headers=columns))
