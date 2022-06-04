from sqlalchemy.ext.declarative import declarative_base
from parser import parse_persons, parse_customers, parse_products, find_person, parse_transactions, find_customer, find_product
from datamodels import Person, Customer, Product, Address, ProductTransaction, Transaction
from database import connect_to_database, Persisted

def already_has_data(session):
    return any(session.query(table).first() is not None for table in Persisted.metadata.sorted_tables)


def add_parsed_data(session):
    lst_persons = parse_persons("../data/Persons.dat")
    lst_customers = parse_customers("../data/Customers.dat")
    lst_transactions = parse_transactions("../data/Transactions.dat")
    lst_products = parse_products("../data/Products.dat")

    for product in lst_products:
        product.data_model = Product(name=product.name, price=product.price)
        session.add(product.data_model)

    for person in lst_persons:
        person.address.data_model = Address(address=person.address.address, city=person.address.city, state=person.address.state, zip=person.address.zip, country=person.address.country)
        session.add(person.address.data_model)

    for customer in lst_customers:
        customer.address.data_model = Address(address=customer.address.address, city=customer.address.city, state=customer.address.state, zip=customer.address.zip, country=customer.address.country)
        session.add(customer.address.data_model)

    session.flush()

    for person in lst_persons:
        address_id = person.address.data_model.id
        emails = ""
        for email in person.email:
            emails += email + "|"
        emails[0:len(email) - 2]
        person.data_model = Person(first_name=person.first_name, last_name=person.last_name, address_id=address_id, email=emails)
        session.add(person.data_model)

    session.flush()

    for customer in lst_customers:
        address_id = customer.address.data_model.id
        person_id = find_person(lst_persons, customer.person_id).data_model.id
        customer.data_model = Customer(type=customer.type, company=customer.company, person_id=person_id, address_id=address_id)
        session.add(customer.data_model)
    
    session.flush()

    for transaction in lst_transactions:
        customer_id = find_customer(lst_customers, transaction.customer_id).data_model.id
        transaction.data_model = Transaction(customer_id=customer_id, date=transaction.date)
        session.add(transaction.data_model)
        

    session.flush()

    for transaction in lst_transactions:
        for product in transaction.lst_products:
            product_id = find_product(lst_products, product).data_model.id
            session.add(ProductTransaction(product_id=product_id, transaction_id=transaction.data_model.id))

def main():
    # Prompts for getting database connection information
    print('Please enter an authority:')
    authority = input()
    print('Please enter a port:')
    port = int(input())
    print('Please enter a database name:')
    database_name = input()
    print('Please enter a username:')
    username = input()
    print('Please enter a password:')
    password = input()
    session = connect_to_database(authority, port, database_name, username, password)
    print('Tables successfully created.')
    if already_has_data(session):
        print('Not creating records because some already exist.')
    else:
        add_parsed_data(session)
        session.commit()
        print('Records successfully parsed and uploaded to database.')

if __name__ == '__main__':
    main()
