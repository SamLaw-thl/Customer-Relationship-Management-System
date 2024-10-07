# Customer Relationship Management (CRM)

import sqlite3
import hashlib
import pandas as pd


def create_table()-> None:
    """
    Creates database tables for a custom CRM system.

    This function establishes a connection to an SQLite database ('crm.db')
    and creates the following tables:
    - 'user': Stores user information (id, username, hashed_password).
    - 'product': Stores product details (project_id, project_type, project_date, project_rating).
    - 'support': Stores support ticket information (ticket_id, project_id, ticket_date, ticket_status, ticket_manager).
    - 'customer': Stores customer data (customer_id, contact_no, purchase_hist, ticket_hist, payment_type).
    - 'ticket': Stores ticket details (customer_id, ticket_id, project_id, ticket_date, ticket_status, ticket_reason).

    Note:
    - Foreign key relationships are established between tables where applicable.
    - The database connection is committed and closed after table creation.

    """
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


def login(username: str, password: str) -> bool:
    """
    Authenticate a user based on their username and password.

    Args:
        username (str): The user's username.
        password (str): The user's password (plaintext).

    Returns:
        bool: True if authentication succeeds, False otherwise.

    Notes:
        - The function connects to an SQLite database ('crm.db').
        - The password is hashed using SHA-224 for increased security.
        - It checks if the provided username and hashed password match any records in the 'user' table.
        - If a matching record is found, authentication succeeds (returns True).
        - Otherwise, authentication fails (returns False).
    """
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


def add_user(username: str, password: str)-> None:
    """
    Adds a new user to the CRM system.

    Args:
        username (str): The desired username for the new user.
        password (str): The user's password (plaintext).

    Notes:
        - The function connects to an SQLite database ('crm.db').
        - The password is hashed using SHA-224 for security.
        - Inserts a new record into the 'user' table with the provided username and hashed password.
        - Commits the changes to the database and closes the connection.
        - Prints a success message if the user was added successfully.
    """
    conn = sqlite3.connect('crm.db') 
    cursor = conn.cursor()
    hashed_password = hashlib.sha224(password.encode()).hexdigest()
    cursor.execute('INSERT INTO user (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    print(f"User added successfully.")


def add_customer(contact_no: str, purchase_hist: str, ticket_hist: str, payment_type: str)-> None:
    """
    Adds a new customer to the CRM system.

    Args:
        contact_no (str): The customer's contact number.
        purchase_hist (str): A description of the customer's purchase history.
        ticket_hist (str): A description of the customer's ticket history.
        payment_type (str): The preferred payment type for the customer.

    Notes:
        - The function connects to an SQLite database ('crm.db').
        - Inserts a new record into the 'customer' table with the provided details.
        - Commits the changes to the database and closes the connection.
        - Prints a success message if the customer was added successfully.
    """
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customer (contact_no, purchase_hist, ticket_hist, payment_type) VALUES (?, ?, ?, ?)', 
                   (contact_no, purchase_hist, ticket_hist, payment_type))
    conn.commit()
    conn.close()
    print(f"Customer added successfully.")


def add_product(project_type: str, project_date: str, project_rating: str)-> None:
    """
    Adds a new product to the CRM system.

    Args:
        project_type (str): The type or category of the product.
        project_date (str): The date associated with the product (e.g., release date).
        project_rating (str): A rating or score for the product (if applicable).

    Notes:
        - The function connects to an SQLite database ('crm.db').
        - Inserts a new record into the 'product' table with the provided details.
        - Commits the changes to the database.
        - Prints a success message indicating that the product was added successfully.
    """
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO product (project_type, project_date, project_rating) VALUES (?, ?, ?)', 
                   (project_type, project_date, project_rating))
    conn.commit()
    print(f"Product added successfully.")


def add_support(ticket_manager: str, ticket_date: str, ticket_status: str)-> None:
    """
    Adds a new support ticket to the CRM system.

    Args:
        ticket_manager (str): The manager responsible for handling the ticket.
        ticket_date (str): The date associated with the support ticket.
        ticket_status (str): The status of the support ticket (e.g., open, resolved).

    Notes:
        - The function connects to an SQLite database ('crm.db').
        - Inserts a new record into the 'support' table with the provided details.
        - Commits the changes to the database.
        - Prints a success message indicating that the support ticket was added successfully.
    """
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO support (ticket_manager, ticket_date, ticket_status) VALUES (?, ?, ?)', 
                   (ticket_manager, ticket_date, ticket_status))
    conn.commit()
    print(f"Support added successfully.")


