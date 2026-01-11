"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Número de aluno: 62211
"""

import sys
from net_client import *

### código do programa principal ###
def show_manager_menu():
     print( """
     \n=== MANAGER MENU ===\n
     >>> CHOOSE ONE out of the available COMMANDS <<< \n
     -------------------------------------------------------------------------\n
     -> TO ACCESS ALL ASSETS, use the following format:\n
        GET_ALL_ASSETS\n
     -------------------------------------------------------------------------\n
     -> TO ADD AN ASSET, use the following format:\n
        ADD_ASSET;[asset_name];[asset_symbol];[asset_price];[available_supply]\n
     -------------------------------------------------------------------------\n
     -> TO REMOVE AN ASSET, use the following format:\n
        REMOVE_ASSET;[asset_symbol]\n
     -------------------------------------------------------------------------\n
     """)
     

def show_user_menu():
     print( """
     \n=== USER MENU ===\n
     >>> CHOOSE ONE out of the available COMMANDS <<< \n
     --------------------------------------------------\n
     -> TO ACCESS ALL ASSETS, use the following format:\n
        GET_ALL_ASSETS\n
     --------------------------------------------------\n
     -> TO CHECK YOUR BALANCE, use the following format:\n
        GET_ASSETS_BALANCE\n
     ---------------------------------------------------\n
     -> TO BUY AN ASSET, use the following format:\n
        BUY;[asset_symbol];[quantity]\n
     ---------------------------------------------------\n
     -> TO SELL AN ASSET, use the following format:\n
        SELL;[asset_symbol];[quantity]\n
     ---------------------------------------------------\n
     -> TO DEPOSIT MONEY, use the following format:\n
        DEPOSIT;[amount]\n
     ---------------------------------------------------\n
     -> TO WITHDRAW MONEY, use the following format:\n
        WITHDRAW;[amount]\n
     ---------------------------------------------------\n  
     """)


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)

    ### código ###
    client_id = sys.argv[1]
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
    socket = NetClient(client_id, HOST, PORT)
    user_commands = {"GET_ALL_ASSETS", "GET_ASSETS_BALANCE", "BUY", "SELL", "DEPOSIT", "WITHDRAW"}
    manager_commands = {"GET_ALL_ASSETS", "ADD_ASSET", "REMOVE_ASSET"}
    valid_commands = {}

    if client_id == "0":
      show_manager_menu()
      valid_commands = manager_commands
    else:
      show_user_menu()
      valid_commands = user_commands
    
    socket.send(client_id)
    
    while True:
      command = input("command >")
      if command == 'EXIT':
         socket.close
         break
      else:
         command_args = command.split(";")
         print(command_args, len(command_args))
         msg_error = f"ERROR: O comando '{command_args[0]}' não é válido. Por favor, verifique se o comando está correto e tente novamente. Use a lista de comandos disponíveis para referência."
         if command_args[0] not in valid_commands:
            print(msg_error)
         else:
            if command_args[0] in {"GET_ALL_ASSETS", "GET_ASSETS_BALANCE"} and len(command_args) != 1:
               print(msg_error)
            
            elif command_args[0] in {"REMOVE_ASSET", "WITHDRAW", "DEPOSIT"} and len(command_args) != 2:
               print(msg_error)
               
            elif command_args[0] in {"BUY", "SELL"} and len(command_args) != 3:
               print(msg_error)
            
            elif command_args[0] == "ADD_ASSET" and len(command_args) != 5:
               print(msg_error)

            else:
               socket.send(f"{command};{client_id}")
               socket.recv()
               print(f"Recebi:\n{socket.recv_msg}")
               


if __name__ == "__main__":
    main()