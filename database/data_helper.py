from database.database import connect_to_database
from database.data_models import Customer, Person, Product, Transaction, ProductTransaction
from sqlalchemy.exc import ProgrammingError

class DataHelper:
  def __init__(self, username, password):
    self.session = connect_to_database('localhost', '3306', 'store', username, password)

  def customers_getone(self, customer_id):
    customer = self.session.query(Customer).filter(Customer.id == customer_id).first()
    if customer != None:
      customer.success = True
    else:
      customer = Customer(success=False, message="A customer with customer ID " + str(customer_id) + " does not exist.")
    return customer

  def persons_getone(self, person_id):
    person = self.session.query(Person).filter(Person.id == person_id).first()
    if person != None:
      person.success = True
    else:
      person = Person(success=False, message="A person with person ID " + str(person_id) + " does not exist.")
    return person

  def products_getone(self, product_id):
    product = self.session.query(Product).filter(Product.id == product_id).first()
    if product != None:
      product.success = True 
    else:
      product = Product(success=False, message="A product with product ID " + str(product_id) + " does not exist.")
    return product

  def product_transaction_getone(self, transaction_id, product_id):
    product_transaction = self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id).filter(ProductTransaction.product_id == product_id).first() 
    if product_transaction != None:
      product_transaction.success = True
    else:
      product_transaction = ProductTransaction(success=False, message="A product ID of " + str(product_id) + " does not exist on transaction " + str(transaction_id) + ".") 
    return product_transaction

  def transactions_getone(self, transaction_id):
    transaction = self.session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction != None:
      transaction.success = True
    else:
      transaction = Transaction(success=False, message="A transaction with transaction ID " + str(transaction_id) + " does not exist.")
    return transaction

  def customers_save(self, customer):
    if customer.id == None:
      self.session.add(customer)
    self.session.commit()
    customer.success = True
    return customer

  def persons_save(self, person):
    if person.id == None:
      self.session.add(person)
    self.session.commit()
    person.success = True
    return person

  def products_save(self, product):
    if product.id == None:
      self.session.add(product)
    self.session.commit()
    product.success = True
    return product

  def product_transaction_save(self, product_transaction):
    if not self.product_transaction_getone(product_transaction.transaction_id, product_transaction.product_id).success:
      self.session.add(product_transaction)
    self.session.commit()
    product_transaction = self.product_transaction_getone(product_transaction.transaction_id, product_transaction.product_id)
    if product_transaction.success:
      product_transaction.success = True
    else:
      product_transaction.success = False
    return product_transaction

  def transactions_save(self, transaction):
    if transaction.id == None:
      self.session.add(transaction)
    self.session.commit()
    transaction.success = True
    return transaction

  def get_persons(self):
    return self.session.query(Person)

  def get_customers(self):
    return self.session.query(Customer)

  def get_products(self):
    return self.session.query(Product)

  def get_transactions(self):
    return self.session.query(Transaction)

  def get_products_by_transaction_id(self, transaction_id):
    product_transactions = self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id)
    lst_products = []
    for product_transaction in product_transactions:
      lst_products.append(self.products_getone(product_transaction.product_id))
    return lst_products

  def products_delete(self, product_id):
    product = self.products_getone(product_id)
    if product.success:
      self.session.query(Product).filter(Product.id == product_id).delete()
      self.session.commit()
    else:
      return Product(success=False, message=product.message)
    if not self.products_getone(product_id).success:
      return Product(success=True)
    else:
      return Product(success=False, message="An unknown error occurred.")

  def customers_delete(self, customer_id):
    customer = self.customers_getone(customer_id)
    if customer.success:
      self.session.query(Customer).filter(Customer.id == customer_id).delete()
      self.session.commit()
    else:
      return Customer(success=False, message=customer.message)
    if not self.customers_getone(customer_id).success:
      return Customer(success=True)
    else:
      return Customer(success=False, message="An unknown error occurred.")

  def persons_delete(self, person_id):
    person = self.persons_getone(person_id)
    if person.success:
      self.session.query(Person).filter(Person.id == person_id).delete()
      self.session.commit()
    else:
      return Person(success=False, message=person.message)
    if not self.persons_getone(person_id).success:
      return Person(success=True)
    else:
      return Person(success=False, message="An unknown error occurred.")

  def transactions_delete(self, transaction_id):
    transaction = self.transactions_getone(transaction_id)
    if transaction.success:
      self.session.query(Transaction).filter(Transaction.id == transaction_id).delete()
      self.session.commit()
    else:
      return Transaction(success=False, message=transaction.message)
    if not self.transactions_getone(transaction_id).success:
      return Transaction(success=True)
    else:
      return Transaction(success=False, message="An unknown error occurred.")

  def product_transactions_delete(self, transaction_id, product_id):
    product_transaction = self.product_transaction_getone(transaction_id, product_id)
    if product_transaction.success:
      self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id).filter(ProductTransaction.product_id == product_id).delete()
      self.session.commit()
    else:
      return ProductTransaction(success=False, message=product_transaction.message)
    if not self.transactions_getone(transaction_id).success:
      return ProductTransaction(success=True)
    else:
      return ProductTransaction(success=False, message="An unknown error occurred.")

  def close(self):
    self.session.close()