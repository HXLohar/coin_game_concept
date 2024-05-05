import random

class block:
    def __init__(self, x=-1, y=-1, is_on_extra_reel = False):
        self.is_extra = is_on_extra_reel
        self.x = x
        self.y = y
        self.regular_symbol = ""
        self.regular_symbol_extra_info = 0
        self.coinflip_symbol = ""
        self.coinflip_symbol_extra_info = 0
        self.coinflip_base_value = 0
        self.oil_multiplier = 1

    def get_image(self):
        return ""

    def get_text(self):
        return ""

class board:
    def __init__(self):
        self.blocks = []

        for column in range(0, 6):
            for row in range(0, 6):
                if row > 0:
                    self.blocks.append(block(column, row))
                else:
                    self.blocks.append(block(column, row, True))
        self.oil_clusters = []
    def find_block(self, column, row):
        return self.blocks[column * 6 + row]
    def reset_board(self):
        pass


class round:
    def __init__(self, base_bet=1.0, extra_option="", tc_multiplier = 1.0):
        self.board = board()
        self.base_bet = base_bet
        self.total_cost = tc_multiplier * base_bet
        self.total_win = 0.0

        self.spin_option = extra_option
        self.bonus_type = 0
        self.spins_left = 0
    def reset_board(self):
        self.board.reset_board()
    def spin(self, reel_id):
        pass

    def convert_scatters(self):
        # 将 S 转换为 油桶
        pass

