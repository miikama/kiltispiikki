
#items.py contains the classes and definitions of different items that are sold


for_sale = []

class Item():
    
    def __init__(self, name, price,icon):
        self.name = name
        self.price = price
        self.loadIcon(icon)
        for_sale.append(self)    

    def remove(self):
        if self in for_sale: for_sale.remove(self)

    def load_icon(self):
        pass
