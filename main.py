import copy
from classes.InventoryClasses import Inventory, Item
from classes.UserClasses import Users
from os import system, name


inventory_database = "./databases/inventory_database.db"
users_database = "./databases/user_database.db"
sales_database = "./databases/sales_database.db"


with open(sales_database) as saleFile:
    total_sale = float(saleFile.read())

inventory = Inventory(inventory_database)
users = Users(users_database)

menu_stack = []

authenticated = False


def clear():

    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def displayMenu(items, back=True, exit=True):
    valid = False
    selection = -1
    while not valid:

        # make sales or donation
        print()
        for i, item in enumerate(items):
            print(f"[{i+1}] {item}")

        add = 1
        if back and exit:
            print(f"[{len(items)+1}] Back")
            print(f"[{len(items)+2}] Exit")
            add = 3
        if (not back) and exit:
            print(f"[{len(items)+1}] Exit")
            add = 2

        print()
        selection = int(input("Make Selection: "))
        clear()
        print()
        if selection not in range(1, len(items) + add):
            print("Invalid selection! Choose Again!")
            print()
            continue
        valid = True
    return selection


def createNewUserMenu():
    global authenticated
    success = False
    valid_username = False
    valid_password = False
    while not (success and valid_username and valid_password):
        print("Account Creation Menu:")
        print()
        inputUsername = input("Enter a username: ")
        inputPassword = input("Enter a password: ")
        confirmInputPassword = input("Enter the password to confirm: ")
        clear()
        if len(inputUsername) < 4:
            print("Username must be 3 characters or longer!")
            valid_username = False
            continue
        else:
            valid_username = True

        if len(inputPassword) < 8:
            print("Passwords must 8 characters or longer!")
            valid_password = False
            continue
        else:
            valid_password = True

        if inputPassword != confirmInputPassword:
            print("Two passwords must match!")
            valid_password = False
            continue
        else:
            valid_password = valid_password and True
        success = users.createUser(inputUsername, inputPassword)
        if not success:
            print("User already exists")
    print("User Creation successful!")
    print()
    if not authenticated:
        authenticateUserMenu()
    else:
        authenticationManagementMenu()


def authenticationManagementMenu():
    if menu_stack[-1] != "auth":
        menu_stack.append("auth")
    items = ["Create New User", "Login with different Credentials"]
    print("Authentication Management")
    selection = displayMenu(items)
    if selection == 1:
        createNewUserMenu()
    elif selection == 2:
        menu_stack.pop()
        authenticateUserMenu()
    elif selection == len(items) + 1:
        handleBack()
    elif selection == len(items) + 2:
        exit()


def authenticateUserMenu():
    global authenticated
    authenticated = False
    print("Login Menu")
    while not authenticated:
        print()
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        clear()
        authenticated = users.authenticateUser(username, password)
        if not authenticated:
            print("Username or password is incorrect. Try again!")
            print()
    authenticated = True
    print("Sucessfully Logged In!")
    mainMenu()


def handleBack():
    global menu_stack
    menu_stack.pop()
    tos = menu_stack[-1]
    if tos == "main":
        clear()
        mainMenu()
    elif tos == "auth":
        clear()
        authenticateUserMenu()


def salesMenu():
    if menu_stack[-1] != "salesMain":
        menu_stack.append("salesMain")
    items = ["Sell", "Donate"]
    print("Sales Menu:")
    selection = displayMenu(items)
    if selection == 1:
        sellMenu()
    elif selection == 2:
        donateMenu()
    elif selection == len(items) + 1:
        handleBack()
    elif selection == len(items) + 2:
        exit()


def donateMenu():
    valid = False
    while not valid:
        print("Donate Menu: ")
        inventory.printStock()
        print()
        itemNumber = int(input("Select an item to donate by typing the S.No.: "))
        count = int(input("How many to donate? "))
        clear()
        item = inventory.getItem(itemNumber - 1)
        if item is not None and count <= item.count:
            new_item = copy.deepcopy(item)
            new_item.count = count
            inventory.removeItem(new_item)
            inventory.printStock()
            print()
            print(f"Item sucessfully donated!")
            input("Press Enter to go back: ")
            clear()
            print()
            valid = True
        elif item is None:
            print("Please entre a valid S.No: ")
        elif count > item.count:
            print("Can't donate more items than available in stock")
    salesMenu()


def sellMenu():
    global total_sale
    valid = False
    while not valid:
        print("Sell Menu: ")
        print()
        inventory.printStock()
        print()
        itemNumber = int(input("Select an item to sell by typing the S.No.: "))
        count = int(input("How many to sell? "))
        clear()
        item = inventory.getItem(itemNumber - 1)
        if item is not None and count <= item.count:
            new_item = copy.deepcopy(item)
            new_item.count = count
            total_sale = total_sale + item.price * count
            inventory.removeItem(new_item)
            inventory.printStock()
            print()
            print(f"Item sucessfully sold! Total Sale: ${total_sale}")
            input("Press Enter to go back: ")
            clear()
            print()
            f = open(sales_database, "w")
            f.write(str(total_sale))
            f.close()
            valid = True
        elif item is None:
            print("Please entre a valid S.No: ")
        elif count > item.count:
            print("Can't sell more items than available in stock")
    salesMenu()