def add_ticket(ticket_date: str, ticket_status: str, ticket_reason: str)-> None:
    """
    Adds a new support ticket to the CRM system.

    Args:
        ticket_date (str): The date associated with the support ticket.
        ticket_status (str): The status of the support ticket (e.g., open, resolved).
        ticket_reason (str): The reason or description for the support ticket.

    Notes:
        - The function connects to an SQLite database ('crm.db').
        - Inserts a new record into the 'ticket' table with the provided details.
        - Calls the 'add_support' function (assuming it exists) to handle related support information.
        - Commits the changes to the database.
        - Prints a success message indicating that the ticket was added successfully.
    """
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ticket (ticket_date, ticket_status, ticket_reason) VALUES ( ?, ?, ?)', 
                   (ticket_date, ticket_status, ticket_reason))
    add_support()
    conn.commit()
    print(f"Ticket added successfully")


def fetch_data(table_name: str) -> callable:
    """
    Decorator that fetches data from a specified table in the CRM system.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        Callable: A wrapped function that receives the fetched data as an argument.

    Notes:
        - The decorator establishes a connection to the SQLite database ('crm.db').
        - Executes a SELECT query to retrieve all rows from the specified table.
        - Closes the connection after fetching the data.
        - The wrapped function (decorated by this decorator) should accept the fetched data as an argument.
    """
    def decorator(func: callable) -> callable:
        def wrapper() -> callable :
            conn = sqlite3.connect('crm.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            conn.close()
            return func(rows)
        return wrapper 
    return decorator


@fetch_data(table_name="customer")
def print_customer(rows: list[tuple[int, str]])-> None:
    """
    Prints customer data retrieved from the CRM system.

    Args:
        rows (list[tuple[int, str]]): A list of tuples representing customer records.
            Each tuple contains the following elements:
            - customer_id (int): The unique identifier for the customer.
            - contact_no (str): The customer's contact number.
            - purchase_hist (str): A description of the customer's purchase history.
            - ticket_hist (str): A description of the customer's ticket history.
            - payment_type (str): The preferred payment type for the customer.

    Notes:
        - The function is decorated with @fetch_data, which fetches data from the 'customer' table.
        - If customer records are found, it prints details for each customer.
        - If no customers are found, it prints a message indicating that no records were found.
    """
    if rows:
        for row in rows:
            print(f"customer_id: {row[0]}, contact_no: {row[1]}, purchase_hist: {row[2]}, ticket_hist: {row[3]}, payment_type: {row[4]} ")
    else:
        print("No customer found.")


@fetch_data(table_name="customer")
def customer_to_csv(rows: list[tuple[int, str]])-> None:
    """
    Exports customer data from the CRM system to a CSV file.

    Args:
        rows (list[tuple[int, str]]): A list of tuples representing customer records.
            Each tuple contains the following elements:
            - customer_id (int): The unique identifier for the customer.
            - contact_no (str): The customer's contact number.
            - purchase_hist (str): A description of the customer's purchase history.
            - ticket_hist (str): A description of the customer's ticket history.
            - payment_type (str): The preferred payment type for the customer.

    Notes:
        - The function is decorated with @fetch_data, which fetches data from the 'customer' table.
        - If customer records are found, it creates a Pandas DataFrame and exports it to a CSV file.
        - The CSV file is named 'customer_data.csv' and does not include an index column.
        - Prints a success message if data is exported successfully.
        - If no customer data is found, it prints a message indicating that no records were found.
    """
    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["customer_id", "contact_no", "purchase_hist", "ticket_hist", "payment_type"]
        df.to_csv('customer_data.csv', index=False)
        print("Customer data successsfully exported to customer_data.csv")
    else:
        print("No customer data to export.")


@fetch_data(table_name="product")
def print_product(rows: list[tuple[int, str]]) -> None:
    """
    Prints product data retrieved from the CRM system.

    Args:
        rows (list[tuple[int, str]]): A list of tuples representing product records.
            Each tuple contains the following elements:
            - project_id (int): The unique identifier for the product.
            - project_type (str): The type or category of the product.
            - project_date (str): The date associated with the product (e.g., release date).
            - project_rating (int): A rating or score for the product (if applicable).

    Notes:
        - The function is decorated with @fetch_data, which fetches data from the 'product' table.
        - If product records are found, it prints details for each product.
        - If no products are found, it prints a message indicating that no records were found.
    """
    if rows:
        for row in rows:
            print(f"project_id: {row[0]}, project_type: {row[1]}, project_date: {row[2]}, project_rating: {row[3]}")
    else:
        print("No product found.")


@fetch_data(table_name="product")
def product_to_csv(rows: list[tuple[int, str]]) -> None:
    """
    Exports product data from the CRM system to a CSV file.

    Args:
        rows (list[tuple[int, str]]): A list of tuples representing product records.
            Each tuple contains the following elements:
            - project_id (int): The unique identifier for the product.
            - project_type (str): The type or category of the product.
            - project_date (str): The date associated with the product (e.g., release date).
            - project_rating (int): A rating or score for the product (if applicable).

    Notes:
        - The function is decorated with @fetch_data, which fetches data from the 'product' table.
        - If product records are found, it creates a Pandas DataFrame and exports it to a CSV file.
        - The CSV file is named 'product_data.csv' and does not include an index column.
        - Prints a success message if data is exported successfully.
        - If no product data is found, it prints a message indicating that no records were found.
    """
    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["project_id", "project_type", "project_date", "project_rating"]
        df.to_csv('product_data.csv', index=False)
        print("Product data successsfully exported to product_data.csv")
    else:
        print("No product data to export.")


# print support table
@fetch_data(table_name="support")
def print_support(rows: list[tuple[int, str, bool]]) -> None:
    """
    Prints support ticket data retrieved from the CRM system.

    Args:
        rows (list[tuple[int, str, bool]]): A list of tuples representing support ticket records.
            Each tuple contains the following elements:
            - ticket_id (int): The unique identifier for the support ticket.
            - project_type (str): The type or category associated with the support ticket.
            - ticket_date (str): The date of the support ticket.
            - ticket_status (bool): The status of the support ticket (True for open, False for resolved).
            - ticket_manager (str): The manager responsible for handling the support ticket.

    Notes:
        - The function is decorated with @fetch_data, which fetches data from the 'support' table.
        - If support ticket records are found, it prints details for each ticket.
        - If no support tickets are found, it prints a message indicating that no records were found.
    """    
    if rows:
        for row in rows:
            print(f"ticket_id: {row[0]}, project_type: {row[1]}, ticket_date: {row[2]}, ticket_status: {row[3]}, ticket_manager: {row[4]}")
    else:
        print("No support found.")


# export support data to csv file
@fetch_data(table_name="support")
def support_to_csv(rows: list[tuple[int, str, bool]]):
    """
    Exports support ticket data from the CRM system to a CSV file.

    Args:
        rows (list[tuple[int, str, bool]]): A list of tuples representing support ticket records.
            Each tuple contains the following elements:
            - ticket_id (int): The unique identifier for the support ticket.
            - project_type (str): The type or category associated with the support ticket.
            - ticket_date (str): The date of the support ticket.
            - ticket_status (bool): The status of the support ticket (True for open, False for resolved).

    Notes:
        - The function is decorated with @fetch_data, which fetches data from the 'support' table.
        - If support ticket records are found, it creates a Pandas DataFrame and exports it to a CSV file.
        - The CSV file is named 'support_data.csv' and does not include an index column.
        - Prints a success message if data is exported successfully.
        - If no support data is found, it prints a message indicating that no records were found.
    """
    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["ticket_id", "project_type", "ticket_date", "ticket_status"]
        df.to_csv('support_data.csv', index=False)
        print("Support data successsfully exported to support_data.csv")
    else:
        print("No support data to export.")


def view_customer_given_payment_type(payment_type: str) -> None:
    """
    Retrieves and prints customer data based on the specified payment type.

    Args:
        payment_type (str): The preferred payment type for filtering customer records.

    Notes:
        - Connects to the SQLite database ('crm.db').
        - Executes a SELECT query to retrieve customer records matching the provided payment type.
        - If matching records are found, it prints details for each customer.
        - If no customers with the specified payment type are found, it prints a message indicating so.
    """
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


def main() -> None:
    """
    Main function for the CRM system.

    Notes:
        - Calls the 'create_table' function to set up database tables.
        - Prompts the user for a username and password.
        - If login is successful, displays a welcome message and presents a menu of options.
        - Handles user input for adding information (customers, products, support, tickets, users),
          printing information (customer, product, support, or filtered by payment type),
          exporting information (to CSV files), and exiting the program.
        - Provides appropriate feedback for invalid input.
    """
    create_table()
    username = input("Enter username: ")
    password = input ("Enter password: ")

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