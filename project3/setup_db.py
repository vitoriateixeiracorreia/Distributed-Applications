import sqlite3
import os

def connect_db():
    db_path = os.path.expanduser('coincenter.db')  
    db_is_created = os.path.isfile(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    if not db_is_created:
        cursor.execute("""    
            CREATE TABLE Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT, --poe id automatico
            is_manager BOOLEAN NOT NULL,
            balance REAL --saldo do cliente
            );
        """)
        cursor.execute("""
            CREATE TABLE Assets (
            asset_symbol TEXT PRIMARY KEY,
            asset_name TEXT NOT NULL,
            price REAL NOT NULL,
            available_quantity INTEGER NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE ClientAssets (
            client_id INTEGER NOT NULL,
            asset_symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY(asset_symbol, client_id),
            FOREIGN KEY(asset_symbol) REFERENCES Assets(asset_symbol) ON DELETE CASCADE,
            FOREIGN KEY(client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE TABLE Transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            asset_symbol TEXT NOT NULL,
            type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME, 
            FOREIGN KEY(client_id) REFERENCES Clients(client_id),
            FOREIGN KEY(asset_symbol) REFERENCES Assets(asset_symbol)
            );
        """)
        cursor.execute("""
            INSERT INTO Assets (asset_symbol, asset_name, price, available_quantity) VALUES
            ('BTC', 'Bitcoin', 100000.0, 1),
            ('ETH', 'Ethereum', 2000.00, 10),
            ('AMZN', 'Amazon.com Inc.', 3400.00, 33),
            ('MSFT', 'Microsoft Corp.', 300.00, 20),
            ('TSLA', 'Tesla Inc.', 700.00, 6);
        """)
        cursor.execute("""
            INSERT INTO Clients (client_id, is_manager, balance) VALUES
            (0, 1, 10000.0);
        """)
        connection.commit()
    return connection, cursor