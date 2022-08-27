from database.database import connect_to_database
from database.data_models import Customer, Product, Transaction, ProductTransaction

class DataHelper:
  def __init__(self, username, password):
    self.session = connect_to_database('localhost', '3306', 'store', username, password)
  
  def close(self):
    self.session.close()

  # Used for updates to patch the old object with the new object's information
  def delta_patch(self, existing, new):
    for attr, value in new.__dict__.items():
      if attr != "id" and attr != "_sa_instance_state" and (type(existing).__name__ == "Transaction" and attr != "products"):
        setattr(existing, attr, value)

  # Check to make sure that the passed in required fields are not None in the object
  def validate_required(self, object, required_fields):
    missing = []
    for required in required_fields:
      if self.is_null_or_whitespace(getattr(object, required)):
        missing.append(required)
    return missing

  def is_null_or_whitespace(self, string):
    if string is None or len(str(string).strip()) == 0:
      return True
    else:
      return False

  #region Get one

  def customers_getone(self, customer_id):
    customer = self.session.query(Customer).filter(Customer.id == customer_id).first()
    if customer != None:
      customer.success = True
    else:
      customer = Customer(success=False, message="A customer with customer ID " + str(customer_id) + " does not exist.")
    return customer

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

  #endregion

  #region Save (create/update) methods

  def customers_save(self, customer):
    try:
      required_fields = ["first_name", "last_name", "address", "city", "country"]
      invalid = []
      missing = self.validate_required(customer, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      # Postal code and state validation for USA and Canada
      if customer.country.upper() == "USA" or customer.country.upper() == "CANADA":
        if self.is_null_or_whitespace(customer.postal_code):
          invalid.append("Postal code is required for USA and Canada.")
        if self.is_null_or_whitespace(customer.state):
          invalid.append("State is required for USA and Canada.")
      else:
        if self.is_null_or_whitespace(customer.postal_code):
          customer.postal_code = ""
        if self.is_null_or_whitespace(customer.state):
          customer.state = ""
      if self.is_null_or_whitespace(customer.email):
        customer.email = ""
      elif len(customer.email) > 0 and "@" not in customer.email:
        invalid.append("Email is invalid.")
      if len(invalid) > 0:
        raise ValueError(" ".join(invalid))
      if customer.id is None:
        self.session.add(customer)
      else:
        existing = self.customers_getone(customer.id)
        self.delta_patch(existing, customer)
      self.session.commit()
      customer.success = True
      return customer
    except Exception as ex:
      customer.success = False
      customer.message = str(ex)
      return customer

  def products_save(self, product):
    try:
      required_fields = ["price", "name"]
      missing = self.validate_required(product, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      if product.id is None:
        self.session.add(product)
      else:
        existing = self.products_getone(product.id)
        self.delta_patch(existing, product)
      self.session.commit()
      product.success = True
      return product
    except Exception as ex:
      product.success = False
      product.message = str(ex)
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

  def transactions_save(self, transaction, products):
    try:
      required_fields = ["customer_id", "date"]
      invalid = []
      missing = self.validate_required(transaction, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      if not self.customers_getone(transaction.customer_id).success:
        invalid.append("A customer with customer ID of " + str(transaction.customer_id) + " does not exist.")
      if len(invalid) > 0:
        raise ValueError(" ".join(invalid))
      if transaction.id is None:
        self.session.add(transaction)
      else:
        existing = self.transactions_getone(transaction.id)
        self.delta_patch(existing, transaction)
      self.session.commit()
      transaction.success = True
      # If the transaction save was successful then update all product transactions
      for existing_product in self.get_products_by_transaction_id(transaction.id):
        self.product_transactions_delete(transaction.id, existing_product.id)
      if products is not None:
        for product in products:
          self.product_transaction_save(ProductTransaction(transaction_id=transaction.id, product_id=product))
      return transaction
    except ValueError as ex:
      transaction.success = False
      transaction.message = str(ex)
      return transaction

  #endregion

  #region Get all methods

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

  #endregion

  #region Delete methods

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
      return Product(success=False, message="Deletion failed.")

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
      return Customer(success=False, message="Deletion failed.")

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
      return Transaction(success=False, message="Deletion failed.")

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
      return ProductTransaction(success=False, message="Deletion failed.")

  #endregion