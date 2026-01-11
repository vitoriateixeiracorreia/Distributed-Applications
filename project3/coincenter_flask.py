"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Número de aluno: 62211
"""

import sys
import signal
from flask import Flask, request, jsonify, make_response
from setup_db import connect_db
from coincenter_data import *
from display_functions import *

from kazoo.client import KazooClient

zh = KazooClient()
zh.start()
zh.ensure_path('/assets')

server = Flask(__name__)

def handle_shutdown(signum, frame):
    sys.exit(0)


@server.route('/asset', methods=["POST"])
@server.route('/asset/<string:asset_symbol>', methods=["GET"])
def asset(asset_symbol=None):
    conn, cursor = connect_db() 

    if request.method == "GET":
        asset_symbol = asset_symbol.strip().upper() if asset_symbol else None
        asset = get_asset(cursor, asset_symbol)
        conn.close()

        if asset:
            response = display_asset(asset[1], asset[0], asset[2], asset[3])
            return make_response(jsonify({"message": response}), 200)

        return make_response(jsonify({"error": "Asset with that symbol does not exist"}), 404)

    if request.method == "POST":
        data = request.get_json()
        asset_symbol = data.get('asset_symbol', '').strip().upper()
        asset = get_asset(cursor, asset_symbol)

        if not asset:
            add_asset(cursor, conn, data)
            conn.close()
            zh.create(f"/assets/{asset_symbol}", ephemeral=True)
            return make_response(jsonify({"message": f"The asset {asset_symbol} was successfully added!"}), 201)

        conn.close()
        return make_response(jsonify({"error": "Asset with that symbol already exists"}), 400)
    

@server.route('/assetset/<string:asset_symbols>', methods=["GET"])
def assetset(asset_symbols):
    conn, cursor = connect_db()
    symbols_list = [s.strip().upper() for s in asset_symbols.split(',')]
    assets = get_assetset(cursor, asset_symbols)
    found_symbols = [asset[0] for asset in assets] if assets else []
    not_found = [s for s in symbols_list if s not in found_symbols]

    response = {}
    if assets:
        for asset in assets:
            response[asset[1]] = display_asset(asset[1], asset[0], asset[2], asset[3])

    conn.close()
    if not_found:
        response["not found"] = list(set(not_found))
    if not response:
        return make_response(jsonify({"error": "No matching assets found"}), 404)
    return make_response(jsonify({"message": response}), 200)


@server.route('/login', methods=["POST"])
def login():
    conn, cursor = connect_db()
    data = request.get_json()
    client = get_client(cursor, data['client_id'])
    if not client:
        client_id = add_client(cursor, conn)
        return make_response(jsonify({"message": client_id}), 200)
    else:
        return make_response(jsonify({"message": data['client_id']}), 200)


@server.route('/user/<int:client_id>', methods=["GET"])
def user(client_id):
    conn, cursor = connect_db()

    user_assets, balance = get_balance(cursor, client_id)
        
    if user_assets is None or balance is None:
        conn.close()
        return make_response(jsonify({"error": "No data found for the given id"}), 404)

    response = display_user(balance, user_assets)
    conn.close()
    return make_response(jsonify({"message": response}), 200)


@server.route('/buy', methods=["POST"])
def buy():
    conn, cursor = connect_db()
    data = request.get_json()
    client_id = data['client_id']
    asset_symbol = data['asset_symbol']
    quantity = data['quantity']

    asset = get_asset(cursor, asset_symbol)
    if not asset:
        return make_response(jsonify({"error": "Asset not found"}), 404)
    price, available_quantity = asset[2], asset[3]

    quantity = float(quantity)
    if quantity > available_quantity:
        return make_response(jsonify({"error": "Not enough asset quantity available"}), 400)

    _, balance = get_balance(cursor, client_id)

    total_cost = price * quantity
    if balance < total_cost:
        return make_response(jsonify({"error": "Insufficient balance"}), 400)

    buy_asset(cursor, conn, client_id, asset_symbol, quantity, total_cost)
    return make_response(jsonify({"message": f"You successfully bought {quantity} of {asset_symbol} for {total_cost}"}), 200)

@server.route('/sell', methods=["POST"])
def sell():
    conn, cursor = connect_db()
    data = request.get_json()
    client_id = data['client_id']
    asset_symbol = data['asset_symbol']
    quantity = float(data['quantity'])

    asset = get_asset(cursor, asset_symbol)
    if not asset:
        return make_response(jsonify({"error": "Asset not found"}), 404)
    price = asset[2]

    # Verifica se o usuário possui a quantidade suficiente do asset
    user_assets, _ = get_balance(cursor, client_id)
    user_asset_quantity = 0
    for user_asset in user_assets:
        if user_asset[0] == asset_symbol:
            user_asset_quantity = user_asset[1]
            break

    if quantity > user_asset_quantity:
        return make_response(jsonify({"error": "You do not own enough of this asset to sell"}), 400)

    total_value = price * quantity

    # Realiza a venda (atualiza o saldo do usuário e a quantidade do asset)
    sell_asset(cursor, conn, client_id, asset_symbol, quantity, total_value)
    return make_response(jsonify({"message": f"You successfully sold {quantity} of {asset_symbol} for {total_value}"}), 200)


@server.route('/withdraw', methods=["POST"])
def withdraw():
    conn, cursor = connect_db()
    data = request.get_json()
    client_id = data['client_id']
    quantity = float(data['amount'])

    _, balance = get_balance(cursor, client_id)
    if quantity > balance:
        return make_response(jsonify({"error": "Insufficient balance"}), 400)

    new_balance = balance - float(quantity)
    decrease_balance(cursor, conn, new_balance, client_id)

    return make_response(jsonify({"message": f"Your balance was updated. New balance: {new_balance}"}), 200)

@server.route('/deposit', methods=["POST"])
def deposit():
    conn, cursor = connect_db()
    data = request.get_json()
    client_id = data['client_id']
    quantity = float(data['amount'])
    print(client_id)
    _, balance = get_balance(cursor, client_id)
    new_balance = balance + quantity
    increase_balance(cursor, conn, new_balance, client_id)
    conn.close()
    return make_response(jsonify({"message": f"Your balance was updated. New balance: {new_balance}"}), 200)


@server.route('/transactions/<string:timestamp>', methods=["GET"])
def transactions(timestamp):
    conn, cursor = connect_db()
    transactions = get_transactions(cursor, timestamp)
    if not transactions:
        conn.close()
        return make_response(jsonify({"error": "No transactions found"}), 404)
    conn.close()
    return make_response(jsonify({"message": display_transactions(transactions)}), 200)
    

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_flask.py server_ip server_port")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    signal.signal(signal.SIGINT, handle_shutdown)

    server.run(host=HOST, port=PORT, debug=True)

if __name__ == "__main__":
    main()
    zh.stop()
    zh.close()