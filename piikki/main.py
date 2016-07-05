from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from piikki_utilities import  ItemHandler
from jnius import autoclass
import os
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
            self.manager.get_screen("osto").update_screen_entering()
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
            self.manager.get_screen("customer").update_screen()
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
        self.acc_name_input =self.main_app.add_input(self.ids.acc_name_container)
        self.given_name_input = self.main_app.add_input(self.ids.given_name_container)
        self.family_name_input = self.main_app.add_input(self.ids.family_name_container)
        self.password1 = self.main_app.add_input(self.ids.password1_container, True)
        self.password2 = self.main_app.add_input(self.ids.password2_container, True)
        
    def create_account(self):
        acc_name = self.acc_name_input.text
        given_name = self.given_name_input.text
        family_name = self.family_name_input.text
        password1 = self.password1.text
        password2 = self.password2.text
        
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
        self.acc_name_input.text = ""
        self.given_name_input.text = ""
        self.family_name_input.text = ""
        self.password1.text = ""
        self.password2.text = ""      
                 
    
'''BuyScreen displays the items in sale and handles buy transactions'''            
class BuyScreen(Screen):
    
    
    def __init__(self, **kv):        
        super(BuyScreen, self).__init__( **kv)
        self.main_app = kv['main_app']
        self.selected_item = None 
        self.pressed_button = None
        self.button_list = []
              
        self.item_list = self.main_app.item_handler.item_list
                
        #just sort the items based on class
        self.item_list.sort(key=lambda x: x.item_class, reverse=True)
        self.show_all_items()
        
    def update_item_list(self):
        self.item_list = self.main_app.item_handler.update_item_list()
        
    def update_screen_entering(self):
        self.ids.account_label.text = self.main_app.current_customer.account_name
        self.ids.tab_value_label.text = str(self.main_app.current_customer.tab_value)
        self.ids.tab_value_label.color = self.tab_color()
        self.show_most_bought()
    
    '''Updates the customer account name and the tab value when entering the screen and when needed'''
    def update_screen(self):
        self.ids.account_label.text = self.main_app.current_customer.account_name
        self.ids.tab_value_label.text = str(self.main_app.current_customer.tab_value)
        self.ids.tab_value_label.color = self.tab_color()
    
    '''Changes the current customer of the app to None, unselects the items, and swithces screens to login screen'''
    def to_login_and_logout(self):
        self.main_app.current_customer = None
        self.unselect_items()
        self.manager.transition.direction="right"                     
        self.manager.current = "login"
        
    def show_all_items(self):
        if len(self.item_list) == 0: pass
        else:
            container = self.ids.buy_item_list
            container.clear_widgets()
            self.unselect_items()
            for item in self.item_list:
                button = ItemButton(item, text = item.name,
                                     background_normal = item.normal_background,
                                     background_down = item.pressed_background)
                button.bind(on_press=self.select_item)
                self.button_list.append(button)
                container.add_widget(button)
            
    def show_candy(self):
        if self.item_list == None: pass
        else:
            candy_list = filter(lambda x: x.item_class == "Candy", self.item_list)
            container = self.ids.buy_item_list
            container.clear_widgets()
            self.unselect_items()
            for item in candy_list:
                button = ItemButton(item, text = "",
                                     background_normal = item.normal_background,
                                     background_down = item.pressed_background)
                button.bind(on_press=self.select_item)
                self.button_list.append(button)
                container.add_widget(button)
    
    def show_soft_drinks(self):
        if self.item_list == None: pass
        else:
            drink_list = filter(lambda x: x.item_class == "Soft drink", self.item_list)
            container = self.ids.buy_item_list
            container.clear_widgets()
            self.unselect_items()
            for item in drink_list:
                button = ItemButton(item, text = "",
                                     background_normal = item.normal_background,
                                     background_down = item.pressed_background)
                button.bind(on_press=self.select_item)
                self.button_list.append(button)
                container.add_widget(button)
    
    def show_food(self):
        if self.item_list == None: pass
        else:
            food_list = filter(lambda x: x.item_class == "Food", self.item_list)
            container = self.ids.buy_item_list
            container.clear_widgets()
            self.unselect_items()
            for item in food_list:
                button = ItemButton(item, text = "",
                                     background_normal = item.normal_background,
                                     background_down = item.pressed_background)
                button.bind(on_press=self.select_item)
                self.button_list.append(button)
                container.add_widget(button)
        
    def show_most_bought(self):
        if len(self.item_list) == 0 or self.main_app.current_customer == None: pass
        else:
            most_bought = self.main_app.current_customer.most_bought()
            if most_bought:
                most_bought_list = [x[0] for x in most_bought]
                container = self.ids.most_bought_item_list
                container.clear_widgets()
                for item in most_bought_list:
                    button = ItemButton(item, text = item.name,
                                         background_normal = item.normal_background,
                                         background_down = item.pressed_background)
                    self.main_app.get_screen("test").ids.test_label3.text = item.normal_background
                    button.bind(on_press=self.select_item)
                    self.button_list.append(button)
                    container.add_widget(button)     

 
        
        
    def select_item(self, button):
        if self.selected_item == None:
            button.background_normal = button.item.pressed_background
            self.selected_item = button.item
            self.pressed_button = button
            self.ids.product_name_label.text = button.item.name
            self.ids.product_price_label.text = str(button.item.price)
            
        elif self.selected_item == button.item:
            button.background_normal = button.item.normal_background
            self.selected_item = None
            self.pressed_button = None
            self.ids.product_name_label.text = ""
            self.ids.product_price_label.text = ""
            
        else:
            self.pressed_button.background_normal = self.selected_item.normal_background
            button.background_normal = button.item.pressed_background
            self.selected_item = button.item
            self.pressed_button = button
            self.ids.product_name_label.text = button.item.name
            self.ids.product_price_label.text = str(button.item.price)
        
    def unselect_items(self):
        for button in self.button_list:
            button.background_normal = button.item.normal_background
        self.selected_item = None
        self.ids.product_name_label.text =""
        self.ids.product_price_label.text = ""
    
    def buy_item(self):
        if self.selected_item == None: pass
        else:
            self.main_app.current_customer.pay_from_tab(self.selected_item.price)
            self.main_app.current_customer.save_buy(self.selected_item)
            self.update_screen()

    def buy_and_exit(self):
        if self.selected_item == None: pass
        else:
            self.main_app.current_customer.pay_from_tab(self.selected_item.price)
            self.to_login_and_logout()
            
    def tab_color(self):        
        tab = self.main_app.current_customer.tab_value 
        if tab >= 5.0:
            return (0,1,0,1)
        elif tab < 5.0 and tab >=0:  
            return (1,1,0,1)
        else:
            return (1,0,0,1)
        
        
