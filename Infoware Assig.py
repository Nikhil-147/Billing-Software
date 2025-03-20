import tkinter 
from tkinter import *
import random
from tkinter import messagebox
import pymysql	

t=tkinter.Tk()
t.title("Billing Slip")
t.geometry('1280x720')

# Variable
c_name=StringVar()
c_phone=StringVar()
item=StringVar()
Rate=IntVar()
quantity=IntVar()
bill_no=StringVar()
x=random.randint(99,9999)
bill_no.set(str(x))

global l1
l1 = [] 
    
# Create Welcome Function 
def welcome():
    textarea.delete(1.0,END)
    textarea.insert(END,"\t     Welcome ABC Retail")
    textarea.insert(END,f"\n\nBill Number:\t\t{bill_no.get()}")
    textarea.insert(END,f"\nCustomer Name:\t\t{c_name.get()}")
    textarea.insert(END,f"\nPhone Number:\t\t{c_phone.get()}")
    textarea.insert(END,f"\n\n======================================")
    textarea.insert(END,"\nProduct\t\tQTY\t\tPrice")
    textarea.insert(END,f"\n======================================\n")
    textarea.configure(font='arial 15 bold')
 
# Create Add Product Function
def additm():
    n=Rate.get()
    m=quantity.get()*n
    l1.append((item.get(), n, quantity.get(), m))
    if item.get()!='':
        textarea.insert(END, f"{item.get()}\t\t{quantity.get()}\t\t{ m}\n")
    else:
        messagebox.showerror('Error','Please enter item')

# Create Genrate Bill Function        
def gbill():
    if c_name.get() == "" or c_phone.get() == "":
        messagebox.showerror("Error", "Customer detail are must")
    else:
        welcome()
        for data in l1:
            textarea.insert(END, f"{data[0]}\t\t{data[2]}\t\t{data[3]}\n")
        textarea.insert(END, f"\n======================================")
        textarea.insert(END, f"\nTotal Paybill Amount :\t\t      {sum(x[3] for x in l1)}")
        textarea.insert(END, f"\n\n======================================")
        save_bill()

