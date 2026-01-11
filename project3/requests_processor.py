"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Número de aluno: 62211
"""
import requests
import json

def add_asset(base_url, cmd_args, headers):
    url = f'{base_url}/asset'
    json_data = {'asset_symbol': cmd_args[1], 'asset_name': cmd_args[0], 'price': cmd_args[2], 'available_quantity': cmd_args[3]}
    return requests.post(url, json=json_data, headers=headers)

def get_asset(base_url, cmd_args, headers):
    url = f'{base_url}/asset/{cmd_args[0]}'
    return requests.get(url, headers=headers)

def get_assetset(base_url, command, headers):
    cmd_args = command[9:]
    url = f'{base_url}/assetset/{cmd_args}'
    return requests.get(url, headers=headers)

def get_transactions(base_url, command, headers):
    cmd_args = command[13:]
    url = f'{base_url}/transactions/{cmd_args}'
    return requests.get(url, headers=headers)

def buy_asset(base_url, id, cmd_args, headers):
    url = f'{base_url}/buy'
    json_data = {'client_id': id, 'asset_symbol': cmd_args[0], 'quantity': cmd_args[1]}
    return requests.post(url, json=json_data, headers=headers)

def get_balance(base_url, id, headers):
    url = f'{base_url}/user/{id}'
    return requests.get(url, headers=headers)

def sell_asset(base_url, id, cmd_args, headers):
    url = f'{base_url}/sell'
    json_data = {'client_id': id, 'asset_symbol': cmd_args[0], 'quantity': cmd_args[1]}
    return requests.post(url, json=json_data, headers=headers)

def deposit(base_url, id, cmd_args, headers):
    url = f'{base_url}/deposit'
    json_data = {'client_id': id, 'amount': cmd_args[0]}
    return requests.post(url, json=json_data, headers=headers)

def withdraw(base_url, id, cmd_args, headers):
    url = f'{base_url}/withdraw'
    json_data = {'client_id': id, 'amount': cmd_args[0]}
    return requests.post(url, json=json_data, headers=headers)

def login(base_url, id, headers):
    url = f'{base_url}/login'
    json_data = {'client_id': id}
    r = requests.post(url, json=json_data, headers=headers)
    data = r.json()
    client_id = data['message']
    return client_id

def process_request(id, base_url, command):
    cmd_args = command.split(";")[1:]
    cmd = command.split(";")[0]
    headers = {'Content-Type': 'application/vnd.collection+json'}
    r = None

    if cmd == 'LOGIN':
        return login(base_url, id, headers)
    elif cmd == 'ADD_ASSET':
        r = add_asset(base_url, cmd_args, headers)
    elif cmd == 'ASSET':
        r = get_asset(base_url, cmd_args, headers)
    elif cmd == 'ASSETSET':
        r = get_assetset(base_url, command, headers)
    elif cmd == 'USER':
        r = get_balance(base_url, cmd_args[0], headers)
    elif cmd == 'TRANSACTIONS':
        r = get_transactions(base_url, command, headers)
    elif cmd == 'BUY':
        r = buy_asset(base_url, id, cmd_args, headers)
    elif cmd == 'HOLDINGS':
        r = get_balance(base_url, id, headers)
    elif cmd == 'SELL':
        r = sell_asset(base_url, id, cmd_args, headers)
    elif cmd == 'DEPOSIT':
        r = deposit(base_url, id, cmd_args, headers)
    elif cmd == 'WITHDRAW':
        r = withdraw(base_url, id, cmd_args, headers)


    print("Status:", r.status_code)
    if r.status_code == 404 or r.status_code == 400:
        data = r.json()
        print(json.dumps(data['error'], indent=2))
    else:
        data = r.json()
        print(json.dumps(data['message'], indent=2))
 