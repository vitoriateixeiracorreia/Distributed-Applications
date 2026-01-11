from coincenter_data import Asset, User
from typing import Dict,List

class CoinCenterSkeleton:

    def __init__(self):
        self.assets:List[Asset] = []
        self.users:Dict[int,User] = {}

    def handle_request(self, request):
        user_id = int(request[-1])
        code = int(request[0])
        response = None

        if user_id not in self.users:
            self.users[user_id] = User(user_id)
        
        if code == 10:
            response = self.handle_add_asset(request[1:-1])
        elif code == 20 or code == 50:
            response = self.handle_get_all_assets(request[0:-1])
        elif code == 30:
            response = self.handle_remove_asset(request)
        elif code == 40 or code == 90:
            response = self.handle_exit(code)
        elif code == 60:
            response = self.handle_get_assets_balance(request)
        elif code == 70:
            response = self.handle_buy(request)
        elif code == 80:
            response = self.handle_sell(request)
        elif code == 100:
            response = self.handle_deposite(request[1:])
        elif code == 110:
            response = self.handle_withdraw(request[1:])
        
        return response


    def handle_add_asset(self, args):
        for asset in self.assets:
            if asset.symbol == args[1]:
                return [11,False]
        new_asset = Asset(args[1], args[0], args[2], args[3])
        self.assets.append(new_asset)
        return [11,True]

    def handle_get_all_assets(self, args):
        code = int(args[0])
        resp = [code+1, True]
        if self.assets:
            for asset in self.assets:
                resp.append(f"{asset.name};{asset.symbol};{asset.price};{asset.available_supply}")
            return resp
        else:
            return [code+1, False]

    def handle_remove_asset(self, args):
        before_rmv = len(self.assets)
        for asset in self.assets:
            if asset.symbol == args[1]:
                self.assets.remove(asset)
        if before_rmv != len(self.assets):
            return [31, True]
        return [31, False]
            

    def handle_get_assets_balance(self, args):
        this_user = self.users[args[1]]
        code = int(args[0])
        resp = [code+1, True]
        if this_user.balance or this_user.holdings:
            resp.append(this_user.balance)
            for asset_symbol, quantity in this_user.holdings.items():
                resp.append(f"{asset_symbol};{quantity}")
            return resp
        else:
            return [code+1, False]

    def handle_buy(self, args):
        quantity = int(args[2])
        user_id = int(args[-1])
        asset_symbol = args[1]

        asset_price = None
        this_asset = None
        this_user = self.users[user_id]

        for asset in self.assets:
            if asset.check_availability(quantity) and asset.symbol == asset_symbol:
                asset_price = asset.price
                this_asset = asset
                break
        
        if asset_price is None:
            return [71, False]

        if this_user.balance >= asset_price * quantity:
            self.handle_withdraw([str(asset_price * quantity) + " EUROS", user_id])
            if args[1] in this_user.holdings.keys():
                this_user.holdings[asset_symbol] += quantity
            else:
                this_user.holdings[asset_symbol] = quantity
            this_asset.decrease_quantity(quantity)
        else:
            return [71, False]

        return [71, True]

    def handle_sell(self, args):
        quantity = int(args[2])
        user_id = int(args[-1])
        asset_symbol = args[1]

        asset_price = None
        this_asset = None
        this_user = self.users[user_id]
        for asset in self.assets:
            if asset.symbol == asset_symbol:
                asset_price = asset.price
                this_asset = asset
                break
        
        existe = True
        for asset in self.assets:
            if asset_symbol == asset.symbol:
                existe = False
        
        if existe:
            return [81, False]

            
        total_quantity = this_user.holdings[asset_symbol]
        if asset_symbol in this_user.holdings and quantity <= total_quantity:
            self.handle_deposite([str(asset_price * quantity) + " EUROS", user_id])
            total_quantity -= quantity
            if total_quantity == 0:
                del this_user.holdings[asset_symbol]
            else:
                this_user.holdings[asset_symbol] -= quantity
            this_asset.increase_quantity(quantity)
        else:
            return [81, False]
        

        return [81, True]

    def handle_exit(self, args):
        return [args+1, True]

    def handle_deposite(self, args):
        this_user = self.users[args[-1]]
        amount = float(args[0].split()[0])
        

        if amount > 0:
            before_dep = this_user.balance
            this_user.balance += amount
            if this_user.balance != before_dep:
                return [101, True]
        
        return [101, False]

    def handle_withdraw(self, args):
        this_user = self.users[args[-1]]
        amount = float(args[0].split()[0])

        if 0 < amount <= this_user.balance:
            before_wd = this_user.balance
            this_user.balance -= amount
            if this_user.balance != before_wd:
                return [111, True]
        
        return [111, False]
