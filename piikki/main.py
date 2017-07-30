
#config has to be first import and set before anything else
from kivy.config import Config
   
#Config.read("~/.kivy/config.ini")
Config.set('kivy', 'keyboard_mode', 'systemanddock')


from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import BorderImage
from kivy.logger import Logger

from kivy.properties import ObjectProperty
from piikki_utilities import  ItemHandler, Settings
from customer import CustomerHandler, Customer
from popups import *
import os

Builder.load_file('piikki.kv')



button_color = (0.26, 0.43, 0.56,1)
button_font_color = (0, 0, 0, 1)
button_font_size = 26


'''MenuScreen is the landing screen of the app'''
class MenuScreen(Screen):
    pass
 
'''LoginScreen is used for login'''  
class LoginScreen(Screen):
    
    def __init__(self, **kv):
        super(LoginScreen, self).__init__(**kv)
        self.main_app = kv['main_app']
        self.selected_account = None	    
        
        self.test_button = Button(text="press")
        
        filter_chars = "abcdefghijklmnopqrstuwxyzo"
        self.init_filter_buttons(filter_chars)
        
    

    #implements a method for kivy screen
    def on_pre_enter(self):
        if self.main_app.customer_handler.customers:    
            for cust in self.main_app.customer_handler.customers:
                self.make_account_button(cust)

    def on_leave(self):                
        self.ids.account_list.clear_widgets()   
        self.unselect_account()
        self.ids.filter_input_label.text = ""
        
    def make_account_button(self,customer):
	button = AccountButton(customer, text = customer.account_name)
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
        
        
    #filter visible account based on the text on filter_input_label
    def filter_account_buttons(self):
	filter_text = self.ids.filter_input_label.text
        self.ids.account_list.clear_widgets()   
	for cust in self.main_app.customer_handler.customers:
	    if filter_text in cust.account_name:
		self.make_account_button(cust)
	
        
    
    #initializes filter buttons for names
    def init_filter_buttons(self, char_list):
	for char in char_list:
	    butt = Button(text=char, font_size=button_font_size,
			    background_normal='', color= button_font_color,
                            background_color = button_color )
	    butt.bind(on_release=self.on_filter_button_press)
	    self.ids.filter_button_container.add_widget(butt)
	    
	    
	    
    def on_filter_button_press(self, button):
	self.ids.filter_input_label.text += button.text
	self.filter_account_buttons()
	
    def on_remove_filter_text(self):
	self.ids.filter_input_label.text = self.ids.filter_input_label.text[0:-1] 
	self.filter_account_buttons()
        

'''AccountScreen is used for creating a new accouont'''
class AccountScreen(Screen):
    
    def __init__(self, **kv):
        Screen.__init__(self, **kv)
        self.main_app = kv['main_app']  
        self.acc_name_input =self.main_app.add_input(self.ids.acc_name_container)
        self.given_name_input = self.main_app.add_input(self.ids.given_name_container)
        self.family_name_input = self.main_app.add_input(self.ids.family_name_container)
        #self.password1 = self.main_app.add_input(self.ids.password1_container, True)
        #self.password2 = self.main_app.add_input(self.ids.password2_container, True)
        self.acc_name_input.bind(on_text_validate=self.on_enter_press)
        self.given_name_input.bind(on_text_validate=self.on_enter_press)
        self.family_name_input.bind(on_text_validate=self.on_enter_press)

    #function for handling enter presses when writing
    def on_enter_press(self,instance):
	self.create_account()
       
    #function called when new account is created. Validates text inputs and creates customer through in customer_handler
    def create_account(self):
        acc_name = self.acc_name_input.text
        given_name = self.given_name_input.text
        family_name = self.family_name_input.text
        #password1 = self.password1.text
        #password2 = self.password2.text
        
        warning_label = self.ids.warning_label
                
        if acc_name == "" or given_name == "" or family_name == "":
            warning_label.text = "Please fill in all the information"
