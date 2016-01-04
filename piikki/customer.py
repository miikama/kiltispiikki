



'''handling of customers'''
class customer():
    
    def __init__(self, account_name, given_name, family_name, password):
        
        '''making the names have same format John Doe'''
        self.customer_name = given_name + " " + family_name
        if given_name.length > 1 and family_name.length > 1:
            self.customer_name = given_name[0].upper() + given_name[1:].lower() + " " + family_name[0].upper() + family_name[1:].lower()
        self.account_name = name
        self.password = password
        self.tab_value = 0
        
        file = open("customers.txt", "a")    
        
        file.write("{},{},{},{},{}\n".format(self.account_name,self.password, self.customer_name, self.tab_value))
        file.close()
    
    
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
