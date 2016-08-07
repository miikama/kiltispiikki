import sqlite3
import os
from piikki_utilities import Item
from kivy.logger import Logger

#full_path =  os.getcwd() #on a computer
#db_path = "{}/{}".format(os.getcwd(), "piikki.db")
#full_path = "/sdcard/data/piikki.db"        #on android, create the data folder on your home folder which is /sdcard


#'''Resets all tab values to 0, USE WITH CAUTION'''        
#def clear_tab_values():
#    
#    con = sqlite3.connect(db_path)
#            
#    c = con.cursor()        
#    c.execute("UPDATE customers SET tab_value=0.0")
#    
#    con.commit()        
#    con.close()

class CustomerHandler():
    
    full_path = os.getcwd()
    db_path = "{}/{}".format(os.getcwd(), "piikki.db")
    customers = []
    
    def __init__(self,path):
        self.full_path = path
        self.db_path =os.path.join(path, "piikki.db")

    '''Returns a list[Customer] of all customers or None if there are no customers'''
    def load_customers(self):       
        
        customers = []
        con = sqlite3.connect(self.db_path)        
        c = con.cursor()      
        
        c.execute("SELECT * FROM customers")
        data=c.fetchall()
        con.close()
        if data is None: return None
        else: 
            for customer in data:
                customers.append(Customer(customer[0], customer[2], tab_value=customer[3]))
        
        self.customers = customers


    '''Creates piikki database if it doesn't exist and adds customer and buy_action tables'''
    def enable_databases(self):      
            con = sqlite3.connect(self.db_path)
                    
            c = con.cursor()        
            c.execute('''CREATE TABLE IF NOT EXISTS customers (account_name text, password text,
             customer_name text, tab_value real)''')
            con.commit() 
            c.close()       
            con.close()
                    
            con = sqlite3.connect(self.db_path)
            c = con.cursor()
            
            c.execute('''CREATE TABLE IF NOT EXISTS buy_actions (account_name text, item_name text, item_class text, buy_value real)''')
            
            con.commit()        
            con.close()
        
    def save_csv(self):
        
        #f = open('customers_csv.txt', 'w')
        
        Logger.info('called save csv, not implemented yet')
            
    def load_csv(self):
        
        
        try: f = open('customers.txt', 'r')
        except IOError: Logger.info('tried to load a nonexisting csv')
        customers = []    
        
        for line in f:
            values = line.split(',')
            acc_name = values[0]
            full_name = values[1]
            value = float(values[2])
            customers.append(Customer(acc_name, full_name,value ))
            
        f.close()    
        return customers
    
        
        

    

    '''Returns row number where the account is in the database or None if it doesn't exist''' 
    def account_row(self,name):
            
            con = sqlite3.connect(self.db_path)        
            c = con.cursor()      
            
            c.execute("SELECT rowid FROM customers WHERE account_name = ?", (name,))
            data=c.fetchone()
            con.close()
            if data is None: return None
            else: return data[0]    



       
    '''all the data is stored in database piikki.db'''
    def create_new_account(self, customer):
        con = sqlite3.connect(self.db_path)
        
        c = con.cursor()        
        values = (customer.account_name, '', customer.customer_name, customer.tab_value)
        c.execute("INSERT INTO customers VALUES (?,?,?,?)", values)
                
        con.commit()        
        con.close() 

        self.customers.append(customer)         
           
        
    '''Saves the buy information into buy_actions TABLE with values account_name, item_name, item_class, buy_value '''    
    def save_buy(self,customer, item):
        con = sqlite3.connect(self.db_path)
        
        c = con.cursor()        
        values = (customer.account_name, item.name, item.item_class, item.price)
        c.execute("INSERT INTO buy_actions VALUES (?,?,?,?)", values)
                
        con.commit()        
        con.close() 
    
    '''Gets the items that the customer has bought, prob dict with item ids as keys'''
    def load_buy_history(self):
        pass   
    
        
    
    '''returns the items in the order of most bought first together with the bought amount'''
    def most_bought(self, customer):
        con = sqlite3.connect(self.db_path)
        
        c = con.cursor()
        c.execute("SELECT  item_name, buy_value, item_class, COUNT(item_name) FROM buy_actions WHERE account_name=? GROUP BY account_name,item_name", (customer.account_name,))
        data = c.fetchall()        
        con.close()
        
        items = [(Item(i[0], i[1], i[2], self.full_path), i[3]) for i in data ]
        items.sort(key=lambda x: x[1])
        items.reverse()
        #items is list of tuples (Item, number of bought)
        return items
        
    
    '''customer pays money to the tab'''
    def pay_to_tab(self,customer, amount):
        customer.pay_to_tab(amount)
        self.update_tab_value(customer)
    
    
    '''customer buys something using the tab'''
    def pay_from_tab(self,customer, amount):
        customer.pay_from_tab(amount)
        self.update_tab_value(customer)
    
    
    '''Updates the customers tab_value in the database'''
    def update_tab_value(self,customer):
        con = sqlite3.connect(self.db_path)
        
        c = con.cursor()               
        c.execute("UPDATE customers SET tab_value=? WHERE account_name=?", (customer.tab_value, customer.account_name))
                
        con.commit()        
        con.close()
    
    
'''class Customer portrays users of the tab'''
class Customer():
    
    def __init__(self, account_name, full_name, tab_value = 0.0):       
        self.customer_name = full_name
        self.account_name = account_name
        self.tab_value = tab_value
        
    '''customer pays money to the tab'''
    def pay_to_tab(self, amount):
        self.tab_value = self.tab_value + amount    
    
    '''customer buys something using the tab'''
    def pay_from_tab(self, amount):
        self.tab_value = self.tab_value - amount
           
    
    