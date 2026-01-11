from coincenter_stub import CoinCenterStub
import sys


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



def is_valid_command(command, user_id):
    command_map = {
    "manager": {
        "ADD_ASSET": (10, 5), #comando: (codigo, length)
        "GET_ALL_ASSETS": (20, 1),
        "REMOVE_ASSET": (30, 2),
        "EXIT": (40, 1)
    },
    "user": {
        "GET_ALL_ASSETS": (50, 1),
        "GET_ASSETS_BALANCE": (60, 1),
        "BUY": (70, 3),
        "SELL": (80, 3),
        "EXIT": (90, 1),
        "DEPOSIT": (100, 2),
        "WITHDRAW": (110, 2)
    }}
    if user_id == 0:
        valid_commands = command_map["manager"]
    else:
        valid_commands = command_map["user"]

    command_args = command.split(";")
    cmd = command_args[0]

    if cmd not in valid_commands or len(command_args) != valid_commands[cmd][1]:
        return False
    return True


def main():

    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)

    user_id = int(sys.argv[1])
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])

    stub = CoinCenterStub(user_id,server_ip,server_port)

    if user_id == 0:
      show_manager_menu()
    else:
      show_user_menu()

    

    try:
        while True:
            command = input("command > ")
            
            if command.upper() == "EXIT":
                stub.exit()
                break
            else:
                if is_valid_command(command, user_id):
                    response = stub.handle_command(command)
                    print(response)
                else:
                    print("invalid command")

    except Exception as e:
        print(f'Erro: {e}')
    
    
if __name__ == "__main__":
    main()