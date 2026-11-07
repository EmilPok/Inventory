def _Player_Input():
    return input("1 - Show inventory | 2 - Shop | 3 - Use item | 4 - Check item | 5 - Sell item | 6 - Quit \n")

def _Check_Action(choice: str, inventory: dict):
    print("\n" + "-" * 50 + "\n")
    match choice:
        case "1":
            _Show_Inventory(inventory)
        case "2":
            _Shop(inventory)
        case "3":
            _Use_Item(inventory)
        case "4":
            _Check_Item(inventory)
        case "5":
            _Sell_Item(inventory)
        case "6":
            return False
        case _:
            print("Choose one of following choices")
    return True

def _Check_Inventory_Space(inventory: dict):
    if len(inventory) == 1:
        print("You dont have any items.\n")
        return False
    return True

def _Show_Inventory(inventory: dict, item: str = ""):    
    if item:
        print(f"{item} - {inventory[item]["Amount"]}")
    else:
        for item in inventory:
            print(f"{item} - {inventory[item]["Amount"]}")

def _Check_Gold(choice: str):
    if choice != "Gold":
        return True
    print("\n" + "-" * 50 + "\n")
    print("Invalid Item\n")
    return False

def _Count_Weight(inventory: dict):
    weight = 0
    for item in inventory:
        if item == "Gold":
            continue
        weight += (inventory[item]["Weight"] * inventory[item]["Amount"])
    return weight

def _Check_Bought_Item(purchased_item: str, inventory: dict, shop_items: dict) -> None:
    print("\n" + "-" * 50 + "\n")
    
    if purchased_item == "Exit":
        print("You exited the shop.")
        return True

    if purchased_item not in shop_items:
        print("Choose an available item.\n")
        return False

    if shop_items[purchased_item]["Cost"] >= inventory["Gold"]["Amount"]:
        print("You dont have enough gold.\n")
        return False
    
    if shop_items[purchased_item]["Weight"] + _Count_Weight(inventory) >= 100:
        print("You cant buy this item, you are too heavy.\n")
        return False

    inventory["Gold"]["Amount"] -= shop_items[purchased_item]["Cost"]

    if purchased_item in inventory:
        inventory[purchased_item]["Amount"] += 1
    else:
        inventory[purchased_item] = {"Amount": 1, "Weight": shop_items[purchased_item]["Weight"], "Cost": shop_items[purchased_item]["Cost"]}

    print(f"You bought {purchased_item}.")
    return True

def _Shop(inventory: dict):
    shop_items: dict = {
        "Sword": {"Weight": 15, "Cost": 50},
        "Dagger": {"Weight": 8, "Cost": 50},
        "Potion": {"Weight": 3, "Cost": 100},
        "Chestplate": {"Weight": 25, "Cost": 200},
        "Helmet": {"Weight": 15, "Cost": 200},
        "Crown": {"Weight": 5, "Cost": 500}
    }
    while True:
        print("Shop items:")
        for shop_item in shop_items:
            print(f"{shop_item} - {shop_items[shop_item]["Cost"]} gold - {shop_items[shop_item]["Weight"]}kg")
        print(f"\nYour stats - {inventory["Gold"]["Amount"]} gold")
        print("What item would you like to buy? (exit to leave the shop)")
        purchased_item = input().capitalize()
        
        if _Check_Bought_Item(purchased_item, inventory, shop_items):
            break
        
        

def _Delete_Item_From_Inventory(inventory: dict, new_item: str):
    if not _Check_Gold(new_item):
        return 0
    try:
        cost_of_item = inventory[new_item]["Cost"]
        inventory[new_item]["Amount"] -= 1
        if inventory[new_item]["Amount"] == 0:
            inventory.pop(new_item)
    except KeyError:
        print("\n" + "-" * 50 + "\n")
        print("There is none of that item in your inventory.\n")
    else:
        return cost_of_item
    return 0

def _Use_Item(inventory: dict):
    if not _Check_Inventory_Space(inventory):
        return
    while True:
        print("What item would you like to use?")
        _Show_Inventory(inventory)
        new_item = input().capitalize()
        if _Delete_Item_From_Inventory(inventory, new_item):
            print("\n" + "-" * 50 + "\n")
            print(f"You used {new_item}")
            break
     
def _Check_Item(inventory: dict):
    if not _Check_Inventory_Space(inventory):
        return
    while True:
        print("What item would you like to check.")
        _Show_Inventory(inventory)
        item_name = input().capitalize()
        if item_name == "Gold":
            print("\n" + "-" * 50 + "\n")
            print(f"You have {inventory["Gold"]["Amount"]} gold.")
            break
        try:
            print("\n" + "-" * 50 + "\n")
            print(f"You have {inventory[item_name]["Amount"]} {item_name}.")
            print(f"{item_name} weighs {inventory[item_name]["Weight"]}kg ", end="")
            print(f"and costs {inventory[item_name]["Cost"]} gold.")
        except KeyError:
            print("There is none of that item in your inventory.\n")
        else:
            break

def _Sell_Item(inventory: dict):
    if not _Check_Inventory_Space(inventory):
        return
    item_to_sell : str
    while True:
        print("What item would you like to sell?")
        _Show_Inventory(inventory)
        item_to_sell = input().capitalize()
        sell_value = _Delete_Item_From_Inventory(inventory, item_to_sell)
        if sell_value:
            inventory["Gold"]["Amount"] += sell_value
            
            print("\n" + "-" * 50 + "\n")
            
            print(f"You sold a {item_to_sell} for {sell_value} gold")
            
            break

def _Main_Game():
    inventory: dict = {"Gold": {"Amount": 999},
                       "Sword": {"Amount": 1, "Weight": 15, "Cost": 50},
                       "Potion": {"Amount": 1, "Weight": 3, "Cost": 100},
                       "Chestplate": {"Amount": 1, "Weight": 25, "Cost": 200}}
    
    while True:
        print()
        choice: str = _Player_Input()
        if not _Check_Action(choice, inventory):
            break
    print("Thank you for playing!")

_Main_Game()