'''CustomerScreen allows customers to add value to the tab and see their balance history'''
class CustomerScreen(Screen):
    
    def __init__(self, **kv):
        super(CustomerScreen, self).__init__(**kv)
        self.main_app = kv['main_app'] 
        self.add_tab_input = self.main_app.add_input(self.ids.add_tab_input_container)
        
    def add_to_tab(self):
        tab_input = self.add_tab_input
        try:
            if tab_input.text == "" or float(tab_input.text) >150.0:
                self.ids.warning_label.text = "Please enter a proper amount"
            else:
                self.main_app.current_customer.pay_to_tab(float(tab_input.text))
                self.update_screen()
                self.ids.warning_label.text = "Added {} succesfully to your tab".format(float(tab_input.text))
                tab_input.text= ""
        except ValueError:
            self.ids.warning_label.text = "Please enter a proper amount"
            
        
        def empty_warning():
            self.ids.warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)
        
    def on_leave_screen(self):
        self.main_app.selected_customer = None
        self.ids.account_label.text = ""
        self.ids.tab_value_label.text = ""
    
    def update_screen(self):
        self.ids.account_label.text = self.main_app.current_customer.account_name
        self.ids.tab_value_label.text = str(self.main_app.current_customer.tab_value)
        self.ids.tab_value_label.color = self.tab_color()
            
    def tab_color(self):        
        tab = self.main_app.current_customer.tab_value 
        if tab >= 5.0:
            return (0,1,0,1)
        elif tab < 5.0 and tab >=0:  
            return (1,1,0,1)
        else:
            return (1,0,0,1)  
        

            
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
        self.price_input = self.main_app.add_input(self.ids.price_input_container)
        self.name_input = self.main_app.add_input(self.ids.name_input_container)
    
    
    def add_item(self):
        warning_label = self.ids.warning_label
        name = self.name_input.text
        price = ""
        try: price = float(self.price_input.text)
        except ValueError: warning_label.text = "Invalid input, use the dot"
        file_name = self.ids.image_input.text
        item_class = self.ids.dropdown_button.text       
        
        if name == "" or price == "" or file_name == "" or item_class == "No class selected":
            warning_label.text = "Please fill all the needed information"
        else:                    
            self.main_app.item_handler.add_item(name,price, file_name, item_class)
            self.name_input.text = ""
            self.price_input.text = ""
            self.ids.image_input.text = ""    
            self.manager.get_screen("osto").update_item_list()
            warning_label.text = "{} added succesfully".format(name)
            
        def empty_warning():
            warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)

        
'''FileScreen is used to select item paths from the device'''        
class FileScreen(Screen):
    pass  

class TestScreen(Screen):
    
    def __init__(self, **kv):
        super(TestScreen, self).__init__(**kv)
        self.main_app = kv['main_app']
        
    def vibrate(self):
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        activity = PythonActivity.mActivity
        vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator.hasVibrator():
            vibrator.vibrate(100)
        else:
            print("no vibrator")
        
        
        
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
        self.app = kv['piikki_app']
        #pc
        path = os.getcwd()
        #android
        #path = self.app.user_data_dir               
        
        self.current_customer = None
        customer.full_path = path
        customer.db_path = os.path.join(path, "piikki.db")   #to be changed from global variable to handler class
        customer.enable_databases()
        self.customer_list = customer.load_customers()
        self.item_handler = ItemHandler(path)

        self.add_widget(MenuScreen(name="menu", main_app = self))
        self.add_widget(TestScreen(name="test", main_app=self))
        self.add_widget(LoginScreen(name="login", main_app = self))
        self.add_widget(AccountScreen(name="account", main_app = self))
        self.add_widget(CustomerScreen(name="customer", main_app = self))
        self.add_widget(BuyScreen(name="osto", main_app = self))
        self.add_widget(AdminScreen(name="admin", main_app = self))
        self.add_widget(FileScreen(name="select", main_app = self))
    
    #add a text input to a given container, used by multiple screens
    def add_input(self, container, passw=False):
        text_input = TextInput(password=passw)
        container.add_widget(text_input)
        return text_input
  
       
        

'''Finally the main app class used by kivy'''        
class PiikkiApp(App):    
    
 
    
    def build(self):
        self.man = PiikkiManager(piikki_app = self)

    
        self.man.get_screen("test").ids.test_label1.text = self.user_data_dir
        self.man.get_screen("test").ids.test_label2.text = os.getcwd()
        #self.man.get_screen("test").ids.test_label3.text = os.path.join(os.getcwd(), "piikki.db")
        
        return self.man

if __name__ == '__main__':
    PiikkiApp().run()

