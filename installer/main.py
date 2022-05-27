from sys import stderr
from parser import parse_persons, parse_customers, parse_products, find_person, parse_transactions, find_customer, find_product
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, InterfaceError

from database import StoreDatabase, Persisted, Product, Address, Person, Customer, Transaction, ProductTransaction


def already_has_data(session):
    return any(session.query(table).first() is not None for table in Persisted.metadata.sorted_tables)


def add_parsed_data(session):
    lst_persons = parse_persons("Persons.dat")
    lst_customers = parse_customers("Customers.dat")
    lst_transactions = parse_transactions("Transactions.dat")
    lst_products = parse_products("Products.dat")

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
    try:
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
        url = StoreDatabase.construct_mysql_url(authority, port, database_name, username, password)
        store_database = StoreDatabase(url)
        store_database.ensure_tables_exist()
        print('Tables successfully created.')
        session = store_database.create_session()
        if already_has_data(session):
            print('Not creating records because some already exist.')
        else:
            add_parsed_data(session)
            session.commit()
            print('Records successfully parsed and uploaded to database.')
    except InterfaceError:
        print(f'Cannot connect to database! Did you type the authority/port correctly?\nAuthority: {authority}, Port: {port}', file=stderr)
        exit(1)
    except ProgrammingError:
        print(f'Unknown database name! Make sure to create a database named "{database_name}".\nIf you typed the database name correctly then double check your credentials!', file=stderr)
        exit(1)
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
