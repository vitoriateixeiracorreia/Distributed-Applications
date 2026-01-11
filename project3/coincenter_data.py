from datetime import datetime

"""
Aplicações Distribuídas - Projeto 3 - coincenter_data.py
Número de aluno: 62211
"""

def add_asset(cursor, conn, data):
    cursor.execute("INSERT INTO Assets (asset_symbol, asset_name, price, available_quantity) VALUES (?,?,?,?)", (data['asset_symbol'].upper(),data['asset_name'].upper(),data['price'],data['available_quantity']))
    conn.commit()
    conn.close()

def get_asset(cursor, asset_symbol):
    cursor.execute("SELECT * FROM Assets WHERE asset_symbol = ?", (asset_symbol.upper(),))
    asset = cursor.fetchone()
    return asset

def get_assetset(cursor, asset_symbols):
    asset_list = asset_symbols.split(',')
    placeholders = ', '.join(['?'] * len(asset_list))
    cursor.execute(f"SELECT * FROM Assets WHERE asset_symbol IN ({placeholders})", asset_list)
    assets = cursor.fetchall()
    return assets

def add_client(cursor, conn):
    cursor.execute("INSERT INTO Clients (is_manager, balance) VALUES (0, 0)") #balance começa a 100?
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_client(cursor, client_id):
    cursor.execute("SELECT * FROM Clients WHERE client_id = ?", (client_id,))
    client = cursor.fetchone()
    return client
   
def get_balance(cursor, client_id):
    cursor.execute("""
        SELECT asset_symbol, quantity FROM ClientAssets
        WHERE client_id = ?
    """, (client_id,))
    user_assets = cursor.fetchall()

    cursor.execute("SELECT balance FROM Clients WHERE client_id = ?", (client_id,))
    balance = cursor.fetchone()
    if balance is None:
        return None, 0

    return user_assets, balance[0]

def decrease_balance(cursor, conn, new_balance, client_id):
    cursor.execute("UPDATE Clients SET balance = ? WHERE client_id = ?", (new_balance, client_id))
    conn.commit()
    conn.close()

def increase_balance(cursor, conn, new_balance, client_id):
    cursor.execute("UPDATE Clients SET balance = ? WHERE client_id = ?", (new_balance, client_id))
    conn.commit()
    conn.close()

def buy_asset(cursor, conn, client_id, asset_symbol, quantity, total_cost):
    cursor.execute("UPDATE Clients SET balance = balance - ? WHERE client_id = ?", (total_cost, client_id))
    # Atualiza quantidade disponível do ativo
    cursor.execute("UPDATE Assets SET available_quantity = available_quantity - ? WHERE asset_symbol = ?", (quantity, asset_symbol))
    # Verifica se o cliente já possui o ativo
    cursor.execute("SELECT quantity FROM ClientAssets WHERE client_id = ? AND asset_symbol = ?", (client_id, asset_symbol))
    result = cursor.fetchone()
    if result:
        # Atualiza a quantidade do ativo do cliente
        cursor.execute("UPDATE ClientAssets SET quantity = quantity + ? WHERE client_id = ? AND asset_symbol = ?", (quantity, client_id, asset_symbol))
    else:
        # Insere novo ativo para o cliente
        cursor.execute("INSERT INTO ClientAssets (client_id, asset_symbol, quantity) VALUES (?, ?, ?)", (client_id, asset_symbol, quantity))
    # Registra a transação
    timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO Transactions (client_id, asset_symbol, type, quantity, price, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (client_id, asset_symbol, 'BUY', quantity, total_cost, timestamp)
    )
    print(client_id, asset_symbol, 'BUY', quantity, total_cost, timestamp)
    conn.commit()
    conn.close()

def sell_asset(cursor, conn, client_id, asset_symbol, quantity, total_gain):
    # Adiciona o valor ao saldo do cliente
    cursor.execute("UPDATE Clients SET balance = balance + ? WHERE client_id = ?", (total_gain, client_id))
    # Atualiza quantidade disponível do ativo
    cursor.execute("UPDATE Assets SET available_quantity = available_quantity + ? WHERE asset_symbol = ?", (quantity, asset_symbol))
    # Verifica a quantidade do ativo do cliente
    cursor.execute("SELECT quantity FROM ClientAssets WHERE client_id = ? AND asset_symbol = ?", (client_id, asset_symbol))
    result = cursor.fetchone()
    if result and result[0] > quantity:
        # Atualiza a quantidade do ativo do cliente
        cursor.execute("UPDATE ClientAssets SET quantity = quantity - ? WHERE client_id = ? AND asset_symbol = ?", (quantity, client_id, asset_symbol))
    elif result and result[0] == quantity:
        # Remove o ativo do cliente se a quantidade for zero
        cursor.execute("DELETE FROM ClientAssets WHERE client_id = ? AND asset_symbol = ?", (client_id, asset_symbol))
    # Registra a transação
    timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO Transactions (client_id, asset_symbol, type, quantity, price, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (client_id, asset_symbol, 'SELL', quantity, total_gain, timestamp)
    )
    conn.commit()
    conn.close()
    
def get_transactions(cursor, timestamp):
    start_time, end_time = timestamp.split(';')
    start_time = datetime.strptime(start_time.strip(), "%Y-%m-%d %H:%M:%S").strftime("%y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time.strip(), "%Y-%m-%d %H:%M:%S").strftime("%y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM Transactions WHERE timestamp > ? AND timestamp < ?", (start_time, end_time))
    transactions = cursor.fetchall()
    return transactions

  
