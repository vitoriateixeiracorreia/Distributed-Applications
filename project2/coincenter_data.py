from typing import Dict,List


class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_supply:float):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.available_supply = available_supply

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

class User():
    def __init__(self, id):
        self.id = id    
        self.balance = 100
        self.holdings:Dict[str,float] = {}