def showInventoryMenu():
    print("Inventory:\n")
    inventory.printStock()
    print()
    input("Press Enter to go back: ")
    inventoryMenu()


def checkInventoryMenu():
    itemName = input("Enter the name of item to check the stock of: ")
    clear()
    inventory.checkStock(itemName)
    print()
    input("Press Enter to go back")
    inventoryMenu()


def addItemMenu():
    print("Add Menu: ")
    name = input("Enter the name of item to add: ")

    print("Enter the type: ")
    types = ["Top", "Bottom", "Outerwear", "Accesories"]
    type = types[displayMenu(types, back=False, exit=False) - 1]

    color = input("Enter the color of item to add: ")

    sizes = ["xs", "sm", "md", "l", "xl", "xxl"]
    print("Enter the size: ")
    size = sizes[displayMenu(sizes, back=False, exit=False) - 1]

    price = float(input("Enter the price of item to add: "))
    count = int(input("Enter the number of item to add: "))

    item = Item(name, type, color, size, price, count)

    inventory.addItem(item)
    inventory.printStock()
    print()
    print(f"Item sucessfully added!")
    input("Press Enter to go back: ")
    clear()
    print()
    inventoryMenu()


def removeItemMenu():
    valid = False
    while not valid:
        print("Remove Item: ")
        inventory.printStock()
        print()
        itemNumber = int(input("Select an item to remove by typing the S.No.: "))
        count = int(input("How many to remove? "))
        clear()
        item = inventory.getItem(itemNumber - 1)
        if item is not None and count <= item.count:
            new_item = copy.deepcopy(item)
            new_item.count = count
            inventory.removeItem(new_item)
            inventory.printStock()
            print()
            print(f"Item sucessfully removed!")
            input("Press Enter to go back: ")
            clear()
            print()
            valid = True
        elif item is None:
            print("Please enter a valid S.No: ")
        elif count > item.count:
            print("Can't remove more items than available in stock")
    inventoryMenu()


def changePriceMenu():
    valid = False
    while not valid:
        print("Change Price of an Item: ")
        inventory.printStock()
        print()
        itemNumber = int(
            input("Select an item to change price of by typing the S.No.: ")
        )
        price = int(input("What is the new price? "))
        clear()
        item = inventory.getItem(itemNumber - 1)
        if item is not None:
            inventory.changePrice(item, price)
            inventory.printStock()
            print()
            print("Price successfully changed")
            input("Press Enter to go back: ")
            clear()
            print()
            print()
            valid = True
        elif item is None:
            print("Please enter a valid S.No: ")
    inventoryMenu()


def listByCategory():
    originalList = copy.deepcopy(inventory.stock)
    categories = ["Type", "Color", "Size", "Price"]
    print("Choose a category")
    category = categories[displayMenu(categories, back=False, exit=False) - 1]
    print(category)

    # sizes = ["xs", "sm", "md", "l", "xl", "xxl"]
    sizeDict = {"xs": 1, "sm": 2, "md": 3, "l": 4, "xl": 5, "xxl": 6}
    if category == "Type":
        inventory.stock.sort(key=lambda x: x.type)
        inventory.printStock()
        print()
        input("Press enter to go back")
        clear()
        inventory.stock = originalList
        inventoryMenu()
    elif category == "Color":
        inventory.stock.sort(key=lambda x: x.color)
        inventory.printStock()
        print()
        input("Press enter to go back")
        clear()
        inventory.stock = originalList
        inventoryMenu()
    elif category == "Size":
        inventory.stock.sort(key=lambda x: sizeDict[x.size])
        inventory.printStock()
        print()
        input("Press enter to go back")
        clear()
        inventory.stock = originalList
        inventoryMenu()

    elif category == "Price":
        inventory.stock.sort(key=lambda x: x.price)
        inventory.printStock()
        print()
        input("Press enter to go back")
        clear()
        inventory.stock = originalList
        inventoryMenu()


def inventoryMenu():
    clear()
    if menu_stack[-1] != "inventory":
        menu_stack.append("inventory")
    items = [
        "Show Inventory",
        "List Items by category",
        "Check if item is in stock",
        "Add item to Inventory",
        "Remove item from inventory",
        "Change price of an Item",
    ]
    print("Inventory Menu: ")
    selection = displayMenu(items)
    if selection == 1:
        showInventoryMenu()
    elif selection == 2:
        listByCategory()
    elif selection == 3:
        checkInventoryMenu()
    elif selection == 4:
        addItemMenu()
    elif selection == 5:
        removeItemMenu()
    elif selection == 6:
        changePriceMenu()
    elif selection == len(items) + 1:
        handleBack()
    elif selection == len(items) + 2:
        exit()


def mainMenu():
    if len(menu_stack) == 0:
        menu_stack.append("main")
    items = [
        "Make sales or donations",
        "Go to inventory management",
        "Manage Authentication",
    ]
    print("Main Menu:")
    selection = displayMenu(items, back=False)
    if selection == 1:
        salesMenu()
    elif selection == 2:
        inventoryMenu()
    elif selection == 3:
        authenticationManagementMenu()
    elif selection == len(items) + 1:
        exit()


#  if no users exist create user
if len(users.users) == 0:
    createNewUserMenu()

# if user\s exists authenticate
authenticateUserMenu()
