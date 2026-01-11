"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Número de aluno: 62211
"""

import sys
import signal
from display_functions import *
from requests_processor import process_request
from datetime import datetime
from kazoo.client import KazooClient
zh = KazooClient()
zh.start()
zh.ensure_path('/assets')

def handle_shutdown(signum, frame):
    print(f"\nA encerrar..\n")
    sys.exit(0)


def is_command_valid(client_id, command):
   command_map = {
      "manager": {
         "ADD_ASSET": 5, #length args comand
         "ASSET": 2,
         "ASSETSET": 2,
         "USER": 2,
         "TRANSACTIONS": 3
      },
      "user": {
         "ASSET": 2,
         "ASSETSET": 2,
         "HOLDINGS": 1,
         "BUY": 3,
         "SELL": 3,
         "DEPOSIT": 2,
         "WITHDRAW": 2
      }
   }

   if client_id == 0:
      valid_commands = command_map["manager"]
   else:
      
         
      valid_commands = command_map["user"]

   command_args = command.split(";")
   cmd = command_args[0]

   if cmd not in valid_commands:
      print(f"ERROR: The command '{cmd}' is not valid. Please check and try again.")
      return False

   if len(command_args) != valid_commands[cmd]:
      print(f"ERROR: The command '{cmd}' expects {valid_commands[cmd]} arguments but received {len(command_args)}.")
      return False

   try:
      if cmd == "ADD_ASSET":
         float(command_args[3])
         int(command_args[4])
      elif cmd == "USER":
         user_id = int(command_args[1])
         if user_id == 0:
            print("ERROR: User ID cannot be zero. Please provide a non-zero user ID.")
            return False
      elif cmd == "TRANSACTIONS":
         datetime.strptime(command_args[1], "%Y-%m-%d %H:%M:%S")
         datetime.strptime(command_args[2], "%Y-%m-%d %H:%M:%S")
      elif cmd in {"BUY", "SELL"}:
         float(command_args[2])
      elif cmd in {"DEPOSIT", "WITHDRAW"}:
         value = float(command_args[1])
   except (ValueError, TypeError):
      print(f"ERROR: Invalid argument types for the command '{cmd}'. Please check and try again.")
      return False

   return True

not_show = set()
def main():
   if len(sys.argv) != 3:
      print("Usage: python3 coincenter_client.py server_ip server_port")
      sys.exit(1)

   HOST = sys.argv[1]
   PORT = int(sys.argv[2])
   print(f'Connected to the server {HOST}:{PORT}\n')
   signal.signal(signal.SIGINT, handle_shutdown)
   BASE_URL = f'http://{HOST}:{PORT}'
   
   show_login_menu()
   while True:
      login_command = input(">> ")
      parts = login_command.strip().split(';')
      if len(parts) < 2 or parts[0] != "LOGIN":
         print("ERROR: Login command must be in the format 'LOGIN;<client_id>'. Please try again.")
         continue
      client_id_str = parts[1]
      try:
         client_id = int(client_id_str)
         if client_id < 0:
            print("ERROR: Client ID must be a non-negative integer (0 or greater). Please try again.")
            continue
         # Only process login after valid client_id
         client_id = int(process_request(client_id, BASE_URL, login_command))
         print(f"BEM-VINDO {client_id}")
         # Show the appropriate menu after successful login
         if client_id == 0:
            show_manager_menu()
         else:
            @zh.ChildrenWatch("/assets")
            def watch_children(children):
               global not_show
               show = set(children) - not_show
               if show:
                  print(f"\nNew assets available: {', '.join(show)}")
                  not_show.update(show)
                  print("command ↓")
            show_user_menu()
         break
      except ValueError:
         print("ERROR: Client ID must be an integer. Please try again.")
      except Exception as e:
         print("ERROR: Failed to Connect to server.")
         sys.exit(0)
   try:
      while True:
         command = input("command >> ")
         if is_command_valid(client_id, command):
            process_request(client_id, BASE_URL, command)
   except Exception as e:
      print(f'Erro: {e}')
   zh.stop()
   zh.close()
               


if __name__ == "__main__":
    main()
