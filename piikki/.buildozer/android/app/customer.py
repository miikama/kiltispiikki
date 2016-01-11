import sqlite3
import os


full_path = "{}/{}".format(os.getcwd(), "piikki.db")  #on a computer
#full_path = "/sdcard/data/piikki.db"         #MAYBE NO   #on android, create the data folder on your home folder which is /sdcard


'''Returns a list[Customer] of all customers or None if there are no customers'''
def load_customers():
    
    customers = []
    
    con = sqlite3.connect(full_path)        
    c = con.cursor()      
    
    c.execute("SELECT * FROM customers")
    data=c.fetchall()
    con.close()
    if data is None: return None
    else: 
        for customer in data:
            customers.append(Customer(customer[0], customer[1], customer[2], tab_value=customer[3]))
    
    return customers


'''Creates customer database if it doesn't exist'''
def enable_databases():      
        con = sqlite3.connect(full_path)
                
        c = con.cursor()        
        c.execute('''CREATE TABLE IF NOT EXISTS customers (account_name text, password text,
         customer_name text, tab_value real)''')
        
        con.commit()        
        con.close()
        
        
'''Resets all tab values to 0, USE WITH CAUTION'''        
def clear_tab_values():
    
    con = sqlite3.connect(full_path)
            
    c = con.cursor()        
    c.execute("UPDATE customers SET tab_value=0.0")
    
    con.commit()        
    con.close()
    

'''Returns row number where the account is in the database or None if it doesn't exist''' 
def account_row(name):
        
        con = sqlite3.connect(full_path)        
        c = con.cursor()      
        
        c.execute("SELECT rowid FROM customers WHERE account_name = ?", (name,))
        data=c.fetchone()
        con.close()
        if data is None: return None
        else: return data[0]    


'''class Customer contains functions concerning customers...'''
class Customer():
    

    
    def __init__(self, account_name, password, full_name,  tab_value = 0.0):       
        self.customer_name = full_name
        self.account_name = account_name
        self.password = password
        self.tab_value = tab_value
        
       
    '''all the data is stored in database piikki.db'''
    def create_new_account(self):
        con = sqlite3.connect(full_path)
        
        c = con.cursor()        
        values = (self.account_name, self.password, self.customer_name, self.tab_value)
        c.execute("INSERT INTO customers VALUES (?,?,?,?)", values)
                
        con.commit()        
        con.close()          
           
        
    '''Saves the buy somewhere'''    
    def save_buy(self):
        pass
    
    '''Gets the items that the customer has bought, prob dict with item ids as keys'''
    def load_buy_history(self):
        pass
    
    '''returns the n most bought items'''
    def n_most_bought(self):
        pass
    
    '''customer pays money to the tab'''
    def pay_tab(self, amount):
        self.tab_value = self.tab_value + amount
    
    
    '''customer buys something using the tab'''
    def add_to_tab(self, amount):
        self.tab_value = self.tab_value - amount
    
    
    '''Updates the customers tab_value in the database'''
    def update_tab_value(self):
        con = sqlite3.connect(full_path)
        
        c = con.cursor()               
        c.execute("UPDATE customers SET tab_value=? WHERE account_name=?", (self.tab_value, self.account_name))
                
        con.commit()        
        con.close()
    
    
    
    
    