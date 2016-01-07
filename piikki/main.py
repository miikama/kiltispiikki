from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
import piikki_utilities
import customer 

Builder.load_file('piikki.kv')


class MenuScreen(Screen):
    pass   
  
class LoginScreen(Screen):
    pass

class AccountScreen(Screen):
    
    def __init__(self, **kv):
        Screen.__init__(self, **kv)
        
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
            cust = customer.Customer(acc_name, given_name, family_name, password1)
            if not cust.account_exists():
                cust.write_new_account()
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
            
    
    
    
            
class BuyScreen(Screen):
    
    
    def __init__(self, **kv):
        Screen.__init__(self, **kv)
        self.item_list = piikki_utilities.update_item_list()
        container = self.ids.buy_item_list
        for item in self.item_list:
            texts = item.name[0].upper() + item.name[1:] + "\n" + str(item.price)
            container.add_widget(ItemButton(text = texts,
                                 background_normal = item.normal_background,
                                 background_down = item.pressed_background))
    
    
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
        
        
class FileScreen(Screen):
    pass  
        
  
  
sm = ScreenManager()
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(AccountScreen(name="account"))
sm.add_widget(BuyScreen(name="osto"))
sm.add_widget(AdminScreen(name="admin"))
sm.add_widget(FileScreen(name="select"))

        
class PiikkiApp(App):    
    

    def build(self):
        return sm

if __name__ == '__main__':
    PiikkiApp().run()

