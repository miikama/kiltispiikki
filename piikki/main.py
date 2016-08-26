from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from piikki_utilities import  ItemHandler
from customer import CustomerHandler, Customer
import os

    


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
            
                
    def on_pre_enter(self):
        if self.main_app.customer_handler.customers:    
            for cust in self.main_app.customer_handler.customers:
                button = AccountButton(cust, text = cust.account_name)
                button.bind(on_release=self.select_account)
                self.ids.account_list.add_widget(button)

    def on_leave(self):                
        self.ids.account_list.clear_widgets()   
        self.unselect_account()                    
        
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
                
            cust = Customer(acc_name, customer_name )
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
   
                 
#        dropdown = CustomDropDown()
#        self.dropdown = dropdown
#        mainbutton = self.ids.dropdown_button
#        mainbutton.bind(on_release=dropdown.open)
#        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
#        self.price_input = self.main_app.add_input(self.ids.price_input_container)
#        self.name_input = self.main_app.add_input(self.ids.name_input_container)



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
    
    def update_item_price(self, item):        
        p = UpdateItemPopup(self,item)    
        p.open()
    
    def delete_item(self, item):
        p = DeleteItemPopup(self,item)
        p.open()
        
    def get_itemlayout(self, item):
        for layout in self.ids.item_manage_container.children:
            if isinstance(layout, ManageItemLayout):
                if layout.item.name == item.name:
                    return layout
        return None
        
'''FileScreen is used to select item paths from the device'''        
class FileScreen(Screen):
    pass  

class TestScreen(Screen):
    
    def __init__(self, **kv):
        super(TestScreen, self).__init__(**kv)
        self.app = App.get_running_app()
        
    def test(self):
        self.app.googleClient.connect()
        
class CustomerLayout(BoxLayout):
    customer = ObjectProperty(None)
    
    def __init__(self, customer, container, **kv):
        self.customer = customer
        self.container = container
        super(CustomerLayout, self).__init__(**kv)

        for child in self.children[int(len(self.children)/2):int(len(self.children))]:
            self.remove_widget(child)
            
    def update_tab_value(self,customer):
        Logger.info('AccManageScreen: called update_tab_value')
        p = UpdateCustomerTabPopup(self, customer)
        p.open()
    
    def delete_customer(self, customer):
        p = DeleteCustomerPopup(self,customer)
        p.open()
        
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
            
class AddItemLayout(BoxLayout):
    
    container = ObjectProperty(None)
    
    def __init__(self,container, **kv):
        self.container = container
        super(AddItemLayout, self).__init__(**kv)
        
        #stupid bug again
        Logger.info('AddItemLayout: length of the children {}'.format(len(self.children)))
        for child in self.children:
            Logger.info('AddItemLayout: The child is {}'.format(child))
        for child in self.children[int(len(self.children)/2):int(len(self.children))]:
            self.remove_widget(child)
            
'''Popup created in python side'''
class UpdateCustomerTabPopup(Popup):
    
    def __init__(self,layout, customer, **kv):
        super(UpdateCustomerTabPopup, self).__init__(**kv)
        self.customer_layout = layout
        self.customer =customer
        self.title = 'Set new tab value for {}'.format(customer.customer_name) 
        self.size_hint = (None,None)
        self.size = (300,300)
        b = BoxLayout(orientation='vertical',
                      spacing = 10, padding = 10)
        b.add_widget(Label(text="Current tab value: {}".format(customer.tab_value)))
        self.balance_input = TextInput()
        b.add_widget(self.balance_input)
        self.info_label = Label(size_hint=[1,.1])
        b.add_widget(self.info_label)
        b2 = BoxLayout(orientation='horizontal',spacing=10, padding=10)        
        b2.add_widget(Button(text='Cancel',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.dismiss)) 
        b2.add_widget(Button(text='Confirm', 
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.update_tab_value))               
        b.add_widget(b2)
        self.content = b
        
    def update_tab_value(self, callback):
        if self.balance_input.text.isnumeric():
            App.get_running_app().man.customer_handler.update_tab_value(self.customer, float(self.balance_input.text))
            self.customer_layout.ids.balance_label.text = str(float(self.balance_input.text))
            Logger.info('UpdateCustomerTabPopup: updated customer {}'.format(self.customer.customer_name))
            self.dismiss()       
        else:
            self.info_label.text = "Not valid number"
            Logger.info('UpdateCustomerTabPopup: Not valid number')
            
