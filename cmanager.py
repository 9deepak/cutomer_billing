from tkinter import *
from tkinter.font import BOLD
import tkinter.messagebox as mb
from db import Database
from fpdf import FPDF,HTMLMixin
import webbrowser


db = Database('store.db')

def populate():
    customer_name_list.delete(0,END)
    for row in db.fetch():
        customer_name_list.insert(END,row)
def add_customer():
    if (customer_name_text.get()=='' or customer_phone_text.get()== '' or end_customer_name_text.get()=='' or end_customer_phone_text.get()=='' or delivery_partner_text.get()=='' or amount_paid_text.get()=='' or internal_amount_text.get()==''):
        mb.showerror('Required Fileds','Fileds with "*" are Mandatory')
        return
    db.insert(customer_name_text.get(),customer_phone_text.get(),end_customer_name_text.get(),end_customer_phone_text.get(),delivery_partner_text.get(),amount_paid_text.get(),internal_amount_text.get())
    customer_name_list.delete(0,END)
    customer_name_list.insert(END,(customer_name_text.get(),customer_phone_text.get(),end_customer_name_text.get(),end_customer_phone_text.get(),delivery_partner_text.get(),amount_paid_text.get(),internal_amount_text.get()))
    clear_Entry()
    populate()

def select_item(event):
    try:
        global selected_item
        index = customer_name_list.curselection()[0]
        selected_item=customer_name_list.get(index)

        customer_name_entry.delete(0,END)
        customer_name_entry.insert(END,selected_item[1])
        customer_phone_entry.delete(0,END)
        customer_phone_entry.insert(END,selected_item[2])
        end_customer_name_entry.delete(0,END)
        end_customer_name_entry.insert(END,selected_item[3])
        end_customer_phone_text_entry.delete(0,END)
        end_customer_phone_text_entry.insert(END,selected_item[4])
        delivery_partner_entry.delete(0,END)
        delivery_partner_entry.insert(END,selected_item[5])
        amount_paid_entry.delete(0,END)
        amount_paid_entry.insert(END,selected_item[6])
        internal_amount_entry.delete(0,END)
        internal_amount_entry.insert(END,selected_item[7])
    except IndexError:
        pass

def remove_customer():
    db.remove(selected_item[0])
    mb.showinfo('success','Removed Entry : {0}'.format(selected_item))
    clear_Entry()
    populate()


def update_customer():
    db.update(selected_item[0],customer_name_text.get(),customer_phone_text.get(),end_customer_name_text.get(),end_customer_phone_text.get(),delivery_partner_text.get(),amount_paid_text.get(),internal_amount_text.get())
    populate()

def clear_Entry():
    customer_name_entry.delete(0,END)
    customer_phone_entry.delete(0,END)
    end_customer_name_entry.delete(0,END)
    end_customer_address_entry.delete(0,END)
    end_customer_phone_text_entry.delete(0,END)
    delivery_partner_entry.delete(0,END)
    amount_paid_entry.delete(0,END)
    internal_amount_entry.delete(0,END)

def excel_entry():
    db.excel()
    mb.showinfo('success','Excel Generated')

def print_entry():
    try:
        print('print initiated')
        class MyFPDF(FPDF,HTMLMixin):
            pass
        pdf = MyFPDF() 
        html="""
    <p align="center"><img src="sv_logo.png" width="250" height="70"></p>
    <h1 align="center" font-style:Arial>Bill Details</h1>
    Dear Customer,<br>
    Thank You for choosing us for your courier service
    <br>
    <hr>
    <table style="border: 1px solid transparent" cellpadding="15">
    <tr><th width="50%"></th><th width="50%"></th></tr>
    <tr><td>Customer name</td><td>: {0}</td></tr>
    <tr><td>Customer phone No</td><td>: {1}</td></tr>
    <tr><td>Delivery Partner</td><td>: {2}</td></tr>
    <tr><td>Amount</td><td>: {3}</td></tr>
    </table>
    <hr>
    <p align="center"><img src="sv.png" width="250" height="100"></p>
    <p align="left">Terms & Conditions :</p>
    <ol>
    <li>The customer is responsible for customs/ duties/ charges and will not hold SV Express International Courier & Cargo (Herein after called as SV Express) against any of the associated charges and/or delays arising due to customs clearance.</li>
    <li>The customer is solely responsible for the dimensions and weight specified to be correct and if there are any variations to the weight and/or dimensions, the customer could be charged for the extra weight and additional processing charges occurring due to change in dimensions/weight declared and also the shipments could be stopped due to discrepancy in dimensions specified.</li>
    <li>SV Express is not responsible for shipment held for any reason beyond our control like government agencies, natural calamities or unforeseen events.</li>
    <li>The customer also agrees not to ship any prohibited items and is solely responsible for the consequences arising out of it if sent.</li>
    <li>Return shipment charges and also possible custom charges will be borne only by the Customer provided if there is no mistake of SV Express.</li>
    <li>Claims on Shipment value above Rs.1000/- would be entertained only upon insurance of the packages.</li>
    <li>In case of damage of shipments  because of solely SV Express mistake, refund will be given in 90 days.</li>
    <li>Claiming conditions:Complaint must be given within 72hrs in writing from the shipment delivery date, along with proof.</li>
    <li>All disputes are subject to Vijayawada jurisdiction only.</li>
    </ol>
    """.format(selected_item[1],selected_item[2],selected_item[5],selected_item[6])
        # Add a page
        pdf.add_page()
        pdf.write_html(html)
        # save the pdf with name .pdf
        pdf.output("customer.pdf")
        path = 'customer.pdf'
        webbrowser.open_new(path)

    except NameError:
        mb.showerror('Error','Selet an Entry to Print')
        pass



