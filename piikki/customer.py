

def load_customers():
    
    customers = []
    
    file = open("customers.txt", "r")    
    file.readline() #reads the first line
    
    for line in file:
        splitline = line.split(",")
        firstname = splitline[1].split(" ")[0]
        secondname = splitline.split(" ")[1]
        customers.append(Customer(splitline[0], firstname, secondname, splitline[2], tab_value= splitline[3]))
    
    print(customers[1].customer_name)
    file.close()

'''handling of customers'''
class Customer():
    
    def __init__(self, account_name, given_name, family_name, password, tab_value = 0):
        
        '''making the names have same format John Doe'''
        self.customer_name = given_name + " " + family_name
        if len(given_name) > 1 and len(family_name) > 1:
            self.customer_name = given_name[0].upper() + given_name[1:].lower() + " " + family_name[0].upper() + family_name[1:].lower()
        self.account_name = account_name
        self.password = password
        self.tab_value = tab_value
        
       
    
    def write_new_account(self):
        file = open("customers.txt", "a")    
        
        file.write("{},{},{},{}\n".format(self.account_name,self.password, self.customer_name, self.tab_value))
        file.close()
    
    # @return True if an account with same account name is already in database 
    def account_exists(self):
        file = open("customers.txt", "r")
        file.readline()
        
        for line in file:
            splitline = line.split(",")
            if splitline[0] == self.account_name:
                return True
        
        return False
    
    
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
