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
        super(LoginScreen, self).__init__(**kv)
        self.main_app = kv['main_app']
        self.selected_account = None
        
        if self.main_app.customer_list == None: pass
        else:
            for cust in self.main_app.customer_list:
                button = AccountButton(cust, text = cust.account_name)
                button.bind(on_release=self.select_account)
                self.ids.account_list.add_widget(button)
                
    def add_account(self, cust):
        button = AccountButton(cust, text = cust.account_name)
        button.bind(on_release=self.select_account)
        self.ids.account_list.add_widget(button)                        
        
    def select_account(self, button):   
        self.selected_account=button.account
        self.ids.account_label.text = button.account.account_name
        self.ids.tab_value_label.text = str(button.account.tab_value)
        self.ids.customer_name_label.text = button.account.customer_name
        self.ids.info_label.text = "Selected account:"
    
    def unselect_account(self):        
        self.selected_account = None
        self.ids.account_label.text = ""
        self.ids.tab_value_label.text = ""
        self.ids.customer_name_label.text = ""
        self.ids.info_label.text = "Please select your account from the list"
        
        
    def login(self):
        warning_label = self.ids.warning_label
        
        if self.selected_account == None:
            warning_label.text = "Please select an account"
        else:
            self.main_app.current_customer = self.selected_account
            self.unselect_account()
            self.manager.get_screen("osto").update_screen()
            self.manager.transition.direction = "left"
            self.manager.current = "osto"           
                
        
        def empty_warning():
            warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)
        
    def view_account(self):
        warning_label = self.ids.warning_label
        
        if self.selected_account == None:
            warning_label.text = "Please select an account"
        else:
            self.main_app.current_customer = self.selected_account
            self.unselect_account()
            self.manager.get_screen("osto").update_screen()
            self.manager.transition.direction = "left"
            self.manager.current = "customer"           
                
        
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
                self.main_app.customer_list.append(cust)
                self.main_app.get_screen("login").add_account(cust)                
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
        super(BuyScreen, self).__init__( **kv)
        self.main_app = kv['main_app']
        self.selected_item = None       
        self.item_list = None

        self.item_list = piikki_utilities.update_item_list()
        container = self.ids.buy_item_list
        if self.item_list == None: pass
        else:
            for item in self.item_list:
                texts = item.name[0].upper() + item.name[1:] + "\n" + str(item.price)
                button = ItemButton(item, text = texts,
                                     background_normal = item.normal_background,
                                     background_down = item.pressed_background)
                button.bind(on_release=self.select_item)
                container.add_widget(button)
    
    def update_screen(self):
        self.ids.account_label.text = self.main_app.current_customer.account_name
        self.ids.tab_value_label.text = str(self.main_app.current_customer.tab_value)
    
    
    def to_menu_and_logout(self):
        self.main_app.current_customer = None
        self.unselect_item()
        self.manager.transition.direction="right"                     
        self.manager.current = "menu"
        
    def select_item(self, button):
        self.selected_item = button.item
        self.ids.product_name_label.text = button.item.name
        self.ids.product_price_label.text = str(button.item.price)
        
    def unselect_item(self):
        self.selected_item = None
        self.ids.product_name_label.text =""
        self.ids.product_price_label.text = ""
    
    def buy_item(self):
        if self.selected_item == None: pass
        else:
            self.main_app.current_customer.add_to_tab(self.selected_item.price)
            self.main_app.current_customer.update_tab_value()
            self.unselect_item()
            self.update_screen()

    def buy_and_exit(self):
        if self.selected_item == None: pass
        else:
            self.main_app.current_customer.add_to_tab(self.selected_item.price)
            self.main_app.current_customer.update_tab_value()
            self.to_menu_and_logout()
            
'''CustomerScreen allows customers to add value to the tab and see their balance history'''
class CustomerScreen(Screen):
    
    def __init__(self, **kv):
        super(CustomerScreen, self).__init__(**kv)
        self.main_app = kv['main_app']
    
            
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


'''ItemButton is used in the BuyScreen to portray the items'''
class ItemButton(Button):
    
    def __init__(self, item, **kv):
        super(ItemButton, self).__init__(**kv)
        self.item = item


'''AccountButton is used in the loginScreen account selection'''
class AccountButton(Button):
    
    def __init__(self,account, **kv):
        Button.__init__(self, **kv)
        self.account = account
        
        
class CustomDropDown(DropDown):
    pass

        
        
'''PiikkiManager is the parent class of every screen and 
    contains data that should be available to all the screens'''  
class PiikkiManager(ScreenManager):  

    def __init__(self, **kv):
        ScreenManager.__init__(self, **kv)
        
        
        self.current_customer = None        
        self.customer_list = customer.load_customers()

        self.add_widget(MenuScreen(name="menu", main_app = self))
        self.add_widget(LoginScreen(name="login", main_app = self))
        self.add_widget(AccountScreen(name="account", main_app = self))
        self.add_widget(CustomerScreen(name="customer", main_app = self))
        self.add_widget(BuyScreen(name="osto", main_app = self))
        self.add_widget(AdminScreen(name="admin", main_app = self))
        self.add_widget(FileScreen(name="select", main_app = self))

        
        
        

'''Finally the main app class used by kivy'''        
class PiikkiApp(App):    
    
    man = PiikkiManager()
        
    
    def build(self):
        #customer.enable_databases()
        return self.man

if __name__ == '__main__':
    PiikkiApp().run()

