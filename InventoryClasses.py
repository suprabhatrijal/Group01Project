class Item:
    def __init__(self) -> None:
        self.name = None  # String
        self.id = None  # Automatically generate id upon object creation
        self.color = None  # String
        self.size = None  # string
        self.price = None  # decimal


class Inventory:
    def __init__(self) -> None:
        self.list = []  # list of type item

    def in_stock(self, item):
        if item in self.list:
            return True
        else:
            return False
