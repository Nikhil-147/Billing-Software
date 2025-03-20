
# Tkinter Billing Software Application

This project is a billing software application built using Python's Tkinter library. It allows users to create and manage billing slips efficiently with a graphical user interface (GUI). The application saves bills to a MySQL database and provides functionality to retrieve past bills.

## Features 
- **Customer Information**: Input customer name and phone number for personalized billing.
- **Product Details**: Add product name, rate, and quantity.
- **Bill Generation**: Automatically calculate total amounts and generate an itemized bill.
- **Database Integration**: Save bills to a MySQL database and retrieve past bills.
- **Clear Screen**: Reset input fields to create a new bill.
- **Exit Option**: Close the application with confirmation.

## Requirements
To run this project, you need:
- Python 3.x
- Tkinter (Pre-installed with Python)
- pymysql
- MySQL server with a pre-configured database

## Setup Instructions
1. **Clone the repository**:
   git clone <repository-URL>
   cd BillingSoftware
  
2. **Install Dependencies**:
   bash
   pip install pymysql

3. **Set Up MySQL Database**:
   - Create a database called `shop`.
   - Create a table using the following SQL query:
     sql
     CREATE TABLE bills (
       bill_no VARCHAR(50),
       customer_name VARCHAR(255),
       phone VARCHAR(15),
       item VARCHAR(255),
       rate FLOAT,
       quantity INT,
       total FLOAT
     );
     
   - Update the MySQL credentials in the `save_bill()` and `retrieve_bills()` functions as per your database configuration.

4. **Run the Application**:
   bash
   python main.py

## Usage
1. Launch the application.
2. Enter customer details (name and phone number).
3. Add products by specifying the name, rate, and quantity.
4. Click **Add Item** to include a product in the bill.
5. Click **Generate Bill** to calculate the total amount and save it to the database.
6. Use **Retrieve Bills** to view past billing records from the database.
7. Use **Clear** to reset fields and start a new transaction.
8. Click **Exit** to close the application.


## Notes
- Ensure MySQL server is running when using this application.
- All entered data is saved in the `shop` database under the `bills` table.
- Error messages will display if invalid inputs are provided or in case of database connection issues.

 
