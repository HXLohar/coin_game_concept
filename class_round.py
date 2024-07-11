import random
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
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

        self.appeared = False

    def get_image(self):
        if not self.appeared:
            return os.path.join(dir_path, "image", "blank.png")
        elif self.regular_symbol == "oil":
            return os.path.join(dir_path, "image", "oil_splash.png")
        elif self.regular_symbol == "":
            return os.path.join(dir_path, "image", "test.png")
        else:
            return os.path.join(dir_path, "image", f"{self.regular_symbol}.png")
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
        for obj in self.blocks:
            obj.regular_symbol = ""
            obj.regular_symbol_extra_info = 0
            obj.coinflip_symbol = ""
            obj.coinflip_symbol_extra_info = 0
            obj.coinflip_base_value = 0
            obj.oil_multiplier = 1
            obj.appeared = False

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
        print(f"DEBUG: ROUND.SPIN ({reel_id}) called")
        for i in range(0, 6):
            affected_block = self.board.find_block(reel_id, i)
            affected_block.appeared = True

    def convert_scatters(self):
        # 将 S 转换为 油桶
        pass

