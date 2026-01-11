def show_manager_menu():
   print("""
   \n=== MANAGER MENU ===\n
   >>> CHOOSE ONE of the available COMMANDS <<<\n
   -------------------------------------------------------------------------\n
   -> TO ADD A NEW ASSET, use the following format:\n
         
      >>ADD_ASSET;[asset_name];[asset_symbol];[asset_price];[available_quantity]\n  
   --------------------------------------------------------------------------------------------------\n
   -> TO GET AN ASSET BASED ON THE ASSET'S SYMBOL, use the following format:\n
         
      >>ASSET;[asset_symbol]\n  
   --------------------------------------------------------------------------------------------------\n
   -> TO ACCESS A SET OF ASSETS BASED ON THEIR SYMBOLS, use the following format:\n
      
      >>ASSETSET;[asset_symbol1],[asset_symbol2],[...]\n
   -------------------------------------------------------------------------\n
   -> TO GET A USER'S BALANCE AND ASSETS BASED ON THE USER'S ID, use the following format:\n
         
      >>USER;[user_id]\n
   -------------------------------------------------------------------------\n
   -> TO GET THE SET OF ALL TRANSACTIONS WITHIN A SPECIFIED TIME RANGE, use the following format:\n
         
      >>TRANSACTIONS;[start_time]**;[end_time]**\n     

      ** YYYY-MM-DD HH:MM:SS\n 
   -------------------------------------------------------------------------\n
   """)
     

def show_user_menu():
   print( """
     \n=== USER MENU ===\n
     >>> CHOOSE ONE out of the available COMMANDS <<< \n
      -------------------------------------------------------------------------\n
     -> TO GET AN ASSET BASED ON THE ASSET'S SYMBOL, use the following format:\n
         
        >>ASSET;[asset_symbol]\n
     --------------------------------------------------------------------------------------------------\n
     -> TO ACCESS A SET OF ASSETS BASED ON THEIR SYMBOLS, use the following format:\n
      
        >>ASSETSET;[asset_symbol1],[asset_symbol2],[...]\n
         
     ---------------------------------------------------\n
     -> TO BUY AN ASSET, use the following format:\n
           
        >>BUY;[asset_symbol];[quantity]\n
     -----------------------------------------------------\n
     -> TO ACCESS YOUR BALANCE AND ASSETS, use the following format:\n
        
         >>HOLDINGS\n
     ---------------------------------------------------\n
     -> TO SELL AN ASSET, use the following format:\n
           
        >>SELL;[asset_symbol];[quantity]\n
     ---------------------------------------------------\n
     -> TO DEPOSIT MONEY, use the following format:\n
        
         >>DEPOSIT;[amount]\n
     ---------------------------------------------------\n
     -> TO WITHDRAW MONEY, use the following format:\n
        
         >>WITHDRAW;[amount]\n
     ---------------------------------------------------\n  
   """)

def show_login_menu():
   print("""
   =============================================
   |               WELCOME TO                  |
   |           COINCENTER CLIENT               |
   =============================================
   |                                           |
   |     TO LOGIN - Type LOGIN;client_id       |
   |                                           |
   |                                           |
   =============================================
   """)

def display_asset(symbol, name, price, available_supply):
    return f"{name} ({symbol}).........{price}$ | {available_supply}"

def display_user(balance, assets):
   result = {}
   result["USER BALANCE"] = f"{balance}$"
   result["ASSETS"] = []
   if assets and len(assets) > 0:
      for asset in assets:
         result["ASSETS"].append({
            "symbol": asset[0],
            "quantity": asset[1]
         })
   return result

def display_transactions(transactions):
   result = []
   for tx in transactions:
      result.append({
         "id": tx[0],
         "client_id": tx[1],
         "asset": tx[2],
         "type": tx[3],
         "quantity": tx[4],
         "price": tx[5],
         "timestamp": tx[6]
      })
   return result
