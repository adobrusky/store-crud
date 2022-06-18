import sys
sys.path.append("..")
from parser import Parser
from database.data_models import Person, Customer, Product, ProductTransaction, Transaction
from database.database import connect_to_database, Persisted

def already_has_data(session):
    return any(session.query(table).first() is not None for table in Persisted.metadata.sorted_tables)


def add_parsed_data(session):
    data_parser = Parser("../data/Persons.dat", "../data/Customers.dat", "../data/Products.dat", "../data/Transactions.dat")

    for product in data_parser.lst_products:
        product.data_model = Product(name=product.name, price=product.price)
        session.add(product.data_model)

    session.flush()

    for person in data_parser.lst_persons:
        person.data_model = Person(first_name=person.first_name, last_name=person.last_name, address=person.address, city=person.city, state=person.state, zip=person.zip, country=person.country, email=person.email)
        session.add(person.data_model)

    session.flush()

    for customer in data_parser.lst_customers:
        person_id = data_parser.find_person(customer.person.id).data_model.id
        customer.data_model = Customer(type=customer.type, company=customer.company, person_id=person_id, address=customer.address, city=customer.city, state=customer.state, zip=customer.zip, country=customer.country)
        session.add(customer.data_model)
    
    session.flush()

    for transaction in data_parser.lst_transactions:
        customer_id = data_parser.find_customer(transaction.customer.id).data_model.id
        transaction.data_model = Transaction(customer_id=customer_id, date=transaction.date)
        session.add(transaction.data_model)
        

    session.flush()

    for transaction in data_parser.lst_transactions:
        for product in transaction.lst_products:
            product_id = data_parser.find_product(product).data_model.id
            session.add(ProductTransaction(product_id=product_id, transaction_id=transaction.data_model.id))

def main():
    # Prompts for getting database connection information
    print('Please enter a username:')
    username = input()
    print('Please enter a password:')
    password = input()
    session = connect_to_database("localhost", "3306", "store", username, password)
    print('Tables successfully created.')
    if already_has_data(session):
        print('Not creating records because some already exist.')
    else:
        add_parsed_data(session)
        session.commit()
        print('Records successfully parsed and uploaded to database.')

if __name__ == '__main__':
    main()
