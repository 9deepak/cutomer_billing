import sqlite3
from xlsxwriter.workbook import Workbook
from datetime import datetime

class Database:
    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS customer_data (id INTEGER PRIMARY KEY,customer_name,customer_phone,end_customer_name,end_customer_phone,delivery_partner,amount_Paid,internal_amount)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("select * from customer_data")
        rows=self.cur.fetchall()
        return rows

    def insert(self,customer_name,customer_phone,end_customer_name,end_customer_phone,delivery_partner,amount_Paid,internal_amount):
        self.cur.execute("INSERT INTO customer_data values (NULL,?,?,?,?,?,?,?)",(customer_name,customer_phone,end_customer_name,end_customer_phone,delivery_partner,amount_Paid,internal_amount))
        self.conn.commit()

    def remove(self,id):
        self.cur.execute("delete from customer_data where id=?",(id,))
        self.conn.commit()

    def update(self,id,customer_name,customer_phone,end_customer_name,end_customer_phone,delivery_partner,amount_Paid,internal_amount):
        self.cur.execute("update customer_data set customer_name=?,customer_phone=?,end_customer_name=?,end_customer_phone=?,delivery_partner=?,amount_Paid=?,internal_amount=? where id=?",(customer_name,customer_phone,end_customer_name,end_customer_phone,delivery_partner,amount_Paid,internal_amount,id))
        self.conn.commit()

    def excel(self):
        dateTimeObj = datetime.now()
        workbook = Workbook('customer_data_{0}-{1}-{2}_{3}:{4}.xlsx'.format(dateTimeObj.day,dateTimeObj.month,dateTimeObj.year,dateTimeObj.hour,dateTimeObj.minute))
        worksheet = workbook.add_worksheet()
        a=self.cur.execute("select * from customer_data")
        for i, row in enumerate(a):
            for j, value in enumerate(row):
                worksheet.write(i,j, value)
        workbook.close()
            
    def __del__(self):
        self.conn.close()

