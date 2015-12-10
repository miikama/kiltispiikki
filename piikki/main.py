from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MenuWindow(BoxLayout):
    pass     
  
    


        
class PiikkiApp(App):

    def build(self):
        return MenuWindow()
    

if __name__ == '__main__':
    PiikkiApp().run()