#        elif password1 != password2:
#            warning_label.text = "The passwords have to match"
        else:
            '''making the names have format John Doe'''
            customer_name = given_name + " " + family_name
            if len(given_name) > 1 and len(family_name) > 1:
                customer_name = given_name[0].upper() + given_name[1:].lower() + " " + family_name[0].upper() + family_name[1:].lower()
                
            cust = Customer(acc_name, customer_name, encode=True)
            if self.main_app.customer_handler.account_row(acc_name) == None :
                self.main_app.customer_handler.create_new_account(cust)
                warning_label.text = "Account created"
            else:  warning_label.text = ("account exists already")
            
        
    
        def empty_warning():
            warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 7)

    def clear_fields(self):
        self.acc_name_input.text = ""
        self.given_name_input.text = ""
        self.family_name_input.text = ""
                 
    
'''BuyScreen displays the items in sale and handles buy transactions'''            
class BuyScreen(Screen):
    
    
    def __init__(self, **kv):        
        super(BuyScreen, self).__init__( **kv)
        self.main_app = kv['main_app']
        self.selected_item = None 
        self.pressed_button = None
        self.button_list = []
              
        self.item_list = self.main_app.item_handler.get_items()
                
        #just sort the items based on class
        self.item_list.sort(key=lambda x: x.item_class, reverse=True)
        self.show_all_items()
        self.init_filter_buttons("abcdefghijklmnopqrstuwxyz")
        
    def on_pre_enter(self):
        self.ids.account_label.text = self.main_app.current_customer.account_name
        self.ids.tab_value_label.text = str(self.main_app.current_customer.tab_value)
        self.ids.tab_value_label.color = self.tab_color()
        self.update_item_list()
        self.show_most_bought()
        self.show_all_items()
        
    def update_item_list(self):
        self.item_list = self.main_app.item_handler.update_item_list()   
    
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
        
    def clear_button_list(self):
        self.button_list=[]    
        
    def show_all_items(self):
        if len(self.item_list) == 0: pass
        else:
            container = self.ids.buy_item_list
            container.clear_widgets()
            self.clear_button_list()
            self.unselect_items()
            for item in self.item_list:
                button = ItemButton(item, text = "",
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
            most_bought = self.main_app.customer_handler.most_bought(self.main_app.current_customer)
            if most_bought:
                most_bought_list = [x[0] for x in most_bought]
                most_bought_list = filter(lambda x: self.item_exists_update_price(x), most_bought_list)
                container = self.ids.most_bought_item_list
                container.clear_widgets()
                for item in most_bought_list:
                    button = ItemButton(item, text = "",
                                         background_normal = item.normal_background,
                                         background_down = item.pressed_background)
                    self.main_app.get_screen("test").ids.test_label3.text = item.normal_background
                    button.bind(on_press=self.select_item)
                    self.button_list.append(button)
                    container.add_widget(button)     
                    
    
    #filter visible products based on the text on product_filter_label
    def filter_products(self):
	filter_text = self.ids.product_filter_label.text
	if self.item_list == None: pass
        else:
            container = self.ids.buy_item_list
            container.clear_widgets()
            self.unselect_items()
            for item in self.item_list:
		if filter_text in item.name:
		    button = ItemButton(item, text = "",
					background_normal = item.normal_background,
					background_down = item.pressed_background)
		    button.bind(on_press=self.select_item)
		    self.button_list.append(button)
		    container.add_widget(button)
	
        
    
    #initializes filter buttons for names
    def init_filter_buttons(self, char_list):
	for char in char_list:
	    butt = Button(text=char, font_size=16,
			    background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png')
	    butt.bind(on_release=self.on_filter_button_press)
	    
	    self.ids.product_filter_button_container.add_widget(butt)
	    #with butt.canvas.before:
	#	border_image = BorderImage( size=(butt.width, butt.height),
	#		    pos=(butt.x, butt.y),  border=(10, 10, 10, 10),
	#		    source='kuvat/musta_reuna.png')
	    
    #determines what happens, when buttons with letters for filtering are pressed
    def on_filter_button_press(self, button):
	self.ids.product_filter_label.text += button.text
	self.filter_products()
	
    #determines what happens when backspace is used
    def on_remove_filter_text(self):
	self.ids.product_filter_label.text = self.ids.product_filter_label.text[0:-1] 
	self.filter_products()

 
        
        
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
            self.main_app.customer_handler.pay_from_tab(self.main_app.current_customer, self.selected_item.price)
            self.main_app.customer_handler.save_buy(self.main_app.current_customer, self.selected_item)
            self.update_screen()

    def buy_and_exit(self):
        if self.selected_item == None: pass
        else:
            self.main_app.customer_handler.pay_from_tab(self.main_app.current_customer, self.selected_item.price)
            self.main_app.customer_handler.save_buy(self.main_app.current_customer, self.selected_item)
            self.to_login_and_logout()
            
    #in most bought this is used to check whether item exists and if it does, update price            
    def item_exists_update_price(self,item):
        for it in self.item_list:
            if it.name == item.name:
                item.price = it.price
                return True
        return False
            
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
                self.main_app.customer_handler.pay_to_tab(self.main_app.current_customer, float(tab_input.text))
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
        

            
'''Screen used for admin stuff, such as adding new items, viewing tabs and changing item prices
    Actually settings'''
class AdminScreen(Screen):
    
    
    def __init__(self,  **kv):
        Screen.__init__(self,  **kv)
        self.main_app = kv['main_app'] 


'''AccManageScreen is used by admin to monitor and change accounts balances and 
to remove accounts'''        
class AccManageScreen(Screen):
    
    def __init__(self, **kv):
        super(AccManageScreen, self).__init__(**kv)
        self.main_app = kv['main_app']        
        
    def on_pre_enter(self):
        for cust in self.main_app.customer_handler.customers:
            layout = CustomerLayout(cust, self.ids.customer_container)
            self.ids.customer_container.add_widget(layout)
            
    def on_leave(self):
        self.ids.customer_container.clear_widgets()
        
    def confirm_replace_cust_db(self):
        p = ConfirmationPopup(self.main_app.customer_handler.replace_customer_db,
                              "Are you sure you wish to replace the current customers?")
        p.open()
        
    def confirm_backup_customers(self):
        p = ConfirmationPopup(self.main_app.customer_handler.backup_customers,
                              "Do you wish to backup your customer db? (by uploading to drive)")
        p.open()
        

'''FileManageScreen is used by admin to add, delete and update items'''
class ItemManageScreen(Screen):
    
    def __init__(self, **kv):
        super(ItemManageScreen, self).__init__( **kv)
        self.main_app = kv['main_app']
        
        for item in self.main_app.item_handler.item_list:
            layout = ManageItemLayout(item, self.ids.item_manage_container)
            self.ids.item_manage_container.add_widget(layout)
            
        self.ids.item_manage_container.add_widget(AddItemLayout(self.ids.item_manage_container))
        
    def add_one_item(self, item):
        last_widget = self.ids.item_manage_container.children[0] #might not work always
        Logger.info('ItemManageScreen: OBS last widget to be removed {}'.format(last_widget))
        self.ids.item_manage_container.remove_widget(last_widget)        
        self.ids.item_manage_container.add_widget(ManageItemLayout(item,self.ids.item_manage_container))
        self.ids.item_manage_container.add_widget(AddItemLayout(self.ids.item_manage_container))

    def add_item(self):        
        p = AddItemPopup(self)    
        p.open()   
        
        
'''FileScreen is used to select item paths from the device'''        
class FileScreen(Screen):
    pass  

class TestScreen(Screen):
    
    def __init__(self, **kv):
        super(TestScreen, self).__init__(**kv)
        self.app = App.get_running_app()
        
        
class CustomerLayout(BoxLayout):
    customer = ObjectProperty(None)
    
    def __init__(self, customer, container, **kv):
        self.customer = customer
        self.container = container
        super(CustomerLayout, self).__init__(**kv)

        for child in self.children[int(len(self.children)/2):int(len(self.children))]:
            self.remove_widget(child)
            
    def update_tab_value(self):
        p = UpdateCustomerTabPopup(self, self.customer)
        p.open()
    
    def confirm_delete_customer(self):
        title = 'Do you wish to remove account for {} ?'.format(self.customer.customer_name)
        p = ConfirmationPopup(self.delete_customer, title)
        p.open()
        
    def delete_customer(self):
        App.get_running_app().man.customer_handler.delete_customer(self.customer)
        self.container.remove_widget(self) 
        
class ManageItemLayout(BoxLayout):
    
    item = ObjectProperty(None)
    container = ObjectProperty(None)
    
    def __init__(self, item, container, **kv):
        self.item = item
        self.container = container
        BoxLayout.__init__(self, **kv)
        
        #for some reason all objects in kivy file are added twice, remove duplicates
        for child in self.children[4:9]:
            self.remove_widget(child)
            
    def confirm_delete_item(self):
        title = 'Do you wish to delete {}?'.format(self.item.name)
        p = ConfirmationPopup(self.delete_item, title)
        p.open()
        
    def delete_item(self):
        App.get_running_app().man.item_handler.delete_item(self.item)
        self.container.remove_widget(self)
    
    def update_item_price(self):        
        p = UpdateItemPopup(self,self.item)    
        p.open()
        
            
class AddItemLayout(BoxLayout):
    
    container = ObjectProperty(None)
    
    def __init__(self,container, **kv):
        self.container = container
        super(AddItemLayout, self).__init__(**kv)
        
        #stupid bug again
        for child in self.children[int(len(self.children)/2):int(len(self.children))]:
            self.remove_widget(child)   
            
            
class MyInputListener(Widget):
    
    def __init__(self, parent_screen, **kv):
	super(MyInputListener,self).__init__(**kv)
	#self.orientation = "vertical"
	#self.data_label = Label(text="saaas")
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
	    print(self._keyboard.widget)
        #self._keyboard.bind(on_key_down=self._on_keyboard_down)
        #self.add_widget(self.data_label)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
	pass
        #self.data_label.text = self.data_label.text
        
        
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
        
        from kivy.utils import platform
        if platform == 'android':
            path = self.app.user_data_dir             
        else:
            path = os.getcwd()  
        
        self.current_customer = None
        self.customer_handler = CustomerHandler(path)
        self.item_handler = ItemHandler(path)
        

        self.add_widget(MenuScreen(name="menu", main_app = self))
        self.add_widget(TestScreen(name="test", main_app=self))
        self.add_widget(LoginScreen(name="login", main_app = self))
        self.add_widget(AccountScreen(name="account", main_app = self))
        self.add_widget(CustomerScreen(name="customer", main_app = self))
        self.add_widget(BuyScreen(name="osto", main_app = self))
        self.add_widget(AdminScreen(name="admin", main_app = self))
        self.add_widget(AccManageScreen(name='acc_manage', main_app = self))
        self.add_widget(ItemManageScreen(name='item_manage', main_app = self))
        self.add_widget(FileScreen(name="select", main_app = self))
        
    
    #add a text input to a given container, used by multiple screens
    def add_input(self, container, passw=False):
        text_input = TextInput(password=passw)
	text_input.write_tab = False
	text_input.multiline = False
        container.add_widget(text_input)
        return text_input
  
       
        

'''Finally the main app class used by kivy'''        
class PiikkiApp(App):  
    

    def check_back_up(self):
        if self.settings.time_to_backup():
            self.man.customer_handler.backup_customers()
 
    
    def build(self):
        self.man = PiikkiManager(piikki_app = self)
        self.settings = Settings(os.getcwd())
        self.check_back_up()
        Clock.schedule_interval(lambda dt: self.check_back_up(), 40000)
        
        return self.man

if __name__ == '__main__':
    PiikkiApp().run()

