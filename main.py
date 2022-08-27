from database.data_models import Product, Customer, Transaction
from database.data_helper import DataHelper
from tabulate import tabulate

def main():
  done = False
  print('Please enter a username:')
  username = input()
  print('Please enter a password:')
  password = input()
  data_helper = DataHelper(username, password)
  while not done:
    entry = input("Would you like to create, read, update, or delete?\n(Type exit to leave)\n").lower().strip()
    if entry != "create" and entry != "read" and entry != "update" and entry != "delete" and entry != "exit":
      print("Invalid input.\n")
      continue
    elif entry == "exit":
      done = True
      data_helper.close()
      continue
    else:
      print("")
      # If user wants to read
      if entry == "read":
        entry = input("Would you like to read customers, products, or transactions?\n(Type exit to leave)\n").lower().strip()
        # Read Customers
        if entry == "customers":
          lst_customers = data_helper.get_customers()
          customers_table = []
          for customer in lst_customers:
            customers_table.append([customer.id, customer.last_name + ", " + customer.first_name, customer.address, customer.city, customer.state, customer.postal_code, customer.country, customer.email])
          columns = ["Customer ID", "Full name", "Street address", "City", "State", "Postal Code", "Country", "Email"]
          print(tabulate(customers_table, headers=columns))
        # Read products
        elif entry == "products":
          lst_products = data_helper.get_products()
          products_table = []
          for product in lst_products:
            products_table.append([product.id, product.name, "$ {:,.2f}".format(float(product.price))])
          columns = ["Product ID", "Name", "Price"]
          print(tabulate(products_table, headers=columns))
        # Read transactions
        elif entry == "transactions":
          lst_transactions = data_helper.get_transactions()
          transactions_table = []
          for transaction in lst_transactions:
            product_ids = ""
            lst_products = data_helper.get_products_by_transaction_id(transaction.id)
            for i in range(0, len(lst_products)):
              product_ids += str(lst_products[i].id)
              if i < len(lst_products) - 1:
                product_ids += ", "
            transactions_table.append([transaction.id, transaction.customer_id, product_ids, transaction.date])
          columns = ["Transaction ID", "Customer ID", "Product ID(s)", "Date of Transaction"]
          print(tabulate(transactions_table, headers=columns))
        elif entry == "exit":
          done = True
          data_helper.close()
          continue
        else:
          print("Invalid input.\n")
        print("")
      # If user wants to create
      elif entry == "create":
        entry = input("Would you like to create a customer, product, or transaction?\n(Type exit to leave)\n").lower().strip()
        # Create products
        if entry == "product":
          name = input("Enter a product name\n").strip()
          price = input("Enter a product price\n").strip()
          product = data_helper.products_save(Product(name=name, price=price))
          if product.success:
            print("Addition successful.")
          else:
            print("Addition failed. " + product.message)
        # Create customers
        elif entry == "customer":
          first_name = input("Enter the customer's first name \n").strip()
          last_name = input("Enter the customer's last name\n").strip()
          address = input("Enter the customer's street address\n").strip()
          city = input("Enter the customer's city\n").strip()
          state = input("Enter customer's state\n").strip()
          country = input("Enter the customer's country\n").strip()
          postal_code = input("Enter the customer's postal code\n").strip()
          email = input("Enter the customer's email\n").strip()
          customer = data_helper.customers_save(Customer(first_name=first_name, last_name=last_name, address=address, city=city, state=state, postal_code=postal_code, country=country, email=email))
          if customer.success:
            print("Addition successful.")
          else:
            print("Addition failed. " + customer.message)
        # Create transactions
        elif entry == "transaction":
          customer_id = input("Enter the transactions's customer ID\n").strip()
          date = input("Enter the transaction's date (yyyy-mm-dd)\n").strip()
          product_ids = input("Enter the transaction's product ID(s) as a comma separated list\n").strip()
          lst_products = []
          if product_ids != "":
            lst_products = products.split(",")
          transaction = data_helper.transactions_save(Transaction(customer_id=customer_id, date=date), lst_products)
          if transaction.success:
            print("Addition successful.")
          else:
            print("Addition failed. " + transaction.message)
        elif entry == "exit":
          done = True
          data_helper.close()
          continue
        else:
          print("Invalid input.\n")
        print("")
      # If user wants to update
      elif entry == "update":
        entry = input("Would you like to update a customer, product, or transaction?\n(Type exit to leave)\n").lower().strip()
        # Update products
        if entry == "product":
          id = input("\nEnter the id of the product you would like to update\n").strip()
          existing = data_helper.products_getone(id)
          if existing.success:
            name = input("\nEnter a product name\n(Press enter to skip)\n").strip()
            price = input("\nEnter a product price\n(Press enter to skip)\n").strip()
            if name != "":
              existing.name = name
            if price != "":
              existing.price = price
            data_helper.products_save(existing)
            print("Update successful.")
          else:
            print("Update failed. " + existing.message)
        # Update customers
        elif entry == "customer":
          id = input("Enter the id of the customer you would like to update\n").strip()
          existing = data_helper.customers_getone(id)
          if existing.success:
            first_name = input("Enter the customer's first name\n(Press enter to skip)\n").strip()
            last_name = input("Enter the customer's last name\n(Press enter to skip)\n").strip()
            address = input("Enter the customer's address\n(Press enter to skip)\n").strip()
            city = input("Enter the customer's city\n(Press enter to skip)\n").strip()
            state = input("Enter customer's state\n(Press enter to skip)\n").strip()
            country = input("Enter the customer's country\n(Press enter to skip)\n").strip()
            postal_code = input("Enter the customer's postal code\n(Press enter to skip)\n").strip()
            email = input("Enter the customer's email\n(Press enter to skip)\n").strip()
            if first_name != "":
              existing.first_name = first_name
            if last_name != "":
              existing.last_name = last_name
            if address != "":
              existing.address = address
            if city != "":
              existing.city = city
            if state != "":
              existing.state = state
            if country != "":
              existing.country = country
            if postal_code != "":
              existing.postal_code = postal_code
            if email != "":
              existing.email = email
            data_helper.customers_save(existing)
            print("Update successful.")
          else:
            print("Update failed. " + existing.message)
        # Update transactions
        elif entry == "transaction":
          id = input("Enter the id of the transaction you would like to update\n").strip()
          existing = data_helper.transactions_getone(id)
          if existing.success:
            customer_id = input("Enter the transaction's customer ID\n(Press enter to skip)\n").strip()
            date = input("Enter the transaction's date (yyyy-mm-dd)\n(Press enter to skip)\n").strip()
            products = input("Enter the transaction's product ID(s) as a comma separated list\n(Press enter to skip)\n").strip()
            if customer_id != "":
              existing.customer_id = customer_id
            if date != "":
              existing.date = date
            lst_products = []
            if products != "":
              lst_products = products.split(",")
            transaction = data_helper.transactions_save(existing, lst_products)
            if not transaction.success:
              print("Update failed. " + transaction.message)
              break
            print("Update successful.")
          else:
            print("Update failed. " + existing.message)
        elif entry == "exit":
          done = True
          data_helper.close()
          continue
        else:
          print("Invalid input.\n")
        print("")
      # If user wants to delete
      elif entry == "delete":
        entry = input("Would you like to delete a customer, product, or transaction?\n(Type exit to leave)\n").lower().strip()
        if entry == "product":
          id = input("Enter the id of the product you would like to delete\n").strip()
          product = data_helper.products_delete(id)
          if product.success:
            print("Deletion successful.")
          else:
            print("Deletion failed. " + product.message)
        elif entry == "customer":
          id = input("Enter the id of the customer you would like to delete\n").strip()
          customer = data_helper.customers_delete(id)
          if customer.success:
            print("Deletion successful.")
          else:
            print("Deletion failed. " + customer.message)
        elif entry == "transaction":
          id = input("Enter the id of the transaction you would like to delete\n").strip()
          transaction = data_helper.transactions_delete(id)
          if transaction.success:
            print("Deletion successful.")
          else:
            print("Deletion failed. " + transaction.message)
        elif entry == "exit":
          done = True
          data_helper.close()
          continue
        else:
          print("Invalid input.\n")
        print("")
          
if __name__ == '__main__':
  main()