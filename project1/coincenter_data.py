"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Número de aluno: 62211
"""
from typing import Dict,List
from abc import ABC, abstractmethod

class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_supply:float):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.available_supply = available_supply

    def __str__(self):
        return f"{self.name} ({self.symbol}).........{self.price}$ | {self.available_supply}"

    def check_availability(self, quantity:int) -> bool:
        if 0 < quantity <= self.available_supply:
            return True
        return False

    def decrease_quantity(self, quantity:int) -> bool:
        if self.check_availability:
            self.available_supply -= quantity
            return True
        return False

    def increase_quantity(self, quantity):
        self.available_supply += quantity

class AssetController:
    assets:List[Asset] = []

    @staticmethod
    def list_all_assets()->str:
        string = "Available Assets: \n"
        string += "--------------------------------------------- \n"
        string += "Asset Name.........Price  |  Available Supply \n"
        string += "--------------------------------------------- \n"
        for asset in AssetController.assets:
           string += asset.__str__() +  "\n"
        string += "\n"
        return string
        
    
    @staticmethod
    def remove_asset(symbol:str):
        for asset in AssetController.assets:
            if asset.symbol == symbol:
                AssetController.assets.remove(asset)

    @staticmethod
    def add_asset(symbol:str,name:str,price:float,available_supply:int):
        for asset in AssetController.assets:
            if asset.symbol == symbol:
                return
        new_asset = Asset(symbol, name, price, available_supply)
        AssetController.assets.append(new_asset)



class Client(ABC):
    def __init__(self, id):
        self.id = id
    
    @abstractmethod
    def process_request(self,_):
        pass
    
class User(Client):
    def __init__(self, user_id:int):
        super().__init__(user_id)
        self.balance:float = 0
        self.holdings:dict[str, float] = {}

    def __str__(self):
        string = f"User: {self.id} \n"
        string += f"Balance: {self.balance} \n"
        string += "Holdings: \n"
        for asset_symbol, quantity in self.holdings.items():
            string += f"{asset_symbol}..........{quantity} \n"
        string += "\n"
        return string

    def deposite(self,amount):
        self.balance += amount

    def withdraw(self,amount):
        self.balance -= amount

    def buy_asset(self, asset_symbol:str, quantity:float) -> bool:
        assets = AssetController.assets
        asset_price = None
        this_asset = None

        for asset in assets:
            if asset.check_availability(quantity) and asset.symbol == asset_symbol:
                asset_price = asset.price
                this_asset = asset
                
                break
        
        if asset_price is None:
            return False

        if self.balance >= asset_price * quantity:
            self.withdraw(asset_price * quantity)
            if asset_symbol in self.holdings.keys():
                self.holdings[asset_symbol] += quantity
            else:
                self.holdings[asset_symbol] = quantity
            this_asset.decrease_quantity(quantity)

        return True

    def sell_asset(self, asset_symbol:str, quantity:float) -> bool:
        assets = AssetController.assets
        asset_price = None
        this_asset = None

        for asset in assets:
            if asset.symbol == asset_symbol:
                asset_price = asset.price
                this_asset = asset
                break
        
        total_quantity = self.holdings[asset_symbol]

        if asset_symbol in self.holdings.keys() and quantity <= total_quantity:
            self.deposite(asset_price * quantity)
            total_quantity -= quantity
            if total_quantity == 0:
                del self.holdings[asset_symbol]
            else:
                self.holdings[asset_symbol] -= quantity
            this_asset.increase_quantity(quantity)
        else:
            return False
        

        return True
    
    def process_request(self, request) -> str:

        
        if "GET_ASSETS_BALANCE" in request:
            if self.balance or self.holdings:
                return str(self)
        
        elif "GET_ALL_ASSETS" in request:
            if AssetController.assets:
                return AssetController.list_all_assets()

        elif "BUY" in request:
            if self.buy_asset(request[1], float(request[2])):
                return "OK"
        
        elif "SELL" in request:
            if self.sell_asset(request[1], float(request[2])):
                return "OK"
        

        elif "DEPOSIT" in request:
            if int(request[1].split()[0]) > 0:
                before_dep = self.balance
                self.deposite(int(request[1].split()[0]))
                if self.balance != before_dep:
                    return "OK"
             
        
        elif "WITHDRAW" in request:
            if 0 < int(request[1].split()[0]) <= self.balance:
                before_wd = self.balance
                self.withdraw(int(request[1].split()[0]))
                if self.balance != before_wd:
                    return "OK"

        return "NOK"

class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    def process_request(self, request):

        if "ADD_ASSET" in request:
            before_add = len(AssetController.assets)
            AssetController.add_asset(request[2],request[1],float(request[3]),int(request[4]))
            if len(AssetController.assets) != before_add:
                return f"OK; {request[2]}"
        
        elif "GET_ALL_ASSETS" in request:
            if AssetController.assets:
                return AssetController.list_all_assets()
        
        elif "REMOVE_ASSET" in request:
            before_add = len(AssetController.assets)
            AssetController.remove_asset(request[1])
            if len(AssetController.assets) != before_add:
                return f"OK; {request[1]}"
        
        return "NOK"

class ClientController:
    clients:Dict[int,Client] = {0:Manager(0)}

    @staticmethod
    def process_request(request:str)->str:
        ### código ###
        print(request)
        request = request.split(";")
        client_id = int(request[-1])
        
        if client_id not in ClientController.clients:
            ClientController.clients[client_id] = User(client_id)
        
        return ClientController.clients[client_id].process_request(request[:-1])            