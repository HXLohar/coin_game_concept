import class_math_model
import class_round
import random
# Model A
# The first model. The approach is straight forward: Everything has a certain probability to happen.
# No seeds involved (good seeds getting all sorts of good treatments and bad seeds getting absolutely nowhere)
# Viewer's discretion is advised.
# ---- ---- ----
# SUPER SPIN: only Super Spin 2 is implemented for now
# Guaranteed "Fire in the Hole", plus 2 oil barrels.
# ---- ---- ----
# BONUS BUY: only 3S buy is implemented for now
SUPER_SPIN_PRICE = [8, 20, 36, 120, 400]
BONUS_BUY_PRICE = [85, 280, 760, 2100]

CONST_REGULAR_OIL_UPGRADE_CHANCE = 0.2
CONST_BIG_OIL_UPGRADE_CHANCE = 0.15
CONST_MEGA_OIL_UPGRADE_CHANCE = 0.1

CONST_OIL_LIMIT = 8
def SUPER_SPIN(mode=2):
    PARAM_FITH_CHANCE = 1.0
    PARAM_EXTRA_OIL_CHANCE = 0.175
    PARAM_OIL_BARRELS = [2, 0, 0, 0]
    this_round = class_round.round
    # Place "Fire in the Hole" on the top reel
    if random.random() <= PARAM_FITH_CHANCE:
        this_round.board.find_block(random.randint(0, 5), 0).regular_symbol = "fire_in_the_hole"
    # Perform a loop with a RNG each time. Break the loop if sum(PARAM_OIL_BARRELS) >= CONST_OIL_LIMIT, or RNG is >=PARAM_EXTRA_OIL_CHANCE.
    # Every time add 1 to PARAM_OIL_BARRELS[0]
    while sum(PARAM_OIL_BARRELS) < CONST_OIL_LIMIT and random.random() <= PARAM_EXTRA_OIL_CHANCE:
        PARAM_OIL_BARRELS[0] += 1
    # Upgrade and place oil barrels
    for i in range(len(PARAM_OIL_BARRELS)):
        for _ in range(PARAM_OIL_BARRELS[i]):
            # Attempt to upgrade the barrel
            if i < len(PARAM_OIL_BARRELS) - 1 and random.random() <= \
                    [CONST_REGULAR_OIL_UPGRADE_CHANCE, CONST_BIG_OIL_UPGRADE_CHANCE, CONST_MEGA_OIL_UPGRADE_CHANCE][i]:
                PARAM_OIL_BARRELS[i] -= 1
                PARAM_OIL_BARRELS[i + 1] += 1
            else:
                # Place the barrel on the board
                while True:
                    x, y = random.randint(0, 5), random.randint(1, 5)
                    if this_round.board.find_block(x, y).regular_symbol == "":
                        this_round.board.find_block(x, y).regular_symbol = \
                        ["oil_barrel_regular", "oil_barrel_big", "oil_barrel_mega", "oil_barrel_giga"][i]
                        break

    return this_round

def BONUS_BUY(mode):
    this_round = class_round.round
    return this_round

MODEL = class_math_model.math_model(SUPER_SPIN_PRICE, BONUS_BUY_PRICE)
MODEL.super_spin_functions.append(SUPER_SPIN)
MODEL.bonus_buy_functions.append(BONUS_BUY)