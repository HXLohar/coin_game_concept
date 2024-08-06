class math_model:
    def __init__(self, super_spin_price=None, bonus_buy_price=None):
        self.super_spin_price = super_spin_price
        self.bonus_buy_price = bonus_buy_price
        self.super_spin_functions = []
        self.bonus_buy_functions = []