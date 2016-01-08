import sqlite3
import os


'''Loads all customers from a text file'''
def load_customers():
    
    customers = []
    
    file = open("customers.txt", "r")    
    file.readline() #reads the first line
    
    for line in file:
        splitline = line.split(",")      
        tab_value = float(splitline[3][:-1])
        customers.append(Customer(splitline[0],splitline[1], splitline[2], tab_value))
    
    print(customers[0].password)
    file.close()
    
    return customers



'''Returns row number where the account is in the database or None if it doesn't exist''' 
def account_row(name):
        path = os.getcwd()
        db_file = "piikki.db"
        full_path = "{}/{}".format(path, db_file)
        
        con = sqlite3.connect(full_path)        
        c = con.cursor()      
        
        c.execute("SELECT rowid FROM customers WHERE account_name = ?", (name,))
        data=c.fetchone()
        con.close()
        if data is None: return None
        else: return data[0]
    
'''Login returns a customer object for given account or None 
    if the account doesn't exist, password isn't needed at the moment''' 
               
def login(account_name):    
    path = os.getcwd()
    db_file = "piikki.db"
    full_path = "{}/{}".format(path, db_file)
    con = sqlite3.connect(full_path)
    
    c = con.cursor()        
    c.execute("SELECT * FROM customers WHERE account_name = ?", (account_name,))
    data = c.fetchone()        
    con.close()
    
    if data == None: return None
    else: return Customer(data[0], data[1],data[2], tab_value=data[3])
    return None
    
    
        

'''class Customer contains functions concerning customers...'''
class Customer():
    

    
    def __init__(self, account_name, password, full_name,  tab_value = 0):
        
        
        self.customer_name = full_name
        self.account_name = account_name
        self.password = password
        self.tab_value = tab_value
        
       
    '''all the data is stored in database piikki.db'''
    def create_new_account(self):
        path = os.getcwd()
        db_file = "piikki.db"
        full_path = "{}/{}".format(path, db_file)
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
    
    
    def update_tab_value(self):
        pass
    
    '''TODO: password identification
            storing bought item history; maybe different text file linking cust id and item id
             '''