#pdf Generation

app =Tk()

#customer Name
customer_name_text = StringVar()
customer_name_label = Label(app,text='*Customer Name :',font=(BOLD,14),pady=20)
customer_name_label.grid(row=0,column=0,sticky=W)
customer_name_entry = Entry(app,textvariable=customer_name_text)
customer_name_entry.grid(row=0,column=1)

#customer Phone
customer_phone_text = StringVar()
customer_phone_label = Label(app,text='*Customer Phone :',font=(BOLD,14))
customer_phone_label.grid(row=0,column=2,sticky=W)
customer_phone_entry = Entry(app,textvariable=customer_phone_text)
customer_phone_entry.grid(row=0,column=3)

# END Delivery customer Name
end_customer_name_text = StringVar()
end_customer_name_label = Label(app,text='*End Customer Name :',font=(BOLD,14))
end_customer_name_label.grid(row=1,column=0,sticky=W)
end_customer_name_entry = Entry(app,textvariable=end_customer_name_text)
end_customer_name_entry.grid(row=1,column=1)

#END customer Phone
end_customer_phone_text = StringVar()
end_customer_phone_text_label = Label(app,text='*END Customer Phone :',font=(BOLD,14))
end_customer_phone_text_label.grid(row=1,column=2,sticky=W)
end_customer_phone_text_entry = Entry(app,textvariable=end_customer_phone_text)
end_customer_phone_text_entry.grid(row=1,column=3)

#END customer Adress
end_customer_address_text = StringVar()
end_customer_address_label = Label(app,text='END Customer Adress :',font=(BOLD,14),pady=20)
end_customer_address_label.grid(row=2,column=0,sticky=W)
end_customer_address_entry = Entry(app,textvariable=end_customer_address_text)
end_customer_address_entry.grid(row=2,column=1)

#Delivery Partner
delivery_partner_text = StringVar()
delivery_partner_label = Label(app,text='*Delivery Partner :',font=(BOLD,14))
delivery_partner_label.grid(row=3,column=0,sticky=W)
delivery_partner_entry = Entry(app,textvariable=delivery_partner_text)
delivery_partner_entry.grid(row=3,column=1)

#Paid Amount
amount_paid_text = StringVar()
amount_paid_label = Label(app,text='*Amount Paid :',font=(BOLD,14))
amount_paid_label.grid(row=3,column=2,sticky=W)
amount_paid_entry = Entry(app,textvariable=amount_paid_text)
amount_paid_entry.grid(row=3,column=3)

#Internal Amount
internal_amount_text = StringVar()
internal_amount_label = Label(app,text='*Internal Amount :',font=(BOLD,14),pady=20)
internal_amount_label.grid(row=4,column=0,sticky=W)
internal_amount_entry = Entry(app,textvariable=internal_amount_text)
internal_amount_entry.grid(row=4,column=1)


customer_name_list = Listbox(app,height=15,width=50)
customer_name_list.grid(row=7,column=0,columnspan=3,rowspan=6,padx=20,pady=20)

#create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=7,column=2)


#set scroll to listbox
customer_name_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=customer_name_list.yview)

#Bind select
customer_name_list.bind('<<ListboxSelect>>',select_item)

#buttons

add_btn = Button(app,text='Add Customer',width=12,command=add_customer)
add_btn.grid(row=5,column=0,pady=20)

remove_btn = Button(app,text='Remove Customer',width=12,command=remove_customer)
remove_btn.grid(row=5,column=1)

update_btn = Button(app,text='Update Customer',width=12,command=update_customer)
update_btn.grid(row=5,column=2)

clear_btn = Button(app,text='Clear Entry',width=12,command=clear_Entry)
clear_btn.grid(row=5,column=3)

print_btn = Button(app,text='Print',width=12,command=print_entry)
print_btn.grid(row=5,column=4)

Excel_btn = Button(app,text='Export Data to Excel',width=15,command=excel_entry)
Excel_btn.grid(row=6,column=2)

app.title("SV Express Customer Details Portal")

app.geometry('900x1200')

populate()

app.mainloop()