# Save Bill into DataBase
def save_bill():
    try:
        db = pymysql.connect(host='localhost',user='root',password='root',database='shop')
        cursor = db.cursor()
        for data in l1:
            cursor.execute("INSERT INTO bills (bill_no, customer_name, phone, item, rate, quantity, total) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (bill_no.get(), c_name.get(), c_phone.get(), data[0], data[1], data[2], data[3]))
        db.commit()
        db.close()
        messagebox.showinfo("Saved", f"Bill No: {bill_no.get()} saved to database successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Retrieve Bill into DataBase
def retrieve_bills():
    try:
        db = pymysql.connect(host='localhost',user='root',password='root',database='shop')
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT bill_no, customer_name, phone FROM bills")
        rows = cursor.fetchall()
        db.close()

        if rows:
            result_window = Toplevel(t)
            result_window.title("Bills and Customers")
            result_window.geometry('600x400')
            text_area = Text(result_window, font='arial 12')
            text_area.pack(expand=True, fill=BOTH)

            text_area.insert(END, "Bill No\tCustomer Name\tPhone Number\n")
            text_area.insert(END, "========================================\n")
            for row in rows:
                text_area.insert(END, f"{row[0]}\t{row[1]}\t{row[2]}\n")
        else:
            messagebox.showinfo("Info", "No bills found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create Clear screen function    
def clear():
    c_name.set('')
    c_phone.set('')
    item.set('')
    Rate.set(0)
    quantity.set(0)
    welcome()
    
# Create Exit Function
def exit():
    op = messagebox.askyesno("Exit", "Do you really want to exit?")
    if op > 0:
        t.destroy()
        


# Headline Billing Software 4D0039
a = Label(t,text="Billing Software",bg='Green',bd=10,font=("times new roman",25,'bold'),fg="gold",relief=GROOVE,justify=CENTER)
a.pack(fill=X)

# Customer Details Frame 1
b = LabelFrame(t,text="Customer Details",bg='Green',bd=8,font=("times new roman",18,'bold'),fg="yellow",relief=GROOVE)
b.place(x=0,y=80,relwidth=1)

# Customer Name
d = Label(b,text="Customer Name",bg='Green',font=("times new roman",15,'bold'),fg="white") 
d.grid(row=0,column=0,padx=10,pady=5)
d1 = Entry(b,width=15,font=("arail 15 bold"),relief=SUNKEN,textvariable=c_name)
d1.grid(row=0,column=1,padx=10,pady=5)


# Customer Phone Number
e = Label(b,text="Phone No.",bg='Green',font=("times new roman",15,'bold'),fg="white") 
e.grid(row=0,column=2,padx=10,pady=5)
e1 = Entry(b,width=15,font=("arail 15 bold"),relief=SUNKEN,textvariable=c_phone)
e1.grid(row=0,column=3,padx=10,pady=5)

# Button to Retrieve Bills
retrieve_button = Button(b, text="Retrieve Bills", font='arial 15 bold', bg='orange', width=15,command=retrieve_bills)
retrieve_button.grid(row=0,column=4,padx=50,pady=5)

# Product Details Frame 2
f = LabelFrame(t, text='Product Details', font=('times new roman', 18, 'bold'), fg='yellow',bg='Green')
f.place(x=20, y=180,width=630,height=500)

# Product Name
g = Label(f, text='Product Name', font=('times new roman',18, 'bold'), bg='Green', fg='white')
g.grid(row=0, column=0, padx=30, pady=20)
g1 = Entry(f, width=20, font='arial 15 bold', relief=SUNKEN, bd=7,textvariable=item)
g1.grid(row=0, column=1, padx=10,pady=20)

# Product Rate
h= Label(f, text='Product Rate', font=('times new roman',18, 'bold'), bg='Green', fg='white')
h.grid(row=1, column=0, padx=30, pady=20)
h1 = Entry(f, width=20, font='arial 15 bold', relief=SUNKEN, bd=7,textvariable=Rate)
h1.grid(row=1, column=1, padx=10,pady=20)

# Product Quantity
j= Label(f, text='Product Quantity', font=('times new roman',18, 'bold'), bg='Green', fg='white')
j.grid(row=2, column=0, padx=30, pady=20)
j1 = Entry(f, width=20, font='arial 15 bold', relief=SUNKEN, bd=7,textvariable=quantity)
j1.grid(row=2, column=1, padx=10,pady=20)


# Button Add Item
btn1=Button(f,text='Add item',font='arial 15 bold',padx=5,pady=10,bg='Orange',width=15,command=additm)
btn1.grid(row=3,column=0,padx=10,pady=30)

# Button Genrate Bill
btn2=Button(f,text='Generate Bill',font='arial 15 bold',padx=5,pady=10,bg='Orange',width=15,command=gbill)
btn2.grid(row=3,column=1,padx=10,pady=30)

# Button Clear
btn3=Button(f,text='Clear',font='arial 15 bold',padx=5,pady=10,bg='Orange',width=15,command=clear)
btn3.grid(row=4,column=0,padx=10,pady=30)

# Button Exit
btn4=Button(f,text='Exit',font='arial 15 bold',padx=5,pady=10,bg='Orange',width=15,command=exit)
btn4.grid(row=4,column=1,padx=10,pady=30)

# Billing Area Frame 3
k = Frame(t,relief=GROOVE,bd=10)
k.place(x=700,y=180,width=500,height=500)


# Label Bill Area
l=Label(k,text='Bill Area',font='arial 15 bold',bd=7,relief=GROOVE)
l.pack(fill=X)

# Scroll Bar
scrol_y=Scrollbar(k,orient=VERTICAL)
textarea=Text(k,yscrollcommand=scrol_y)

scrol_y.pack(side=RIGHT,fill=Y)
scrol_y.config(command=textarea.yview)
textarea.pack()


welcome()
  

t.mainloop()