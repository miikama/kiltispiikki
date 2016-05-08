from PIL import Image
import os

# All the items are on their own separate lines

item_file_path = "items.txt"
customer_file_path = "customers.txt"
full_path = os.getcwd()
#full_path = "/sdcard/data

class Item():
    
    def __init__(self, name, price, item_class):
        self.name = name
        self.price = price
        self.item_class = item_class #string with value Candy, Soft drink or Food
        self.normal_background = "{}{}{}{}".format(full_path, "/itempics/", name, "_normal_pic.png")
        self.pressed_background = "{}{}{}{}".format(full_path, "/itempics/",name, "_pressed_pic.png")  


def add_item(name, price, filename, item_class):
    file = open(full_path + "/items.txt", "a")    
    normal_background, pressed_background = make_item_backgrounds(name, filename)
    
    file.write("{},{},{}\n".format(name, price,item_class))
    file.close()
    
    
def update_item_list():
    file = open(full_path + "/items.txt", "r")
    
    items = []
    file.readline() #reads the first description line
    
    for line in file:
        a = line.split(",")
        name = a[0]
        price = float(a[1])
        item_class = a[2][:-1]
        items.append(Item(name,price, item_class))
        
    return items
    
    

def make_item_backgrounds(name,filename):
    
    
    item_name = name.lower()
    
    pic = Image.open(filename)    
    border = Image.open(full_path + "/kuvat/border1.png")    
    
    pic = pic.resize((300,300), Image.ANTIALIAS)
    border = border.resize((300,300), Image.ANTIALIAS)    
   
    pic2 = pic
    pic1_path = full_path + "/itempics/{}{}{}".format(item_name,"_normal_" , "pic.png")
    pic2_path = full_path + "/itempics/{}{}{}".format(item_name, "_pressed_" ,"pic.png")
   
    #creating normal background
    pic.paste(border, (0,0), border)    
    pic.save(pic1_path ,"PNG")
    
    #creating the pressed background
    colour = Image.new("RGBA", (300,300), (50,50,225, 50))
    pic2.paste(colour, (0,0,300,300), colour)
    pic2.save(pic2_path,"PNG")
    
    return pic1_path, pic2_path

    


