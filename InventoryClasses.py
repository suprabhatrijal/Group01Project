from tabulate import tabulate
import uuid


headers = ["S.No", "ID", "Name", "Type", "Color", "Size", "Price", "Count"]


class Item:
    def __init__(
        self,
        name,
        type,
        color,
        size,
        price,
        count,
        id=None,
    ) -> None:
        if id is None:
            self.id = uuid.uuid4().int
        else:
            self.id = int(id)
        self.name = name
        self.type = type
        self.color = color
        self.size = size
        self.price = float(price)
        self.count = int(count)


class Inventory:
    def __init__(self, fileName) -> None:
        self.database = fileName
        self.stock = self.readFromFile()

    def checkStock(self, itemName):
        itemFound = False
        table = []
        for stockItem in self.stock:
            if itemName == stockItem.name:
                table.append(
                    [
                        stockItem.id,
                        stockItem.name,
                        stockItem.type,
                        stockItem.color,
                        stockItem.size,
                        stockItem.price,
                        stockItem.count,
                    ]
                )
                itemFound = True

        if not itemFound:
            self.printStock()
            print()
            print("The item is not in stock :(")
        else:
            string = tabulate(table, headers=headers)
            print(string)
            print()
            print("The item is in stock!")

    # print the current stock
    def printStock(self):
        table = []
        for i, item in enumerate(self.stock):
            table.append(
                [
                    str(i + 1),
                    str(item.id),
                    item.name,
                    item.type,
                    item.color,
                    item.size,
                    item.price,
                    item.count,
                ]
            )
        print(tabulate(table, headers=headers))

    def readFromFile(self):
        with open(self.database, "r") as file:
            items = []
            lines = file.readlines()
            for line in lines[1:]:
                itemList = line.split(",")
                item = Item(
                    itemList[1].strip(),
                    itemList[2].strip(),
                    itemList[3].strip(),
                    itemList[4].strip(),
                    float(itemList[5].strip()),
                    int(itemList[6].strip()),
                    id=int(itemList[0].strip()),
                )
                items.append(item)

        return items

    def writeToFile(self):
        with open(self.database, "w") as file:
            file.write("ID, Name, Type, Color, Size, Price, Count \n")
            for item in self.stock:
                itemString = f"{item.id}, {item.name}, {item.type}, {item.color}, {item.size}, {item.price}, {item.count}, \n"
                file.write(itemString)

    def addItem(self, item):
        for i, stockItem in enumerate(self.stock):
            if (
                stockItem.name == item.name
                and stockItem.color == item.color
                and stockItem.size == item.size
            ):
                stockItem.count += item.count
                self.stock[i] = stockItem
                self.writeToFile()
                return
        self.stock.append(item)
        self.writeToFile()

    def removeItem(self, item):
        for i, stockItem in enumerate(self.stock):
            if (
                stockItem.name == item.name
                and stockItem.color == item.color
                and stockItem.size == item.size
            ):
                stockItem.count -= item.count
                if stockItem.count <= 0:
                    self.stock.remove(stockItem)
                else:
                    self.stock[i] = stockItem
        self.writeToFile()

    def getItem(self, index):
        if index >= 0 and index < len(self.stock):
            return self.stock[index]
        return None

    def changePrice(self, item, price):
        for i, stockItem in enumerate(self.stock):
            if stockItem.id == item.id:
                stockItem.price = price
                self.stock[i] = stockItem
                self.writeToFile()
