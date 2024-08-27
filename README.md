# Customer Relationship Management (CRM) System

# Overview
This Python-based CRM system allows you to manage customer data, track products, handle support tickets, and authenticate users. It uses an SQLite database to store information securely.

# Database Schema
![schema](.\img\CusReMa_schema.png)

# Features
1. User Authentication:
    - Users can log in with their username and password.
    - Passwords are securely hashed using SHA-224.

2. Database Tables:
    - The system includes the following tables:
    - `user`: Stores user information.
    - `product`: Contains details about projects.
    - `support`: Handles support tickets.
    - `customer`: Stores customer information.
    - `ticket`: Represents individual support tickets.

3. Functionality:
    - Add new users, customers, products, support details, and tickets.
    - Print information from tables (customers, products, support).
    - Export data to CSV files.
    - Filter customers by payment type.

Getting Started
1. Prerequisites:
    - Python 3.x installed.
    - Ensure you have the required libraries (`sqlite3`, `hashlib`, `pandas`)`.
        
2. Setup:
    - Clone this repository to your local machine.
    - Create an SQLite database file named `crm.db`.
    - Run the `create_table()` function to set up the necessary tables.

3. Usage:
    - Run the program (`python crm.py`).
    - Log in with your username and password.
    - Choose from the menu options to add data, print tables, or export data.

# Menu Options
1. Add Information:
    - Choose options to add customers, products, support details, tickets, or new users.

2. Print Information:
    - View customer, product, or support data.
    - Filter customers by payment type.

3. Export Information:
    - Export customer, product, or support data to CSV files.

4. Exit:
    Terminate the program.

# Example Usage
1. Adding a new customer:
```
Choose an option: 1
Enter contact_no: 1234567890
Enter purchase_hist: 5
Enter ticket_hist: 3
Enter payment_type: credit card
Customer added successfully.
```

2. Printing customer data:
```
Choose an option: 2
1. Print customer table
2. Print product table
3. Print support table
4. Print customer data based on payment type
Choose an option: 1
customer_id: 1, contact_no: 1234567890, purchase_hist: 5, ticket_hist: 3, payment_type: credit card
```

# License
This project is licensed under the MIT License - feel free to use, modify, and distribute it.