'''Popup created in python side'''
class DeleteCustomerPopup(Popup):
    
    def __init__(self,layout, customer, **kv):
        super(DeleteCustomerPopup, self).__init__(**kv)
        self.customer_layout = layout
        self.customer = customer
        self.title = 'Do you wish to remove account for {} ?'.format(customer.customer_name)
        self.size_hint = (None,None)
        self.size = (300,300)
        b = BoxLayout(orientation='vertical',
                      spacing = 10, padding = 10)
        b.add_widget(Button(text='Cancel',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.dismiss))      
        b.add_widget(Button(text='Confirm', 
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.confirm))
          
        self.content = b
        
    def confirm(self, callback):

        App.get_running_app().man.customer_handler.delete_customer(self.customer)
        self.customer_layout.container.remove_widget(self.customer_layout) 
        self.dismiss()
        

'''Popup created in python side'''
class UpdateItemPopup(Popup):
    
    def __init__(self,manage_screen,item, **kv):
        super(UpdateItemPopup, self).__init__(**kv)
        self.manage_screen = manage_screen
        self.item =item
        self.title = 'Update item price'
        self.size_hint = (None,None)
        self.size = (300,400)
        b = BoxLayout(orientation='vertical',
                      spacing = 10, padding = 10)
        b.add_widget(Label(text='Give a new price'))
        self.price_input = TextInput(text='With a dot e.g. 0.0')
        b.add_widget(self.price_input)
        b.add_widget(Button(text='Confirm', 
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.confirm))
        b.add_widget(Button(text='Cancel',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.dismiss))
        
        
        self.content = b
        
    def confirm(self, callback):
        new_price=0
        try: 
            new_price = float(self.price_input.text)
            App.get_running_app().man.item_handler.update_item_price(self.item,new_price)
            self.manage_screen.get_itemlayout(self.item).ids.price_label.text = str(new_price)
            
        except ValueError: pass

        self.dismiss()
        
'''Popup created in python side'''
class DeleteItemPopup(Popup):
    
    def __init__(self,manage_screen, item, **kv):
        super(DeleteItemPopup, self).__init__(**kv)
        self.parent_screen = manage_screen
        self.item =item
        self.title = 'Do you wish to delete {}'.format(item.name)
        self.size_hint = (None,None)
        self.size = (300,300)
        b = BoxLayout(orientation='vertical',
                      spacing = 10, padding = 10)
        b.add_widget(Button(text='Confirm', 
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.confirm))
        b.add_widget(Button(text='Cancel',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.dismiss))        
        self.content = b
        
    def confirm(self, callback):

        App.get_running_app().man.item_handler.delete_item(self.item)
        layout_to_delete = self.parent_screen.get_itemlayout(self.item)
        Logger.info('DeleteitemPopup: the layout: {}'.format(layout_to_delete))
        if layout_to_delete != None:
            self.parent_screen.ids.item_manage_container.remove_widget(self.parent_screen.get_itemlayout(self.item))
        else:
            Logger.info('DeleteItemPopup: could not find layout to be deleted')
        self.dismiss()
        

