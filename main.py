# Customer Relationship Management (CRM)

import sqlite3
import hashlib
import pandas as pd

def create_table():
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()

    # Create table for user
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL
    )
    ''')

    # Create table for product
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_type TEXT NOT NULL,
        project_date DATE,
        project_rating INTEGER
    )
    ''')

    # Create table for support
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS support (
        ticket_id INTEGER ,
        project_id INTEGER,
        ticket_date DATE,
        ticket_status BOOLEAN,    
        ticket_manager TEXT NOT NULL,   
        FOREIGN KEY (project_id) REFERENCES product(project_id),
        FOREIGN KEY (ticket_status) REFERENCES ticket(ticket_status),
        FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id),
        FOREIGN KEY (ticket_date) REFERENCES ticket(ticket_date)
    )
    ''')

    # Create table for customer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_no INT NOT NULL,
        purchase_hist INTEGER,
        ticket_hist INTEGER,
        payment_type TEXT NOT NULL,
        FOREIGN KEY (purchase_hist) REFERENCES product(product_id),
        FOREIGN KEY (ticket_hist) REFERENCES support(ticket_id)
    )
    ''')

    # Create table for tickets
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticket (
        customer_id INTEGER,
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        ticket_date DATE,
        ticket_status BOOLEAN,
        ticket_reason TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
        FOREIGN KEY (project_id) REFERENCES product(project_id)            
    )
    ''')

    conn.commit()
    conn.close()


# User authentication
def login(username, password):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha224(password.encode()).hexdigest()   # hashed password makes the security stronger
    cursor.execute(f"SELECT id FROM user WHERE username = ? AND hashed_password = ?", (username, hashed_password))
    rows = cursor.fetchone()
    conn.close()

    if rows:
        return True
            
    else:
        return False


# add new user
def add_user(username, password):
    conn = sqlite3.connect('crm.db') 
    cursor = conn.cursor()
    hashed_password = hashlib.sha224(password.encode()).hexdigest()
    cursor.execute('INSERT INTO user (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    print(f"User added successfully.")


# add new customer
def add_customer(contact_no, purchase_hist, ticket_hist, payment_type):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customer (contact_no, purchase_hist, ticket_hist, payment_type) VALUES (?, ?, ?, ?)', 
                   (contact_no, purchase_hist, ticket_hist, payment_type))
    conn.commit()
    conn.close()
    print(f"Customer added successfully.")


# add new product
def add_product(project_type, project_date, project_rating):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO product (project_type, project_date, project_rating) VALUES (?, ?, ?)', 
                   (project_type, project_date, project_rating))
    conn.commit()
    print(f"Product added successfully.")


# add new support
def add_support(ticket_manager, ticket_date, ticket_status):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO support (ticket_manager, ticket_date, ticket_status) VALUES (?, ?, ?)', 
                   (ticket_manager, ticket_date, ticket_status))
    conn.commit()
    print(f"Support added successfully.")

# add new ticket
def add_ticket(ticket_date, ticket_status, ticket_reason):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ticket (ticket_date, ticket_status, ticket_reason) VALUES ( ?, ?, ?)', 
                   (ticket_date, ticket_status, ticket_reason))
    add_support()
    conn.commit()
    print(f"Ticket added successfully")


# fetch data by specifying the table name
def fetch_data(table_name):
    def decorator(func):
        def wrapper():
            conn = sqlite3.connect('crm.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            conn.close()
            return func(rows)
        return wrapper 
    return decorator


# print customer table
@fetch_data(table_name="customer")
def print_customer(rows):
    if rows:
        for row in rows:
            print(f"customer_id: {row[0]}, contact_no: {row[1]}, purchase_hist: {row[2]}, ticket_hist: {row[3]}, payment_type: {row[4]} ")
    else:
        print("No customer found.")


# export customer data to csv file
@fetch_data(table_name="customer")
def customer_to_csv(rows):
    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["customer_id", "contact_no", "purchase_hist", "ticket_hist", "payment_type"]
        df.to_csv('customer_data.csv', index=False)
        print("Customer data successsfully exported to customer_data.csv")
    else:
        print("No customer data to export.")


# print product table
@fetch_data(table_name="product")
def print_product(rows):
    if rows:
        for row in rows:
            print(f"project_id: {row[0]}, project_type: {row[1]}, project_date: {row[2]}, project_rating: {row[3]}")
    else:
        print("No product found.")


# export product data to csv file
@fetch_data(table_name="product")
def product_to_csv(rows):
    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["project_id", "project_type", "project_date", "project_rating"]
        df.to_csv('product_data.csv', index=False)
        print("Product data successsfully exported to product_data.csv")
    else:
        print("No product data to export.")


# print support table
@fetch_data(table_name="support")
def print_support(rows):
    if rows:
        for row in rows:
            print(f"ticket_id: {row[0]}, project_type: {row[1]}, ticket_date: {row[2]}, ticket_status: {row[3]}, ticket_manager: {row[4]}")
    else:
        print("No support found.")


# export support data to csv file
@fetch_data(table_name="support")
def support_to_csv(rows):
    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["ticket_id", "project_type", "ticket_date", "ticket_status"]
        df.to_csv('support_data.csv', index=False)
        print("Support data successsfully exported to support_data.csv")
    else:
        print("No support data to export.")


def view_customer_given_payment_type(payment_type):
    print(payment_type)
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer WHERE payment_type = ?', (payment_type,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"customer_id: {row[0]}, contact_no: {row[1]}, purchase_hist: {row[2]}, ticket_hist: {row[3]}, payment_type: {row[4]} ")
    else:
        print("No customer found.")


def main():
    create_table()
    username = input("Enter username: ")
    password = input ("Enter password: ")
    #change to False for actual pswd
    if login(username, password) == False:
        print("Invalid username or password")
    
    else:
        print(f"Welcome, {username}.\n")
        while True:
            print("1. Add information")
            print("2. Print information")
            print("3. Export information")
            print("4. Exit")
            menu = input("\nChoose an option: ")
            if menu == '1':
                print("1. Add customer")
                print("2. Add product")
                print("3. Add support")
                print("4. Add a ticket")
                print("5. Add a user")
                choice = input("\nChoose an option: ")
                if choice == '1':
                    contact_no = input("Enter contact_no: ")
                    purchase_hist = input("Enter purchase_hist: ")
                    ticket_hist = input("Enter ticket_hist: ")
                    payment_type = input("Enter payment_type: ")
                    add_customer(contact_no, purchase_hist, ticket_hist, payment_type)
                elif choice == '2':
                    project_type = input("Enter project_type: ")
                    project_date = input("Enter project_date: ")
                    project_rating = input("Enter project_rating: ")
                    add_product(project_type, project_date, project_rating)
                elif choice == '3':
                    ticket_date = input("Enter ticket_date: ")
                    ticket_status = input("Enter ticket_status: ")    
                    ticket_manager = input("Enter ticket manager name: ")
                    add_support(ticket_manager, ticket_date, ticket_status)
                elif choice == '4':
                    ticket_reason = input("Why would you like to create a ticket? ")
                    ticket_date = input("Enter ticket_date: ")
                    ticket_status = input("Enter ticket_status: ")    
                    add_ticket(ticket_date, ticket_status, ticket_reason)
                elif choice == '5':
                    new_username = input("Enter new username: ")
                    new_password = input("Enter new password: ")
                    add_user(new_username, new_password)
                else:
                    print("Invalid input. Exiting...")
                    break
            if menu == '2':
                print("1. Print customer table")
                print("2. Print product table")
                print("3. Print support table")
                print("4. Print customer data based on payment type")
                choice = input("\nChoose an option: ")
                if choice == '1':
                    print_customer()
                elif choice == '2':
                    print_product()
                elif choice =='3':
                    print_support
                elif choice =='4':
                    payment_type = input("Enter the payment type: ")
                    view_customer_given_payment_type(payment_type)
                else:
                    print("Invalid input. Exiting...")
                    break
            if menu == '3':
                print("1. Export customer data to csv")
                print("2. Export product data to csv")
                print("3. Export support data to csv")
                choice = input("\nChoose an option: ")
                if choice == "1":
                    customer_to_csv()
                if choice == "2":
                    product_to_csv()
                if choice == "3":
                    support_to_csv()
                else:
                    print("Invalid input. Exiting...")
                    break
            if menu == '4':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
    

if __name__ == "__main__":
    main()