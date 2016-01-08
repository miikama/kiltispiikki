from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
import sqlite3
import os
import piikki_utilities
import customer
 

Builder.load_file('piikki.kv')

'''MenuScreen is the landing screen of the app'''
class MenuScreen(Screen):
    pass   
 
'''LoginScreen is used for login'''  
class LoginScreen(Screen):
    
    def __init__(self, **kv):
        Screen.__init__(self, **kv)
        self.main_app = kv['main_app']
        
    def login(self):
        self.main_app.current_customer = None
        warning_label = self.ids.warning_label
        account_name = self.ids.account_name.text
        password = self.ids.password.text
        
        if account_name == "" or password == "":
            warning_label.text = "Please fill all the fields"
        else:
            self.main_app.current_customer = customer.login(account_name)
            if self.main_app.current_customer == None:
                warning_label.text = "No such account"
            else:
                self.manager.transition.direction = "left"
                self.manager.current = "osto"
        
        def empty_warning():
            warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)
        

'''AccountScreen is used for creating a new accouont'''
class AccountScreen(Screen):
    
    def __init__(self, **kv):
        Screen.__init__(self, **kv)
        self.main_app = kv['main_app']    
        
    def create_account(self):
        acc_name = self.ids.acc_name.text
        given_name = self.ids.given_name.text
        family_name = self.ids.family_name.text
        password1 = self.ids.password1.text
        password2 = self.ids.password2.text
        
        warning_label = self.ids.warning_label
                
        if acc_name == "" or given_name == "" or family_name == "" or password1 == "" or password2 == "":
            warning_label.text = "Please fill in all the information"
        elif password1 != password2:
            warning_label.text = "The passwords have to match"
        else:
            '''making the names have format John Doe'''
            customer_name = given_name + " " + family_name
            if len(given_name) > 1 and len(family_name) > 1:
                customer_name = given_name[0].upper() + given_name[1:].lower() + " " + family_name[0].upper() + family_name[1:].lower()
                
            cust = customer.Customer(acc_name,password1, customer_name )
            if customer.account_row(acc_name) == None :
                cust.create_new_account()
                warning_label.text = "Account created"
            else:  warning_label.text = ("account exists already")
            
        
    
        def empty_warning():
            warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)

    def clear_fields(self):
        self.ids.acc_name.text = ""
        self.ids.given_name.text = ""
        self.ids.family_name.text = ""
        self.ids.password1.text = ""
        self.ids.password2.text = ""      
            
    
    
    
'''BuyScreen displays the items in sale and handles buy transactions'''            
class BuyScreen(Screen):
    
    
    def __init__(self, **kv):
        Screen.__init__(self, **kv)
        self.main_app = kv['main_app']    
        
        self.item_list = piikki_utilities.update_item_list()
        container = self.ids.buy_item_list
        for item in self.item_list:
            texts = item.name[0].upper() + item.name[1:] + "\n" + str(item.price)
            container.add_widget(ItemButton(text = texts,
                                 background_normal = item.normal_background,
                                 background_down = item.pressed_background))
    
    
    def to_menu_and_logout(self):
        self.main_app.current_customer = None
        self.manager.transition.direction="right"                     
        self.manager.current = "menu"
    
    def buy_item(self):
        print("painettiin")


class ItemButton(Button):
    pass
        
class CustomDropDown(DropDown):
    pass

'''Screen used for admin stuff, such as adding new items, viewing tabs and changing item prices'''
class AdminScreen(Screen):
    
    
    def __init__(self,  **kv):
        Screen.__init__(self,  **kv)
        self.main_app = kv['main_app']    
                 
        dropdown = CustomDropDown()
        self.dropdown = dropdown
        mainbutton = self.ids.dropdown_button
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
    
    
    def add_item(self):
        name = self.ids.name_input.text
        price = ""
        try: price = float(self.ids.price_input.text)
        except ValueError: pass
        file_name = self.ids.image_input.text
        item_class = self.ids.dropdown_button.text
        
        warning_label = self.ids.warning_label
        
        if name == "" or price == "" or file_name == "" or item_class == "No class selected":
            warning_label.text = "Please fill all the needed information"
        else:                    
            piikki_utilities.add_item(name,price, file_name, item_class)
            
            self.ids.name_input.text = ""
            self.ids.price_input.text = ""
            self.ids.image_input.text = ""            
            warning_label.text = "{} added succesfully".format(name)
            
        def empty_warning():
            warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)
        
'''FileScreen is used to select item paths from the device'''        
class FileScreen(Screen):
    pass  
        
        
'''PiikkiManager is the parent class of every screen and 
    contains data that should be available to all the screens'''  
class PiikkiManager(ScreenManager):  

    def __init__(self, **kv):
        ScreenManager.__init__(self, **kv)

        self.add_widget(MenuScreen(name="menu", main_app = self))
        self.add_widget(LoginScreen(name="login", main_app = self))
        self.add_widget(AccountScreen(name="account", main_app = self))
        self.add_widget(BuyScreen(name="osto", main_app = self))
        self.add_widget(AdminScreen(name="admin", main_app = self))
        self.add_widget(FileScreen(name="select", main_app = self))

        
        self.current_customer = None
        self.all_customers = customer.load_customers()
        

'''Finally the main app class used by kivy'''        
class PiikkiApp(App):    
    
    man = PiikkiManager()
    
    def enable_databases(self):
        path = os.getcwd()
        db_file = "piikki.db"
        full_path = "{}/{}".format(path, db_file)
        con = sqlite3.connect(full_path)
                
        c = con.cursor()        
        c.execute('''CREATE TABLE IF NOT EXISTS customers (account_name text, password text,
         customer_name text, tab_value real)''')
        
        con.commit()        
        con.close()
    
    def build(self):
        self.enable_databases()
        return self.man

if __name__ == '__main__':
    PiikkiApp().run()