'''Popup created in python side'''
class AddItemPopup(Popup):
    
    def __init__(self, manage_screen, **kv):
        super(AddItemPopup, self).__init__(**kv)
        self.parent_screen = manage_screen
        self.title = 'Add a new item'
        self.size_hint = (None,None)
        self.size = (400,400)
        self.auto_dismiss = False
        self.selected_type = None
        b = BoxLayout(orientation='vertical',
                      spacing = 10, padding = 10)
        self.name_input = TextInput(text='Name of the item')
        self.price_input = TextInput(text='Price e.g. 0.0')
        self.dropdown = CustomDropDown()
        b1 = BoxLayout(spacing = 10)
        self.soft_drink_button = Button(text = 'Soft drink',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.select_type)
        self.candy_button = Button(text = 'Candy',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.select_type)
        self.food_button = Button(text = 'Food',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.select_type)
        self.warning_label = Label()
        l1 = Label(text='file name \'kuva.png\', in home/user/Pictures/')
        self.path_input = TextInput(text='~/Pictures/*')
        b1.add_widget(self.soft_drink_button)
        b1.add_widget(self.candy_button)
        b1.add_widget(self.food_button)
        b.add_widget(self.name_input)
        b.add_widget(self.price_input)
        b.add_widget(Label(text='Select item type'))
        b.add_widget(b1)
        b.add_widget(l1)
        b.add_widget(self.path_input)
        b2 = BoxLayout(spacing = 10)
        b2.add_widget(Button(text='Cancel',
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.dismiss))
        b2.add_widget(Button(text='Add item', 
                            background_normal='kuvat/nappi_tausta.png',
                            background_down='kuvat/nappi_tausta_pressed.png',
                            on_release=self.confirm))
        b.add_widget(self.warning_label)
        b.add_widget(b2)
        
        
        self.content = b
        
    def confirm(self, callback):
        price=0
        name = self.name_input.text
        pictures = os.path.join(os.path.expanduser("~"), "Pictures")
        file_name = os.path.join(pictures, self.path_input.text)
        Logger.info('AddItemPopup: file path for picture {}'.format(file_name))
        item_class = self.selected_type
        
        try: 
            price = float(self.price_input.text)        
            if name == "" or price == "" or file_name == "" or item_class == None:
                self.warning_label.text = "Please fill all the needed information"
            elif not os.path.isfile(file_name):
                self.warning_label.text = "picture does not exist"
            else:
                #where the update happens
                sm = App.get_running_app().man
                it = sm.item_handler.add_item(name, price,
                                             file_name, item_class)
                self.parent_screen.add_one_item(it)
                self.dismiss()
        except ValueError: self.warning_label.text = "Invalid input, use the dot"
        
        def empty_warning():
            self.warning_label.text = ""        
        Clock.schedule_once(lambda dt: empty_warning(), 5)
        
    #just manually unselect all and select the pressed button
    def select_type(self, *args):        
        self.soft_drink_button.background_normal='kuvat/nappi_tausta.png'
        self.candy_button.background_normal = 'kuvat/nappi_tausta.png'
        self.food_button.background_normal = 'kuvat/nappi_tausta.png'
        args[0].background_normal = 'kuvat/nappi_tausta_pressed.png'
        self.selected_type = args[0].text
        
        
        
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
        
        #customer.full_path = path
        #customer.db_path = os.path.join(path, "piikki.db")   #to be changed from global variable to handler class
        #self.customer_list = customer.load_customers()
        self.customer_handler = CustomerHandler(path)
        self.customer_handler.enable_databases()
        self.customer_handler.load_customers()        
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
        container.add_widget(text_input)
        return text_input
  
       
        

'''Finally the main app class used by kivy'''        
class PiikkiApp(App):  
    

    
 
    
    def build(self):
        self.man = PiikkiManager(piikki_app = self)
        
        from gdrive import GoogleClient
        self.googleClient = GoogleClient()

    
        self.man.get_screen("test").ids.test_label1.text = self.user_data_dir
        self.man.get_screen("test").ids.test_label2.text = os.getcwd()
        #self.man.get_screen("test").ids.test_label3.text = os.path.join(os.getcwd(), "piikki.db")
        
        return self.man

if __name__ == '__main__':
    PiikkiApp().run()

