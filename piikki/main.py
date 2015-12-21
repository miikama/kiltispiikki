from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder


Builder.load_file('piikki.kv')


class MenuScreen(Screen):
    pass     
  
class BuyScreen(Screen):
    pass    
 
    
sm = ScreenManager()
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(BuyScreen(name="osto"))

        
class PiikkiApp(App):

    def build(self):
        return sm
    

if __name__ == '__main__':
    PiikkiApp().run()

