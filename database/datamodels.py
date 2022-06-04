from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from database.database import Persisted

class Address(Persisted):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String(256), nullable=False)
    city = Column(String(256), nullable=False)
    state = Column(String(256), nullable=False)
    zip = Column(String(256), nullable=False)
    country = Column(String(256), nullable=False)
    person = relationship('Person', back_populates='address', uselist=False)
    customer = relationship('Customer', back_populates='address', uselist=False)

class Person(Persisted):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id', ondelete='CASCADE'), nullable=False)
    email = Column(String(256), nullable=False)
    customer = relationship('Customer', back_populates='person', uselist=False)
    address = relationship('Address', back_populates='person')


class Customer(Persisted):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    type = Column(String(1), nullable=False)
    company = Column(String(256), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete='CASCADE'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id', ondelete='CASCADE'), nullable=False)
    address = relationship('Address', back_populates='customer')
    person = relationship('Person', back_populates='customer')
    transaction = relationship('Transaction', back_populates='customer')


class Product(Persisted):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    product_transactions = relationship('ProductTransaction', uselist=True, back_populates='product')
    transactions = relationship('Transaction', uselist=True, secondary='product_transactions', overlaps='product_transactions')


class Transaction(Persisted):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, server_default=func.now())
    customer = relationship('Customer', back_populates='transaction')
    product_transactions = relationship('ProductTransaction', uselist=True, back_populates='transaction', overlaps='transactions')
    products = relationship('Product', uselist=True, secondary='product_transactions', overlaps='product_transactions,transactions')

class ProductTransaction(Persisted):
    __tablename__ = 'product_transactions'
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id', ondelete='CASCADE'), primary_key=True)
    product = relationship('Product', back_populates='product_transactions', overlaps='products,transactions')
    transaction = relationship('Transaction', back_populates='product_transactions', overlaps='products,transactions')