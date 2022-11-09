# importing libraries
import json
import hashlib


# Function for Creating users
def CreateUser():
    print("*****************************")
    print("*******User Creation*********")
    print("*****************************\n")
    CLogin = input("Please enter a login: ").strip()
    password = input("Enter password: ")
    confpass = input("Confirm password: ")
    if confpass == password:
        encoder1 = confpass.encode()
        hashedU = hashlib.md5(encoder1).hexdigest()
        with open("logins&hashedpasswords.txt", "a") as file:
            file.write(CLogin + "\n")
            file.write(hashedU)
        file.close()
        print("Thank you, You have sucessfully registered!")
        UserLogin()
    else:
        print("This password is not the same please try again! \n")
        CreateUser()


# Function for Logging in Users
def UserLogin():
    print("*****************************")
    print("*******User Login************")
    print("*****************************\n")
    CLogin = input("Please enter your login: ").strip()
    password = input("Please enter your password: ")
    encoder2 = password.encode()
    hashedP = hashlib.md5(encoder2).hexdigest()
    with open("logins&hashedpasswords.txt", "r") as file:
        stored_CLogin, stored_password = file.read().split("\n")
    file.close()
    if CLogin == stored_CLogin and hashedP == stored_password:
        print("You have successfully logged in! \n")
    else:
        ask1 = int(
            input(
                "Login failed, Would you like to try again, register, or quit? Press 0 to try again, 1 to register, or 7 to exit. \n"
            )
        )
        if ask1 == 0:
            UserLogin()
        elif ask1 == 1:
            CreateUser()
        else:
            quit()


# Funciton for asking the user if they are registered or not#
def AskUser():
    ask = input(" Are you a registered user? \n")
    if ask == "Yes" or ask == "yes" or ask == "y" or ask == "Y":
        UserLogin()
    else:
        CreateUser()


# First function call#
AskUser()

# Creating variable for a Flag Controlled Loop#
Inv_Menu = True

# Creating an inventory using a dictionary#
inv = {
    "CPU": {"Intel": 12, "AMD": 14, "ARM": 19, "QUALCOMM": 11},
    "GPU": {"NVIDIA": 30, "AMD": 50, "Intel": 190},
    "PSU": {"EVGA": 168, "Corsair": 89, "CoolerMaster": 31, "be quiet!": 91},
    "Motherboard": {"Asrock": 70, "ASUS": 80, "MSI": 90, "Gigabyte": 110},
}

# Function for the Menu#
def menuI():
    while Inv_Menu:
        print("*****************************")
        print("Bredy & Co. Inventory System")
        print("*****************************\n")
        print(" 1. Add")
        print(" 2. Remove")
        print(" 3. Update Inv")
        print(" 4. Search Inv")
        print(" 5. Print Report")
        print(" 6. Export Inv")
        print(" 7. Quit System \n")
        print(
            "Note: Our current sections for our inventory are CPU, GPU, PSU, and MOTHERBOARD \n"
        )
        OPTION = int(input("Choose Option: "))
        if OPTION not in range(1, 8):
            print("Option not valid, please try again")
        else:
            break
    return menuOptions(OPTION)


# Function for taking in user input to choose the different inventory options#
def menuOptions(OPTION):
    if OPTION == 1:
        addInv()
    elif OPTION == 2:
        removeInv()
    elif OPTION == 3:
        updateInv()
    elif OPTION == 4:
        searchInv()
    elif OPTION == 5:
        printInv()
    elif OPTION == 6:
        exportInv()
    elif OPTION == 7:
        exit()


# Add to Inventory Function#
def addInv():
    print("Adding Inventory")
    print("**************** \n")
    Cat = input("What Category would you like to add in CPU/GPU/PSU/MOTHERBOARD: ")
    item = input("What is the item you want to add?: ")
    quantity = int(input("What is the quantity of this item?: "))
    if Cat in inv:
        inv[Cat][item] = quantity
        print(item + ": " + str(inv[Cat][item]))
    else:
        print("You may not add to this Category/Item at this time")
    OPTION = int(input("Enter 0 to continue or 7 to exit: "))
    if OPTION == 0:
        menuI()
    else:
        exit()


# Remove to Inventory Function#
def removeInv():
    print("Removing Inventory")
    print("****************** \n")
    Cat = input("What Category would you like to remove in CPU/GPU/PSU/MOTHERBOARD")
    item = input("What is the item you want to remove?: ")
    quantity = int(input("How many of these do you want to remove : "))
    if Cat in inv:
        inv[Cat][item] -= quantity
        print(item + ": " + str(inv[Cat][item]))
    else:
        print("You may not removeto this Category/Item at this time")
    OPTION = int(input("Operation Sucessful! Enter 0 to continue or 7 to exit: "))
    if OPTION == 0:
        menuI()
    else:
        exit()


# Update to Inventory Function#
def updateInv():
    print("Updating Inventory")
    print("****************** \n")
    Cat = input("Enter the category of item you'd like to update: ")
    item = input("What is the item that you want to update: ?")
    quantity = int(input("What is the updated value?: "))
    if Cat in inv:
        inv[Cat][item] = quantity
        print(item + ": " + str(inv[Cat][item]))
    else:
        print("That item is not in our inventory\n")
    OPTION = int(input("Enter 0 to continue or 7 to exit: \n"))
    if OPTION == 0:
        menuI()
    else:
        exit()


# Search Inventory Function#
def searchInv():
    print("Searching Inventory")
    print("******************* \n")
    Cat = input("Enter the name of the Category: ")
    item = input("Enter the type of the item: ")
    if Cat in inv:
        if item in inv[Cat]:
            print(
                "This item is in our inventory and there are "
                + str(inv[Cat][item])
                + "\n"
            )
        elif item not in inv[Cat]:
            print("That item is not in the inventory \n")
    else:
        print("This Category is not available, please pick another category \n")
        searchInv()
    OPTION = int(input("Enter 0 to continue or 7 to exit: "))
    if OPTION == 0:
        menuI()
    else:
        exit()


# Print Inventory Function#
def printInv():
    print("Current Inventory")
    print("*****************\n")
    for category, items in inv.items():
        print(category, items)
    OPTION = int(input("Operation Sucessful! Enter 0 to continue or 7 to exit: "))
    if OPTION == 0:
        menuI()
    else:
        exit()


# Export Inventory to txt file Function#
def exportInv():
    print("Check the root folder for your export")
    with open("inventory.txt", "w") as a:
        for key, value in inv.items():
            a.write("%s:%s\n" % (key, value))
    OPTION = int(input("Operation Sucessful! Enter 0 to continue or 7 to exit: "))
    if OPTION == 0:
        menuI()
    else:
        exit()


# Function Calling Menu
menuI()
