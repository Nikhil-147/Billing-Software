from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                                 QFrame, QTextEdit, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt
import random
import pymysql

if QApplication.instance() is None:
    app = QApplication([])
window = QWidget()
window.setWindowTitle("Billing Slip")
window.setGeometry(100, 100, 1280, 720)

# Variables
c_name = ""
c_phone = ""
item = ""
rate = 0
quantity = 0
bill_no = str(random.randint(99, 9999))
l1 = []

# Header
header = QLabel("Billing Software", window)
header.setStyleSheet("background-color: green; color: gold; font-size: 25px; font-weight: bold;")
header.setAlignment(Qt.AlignCenter)

# Customer Details
customer_frame = QFrame(window)
customer_layout = QHBoxLayout(customer_frame)
customer_frame.setStyleSheet("background-color: green; color: yellow; font-size: 15px;")

customer_layout.addWidget(QLabel("Customer Name:", window))
name_input = QLineEdit(window)
customer_layout.addWidget(name_input)

customer_layout.addWidget(QLabel("Phone No:", window))
phone_input = QLineEdit(window)
customer_layout.addWidget(phone_input)

retrieve_button = QPushButton("Retrieve Bills", window)
customer_layout.addWidget(retrieve_button)

# Product Details
product_frame = QFrame(window)
product_layout = QVBoxLayout(product_frame)
product_frame.setStyleSheet("background-color: green; color: white; font-size: 15px;")

product_name_input = QLineEdit(window)
product_rate_input = QLineEdit(window)
product_quantity_input = QLineEdit(window)

product_layout.addWidget(QLabel("Product Name:"))
product_layout.addWidget(product_name_input)

product_layout.addWidget(QLabel("Product Rate:"))
product_layout.addWidget(product_rate_input)

product_layout.addWidget(QLabel("Product Quantity:"))
product_layout.addWidget(product_quantity_input)

add_button = QPushButton("Add Item", window)
product_layout.addWidget(add_button)

generate_button = QPushButton("Generate Bill", window)
product_layout.addWidget(generate_button)

clear_button = QPushButton("Clear", window)
product_layout.addWidget(clear_button)

exit_button = QPushButton("Exit", window)
product_layout.addWidget(exit_button)

# Bill Area
text_area = QTextEdit(window)
text_area.setReadOnly(True)

layout = QVBoxLayout(window)
layout.addWidget(header)
layout.addWidget(customer_frame)
layout.addWidget(product_frame)
layout.addWidget(text_area)

# Functions
def welcome():
    text_area.clear()
    text_area.append(f"\tWelcome ABC Retail\n\nBill Number: {bill_no}")

welcome()

def add_item():
    try:
        name = product_name_input.text()
        rate_val = float(product_rate_input.text())
        quantity_val = int(product_quantity_input.text())
        total = rate_val * quantity_val
        l1.append((name, rate_val, quantity_val, total))
        text_area.append(f"{name}\t{quantity_val}\t{total}")
    except ValueError:
        QMessageBox.warning(window, "Error", "Please enter valid product details")

def generate_bill():
    if not name_input.text() or not phone_input.text():
        QMessageBox.warning(window, "Error", "Customer details are required!")
        return
    text_area.append("\n======================================")
    text_area.append(f"Total Paybill Amount: {sum(x[3] for x in l1)}")
    text_area.append("======================================")
    save_bill()

def save_bill():
    try:
        db = pymysql.connect(host='localhost', user='root', password='root', database='shop')
        cursor = db.cursor()
        for data in l1:
            cursor.execute("INSERT INTO bills (bill_no, customer_name, phone, item, rate, quantity, total) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (bill_no, name_input.text(), phone_input.text(), data[0], data[1], data[2], data[3]))
        db.commit()
        db.close()
        QMessageBox.information(window, "Saved", "Bill saved to database successfully!")
    except Exception as e:
        QMessageBox.critical(window, "Error", str(e))

def retrieve_bills():
    try:
        db = pymysql.connect(host='localhost', user='root', password='root', database='shop')
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT bill_no, customer_name, phone FROM bills")
        rows = cursor.fetchall()
        db.close()

        if rows:
            bill_info = "Bill No\tCustomer Name\tPhone Number\n"
            bill_info += "=" * 40 + "\n"
            for row in rows:
                bill_info += f"{row[0]}\t{row[1]}\t{row[2]}\n"
            QMessageBox.information(window, "Bills", bill_info)
        else:
            QMessageBox.information(window, "Info", "No bills found.")
    except Exception as e:
        QMessageBox.critical(window, "Error", str(e))

def clear():
    name_input.clear()
    phone_input.clear()
    product_name_input.clear()
    product_rate_input.clear()
    product_quantity_input.clear()
    welcome()

add_button.clicked.connect(add_item)
generate_button.clicked.connect(generate_bill)
clear_button.clicked.connect(clear)
exit_button.clicked.connect(window.close)
retrieve_button.clicked.connect(retrieve_bills)

window.show()
app.exec()
