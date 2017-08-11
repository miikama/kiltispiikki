from PIL import Image
from kivy.logger import Logger
from datetime import datetime, timedelta
#import os
#import time

#full_path = os.getcwd()
#full_path = "/sdcard/data"


class Item():
    
    def __init__(self, name, price, item_class, full_path):
        self.name = name
        self.price = price
        self.item_class = item_class #string with value Candy, Soft drink or Food
        self.normal_background = "{}{}{}{}".format(full_path, "/itempics/", name.lower(), "_normal_pic.png")
        self.pressed_background = "{}{}{}{}".format(full_path, "/itempics/",name.lower(), "_pressed_pic.png")
        
class Settings():
    
    def __init__(self, full_path):
        self.full_path = full_path
        self.last_backup = self.read_settings()
        self.time_between_backups = timedelta(days=3)
        
     #TODO problems with multiple computers with different versions of settings.txt and different last backups
    '''reads settings.txt file and return the options as a list 
        (currently only one option so no list)'''       
    def read_settings(self):
        last_backup_date = None
        #make new file if one does not exist
        try:
            file = open(self.full_path + "/settings.txt", "r")           
            #commenting on the settings if the first char is '#'
            
            for line in file:
                if line[0] == '#': continue
                line_wo_newline = line[:-1]
                a = line_wo_newline.split("=")
                if a[0]=='last_backup':
                    last_backup_date = a[1]
                    if last_backup_date == "None":
			last_backup_date = None
			Logger.info("Settings: no last backup based on settings")
                    else:
			last_backup_date = datetime.strptime(last_backup_date, '%d-%m-%Y_%H:%M')
                if a[0]=='days_between_backups':
                    self.time_between_backups=timedelta(days=float(a[1]))
            file.close()
            
        except IOError:
            file = open(self.full_path +"/settings.txt", 'w')
            file.write('#this file contains settings\n')
            file.write('last_backup=None\n')
            file.write('days_between_backups=3\n')            
            file.close()
            
        return last_backup_date
     
    #if time from the last backup is longer than n days set in settings.txt
    def time_to_backup(self):
        
        if self.last_backup == None: return True
        if self.last_backup + self.time_between_backups < datetime.now():   
            Logger.info('Settings: time to backup {}'.format(True))
            return True
        Logger.info('Settings: time to backup {}'.format(False))
        return False        
    
    #updates the last updated time
    def update_settings(self, update_time=None):
        
        from tempfile import mkstemp
        from shutil import move
        from os import remove, close
        
        #Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path,'w') as new_file:
            with open(self.full_path + "/settings.txt") as old_file:
                for line in old_file:
                    if update_time:
                        if(line.split('=')[0] =='last_backup'):                        
                            new_file.write("{}={}\n".format('last_backup', update_time))
                        else:
                            new_file.write(line)
                    else:
                        new_file.write(line)
        close(fh)
        
        #Remove original file
        remove(self.full_path +"/settings.txt" )
        #Move new file
        move(abs_path, self.full_path +"/settings.txt")
    
    
class ItemHandler():

    item_list = []
    
    def __init__(self, path):
        self.full_path = path
        self.item_list = self.update_item_list()
        
    def get_items(self):
        return self.item_list
    
    def update_path(self, new_path):
        self.full_path = new_path

    def add_item(self,name, price, filename, item_class):
        
        file = open(self.full_path + "/items.txt", "a")    
        normal_background, pressed_background = self.make_item_backgrounds(name, filename)
        
        file.write("{},{},{}\n".format(name.lower(), price,item_class))
        file.close()
        self.update_item_list()
        
        return Item(name.lower(),price, item_class, self.full_path)
        
        
    def update_item_list(self):
        items = []
        #make new file if one does not exist
        try:
            file = open(self.full_path + "/items.txt", "r")        
        
            file.readline() #reads the first description line
            
            for line in file:
                a = line.split(",")
                name = a[0]
                price = float(a[1])
                item_class = a[2][:-1]
                items.append(Item(name,price, item_class, self.full_path))
                items.sort(key=lambda x: x.name)
                
            file.close()
            
        except IOError:
			file = open(self.full_path +"/items.txt", 'w')
			file.write("name,price,Item class")
			file.close()
            
        return items
        
    def update_item_price(self,item,new_price):
        Logger.info('Item_handler: on update_item_price with item {} and new price {}'.format(item.name,new_price))
        
        from tempfile import mkstemp
        from shutil import move
        from os import remove, close
        
        #Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path,'w') as new_file:
            with open(self.full_path + "/items.txt") as old_file:
                for line in old_file:
                    if(line.split(',')[0] ==item.name):
                        new_file.write("{},{},{}\n".format(item.name.lower(), new_price,item.item_class))
                        Logger.info('ItemHandler: update price replace called')
                    else:
                        new_file.write(line)
        close(fh)
        
        #Remove original file
        remove(self.full_path +"/items.txt" )
        #Move new file
        move(abs_path, self.full_path +"/items.txt")
        self.update_item_list()
        
    def delete_item(self,item):
        Logger.info('Item_handler: about to delete {}'.format(item.name))
        
        from tempfile import mkstemp
        from shutil import move
        from os import remove, close
        
        #Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path,'w') as new_file:
            with open(self.full_path + "/items.txt") as old_file:
                for line in old_file:
                    if(line.split(',')[0] ==item.name):
                        pass
                    else:
                        new_file.write(line)
        close(fh)
        #Remove original file
        remove(self.full_path +"/items.txt" )
        #Move new file
        move(abs_path, self.full_path +"/items.txt")    
    
    def make_item_backgrounds(self, name,filename):
        
        
        item_name = name.lower()
        
        pic = Image.open(filename)    
        border = Image.open(self.full_path + "/kuvat/border1.png")    
        
        pic = pic.resize((300,300), Image.ANTIALIAS)
        border = border.resize((300,300), Image.ANTIALIAS)    
       
        pic2 = pic
        pic1_path = self.full_path + "/itempics/{}{}{}".format(item_name,"_normal_" , "pic.png")
        pic2_path = self.full_path + "/itempics/{}{}{}".format(item_name, "_pressed_" ,"pic.png")
       
        #creating normal background
        #pic.paste(border, (0,0), border)    
        pic.save(pic1_path ,"PNG")
        
        #creating the pressed background
        colour = Image.new("RGBA", (300,300), (50,50,225, 50))
        pic2.paste(colour, (0,0,300,300), colour)
        pic2.save(pic2_path,"PNG")
        
        return pic1_path, pic2_path
    
        
    
    
