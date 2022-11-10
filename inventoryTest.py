from InventoryClasses import Inventory, Item

inventory_database = "inventory_database.db"
sales_database = "sales_database.db"
user_database = "user_database.db"

inventory = Inventory(inventory_database)

puffer_jacket = Item("Puffer Jacket", "Jacket", "Yellow", "xl", 20, 5)
cotton_pants = Item("Cotton Pants", "Pants", "Green", "l", 20, 3)
inventory.addItem(cotton_pants)
inventory.addItem(puffer_jacket)
inventory.printStock()
